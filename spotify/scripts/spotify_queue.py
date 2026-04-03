#!/usr/bin/env python3
import argparse
import json
import os
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from getpass import getpass
from pathlib import Path


REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPES = ["user-modify-playback-state", "user-read-playback-state"]
DEFAULT_TRACKS = [
    ("Artist One", "Track One"),
    ("Artist Two", "Track Two"),
]


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def secrets_path() -> Path:
    return skill_root() / ".spotify_client.json"


def token_path() -> Path:
    return skill_root() / ".spotify_token.json"


def save_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload, indent=2) + "\n")
    os.chmod(path, 0o600)


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text())


def api_request(method: str, url: str, *, headers=None, data=None):
    req = urllib.request.Request(url, method=method, headers=headers or {}, data=data)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return resp.status, raw.decode("utf-8") if raw else ""
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{exc.code} {exc.reason}: {detail}") from exc


def token_request(form: dict) -> dict:
    payload = urllib.parse.urlencode(form).encode("utf-8")
    _, body = api_request(
        "POST",
        "https://accounts.spotify.com/api/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=payload,
    )
    return json.loads(body)


def refresh_access_token(client_id: str, client_secret: str, refresh_token: str) -> dict:
    return token_request(
        {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
        }
    )


def exchange_code_for_token(client_id: str, client_secret: str, code: str) -> dict:
    return token_request(
        {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": client_id,
            "client_secret": client_secret,
        }
    )


def ensure_credentials() -> tuple[str, str]:
    env_id = os.getenv("SPOTIFY_CLIENT_ID")
    env_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    if env_id and env_secret:
        return env_id, env_secret

    saved = load_json(secrets_path()) or {}
    client_id = saved.get("client_id") or input("Spotify client id: ").strip()
    client_secret = saved.get("client_secret") or getpass("Spotify client secret: ").strip()
    if not client_id or not client_secret:
        raise RuntimeError("Spotify client id and client secret are required.")
    if saved.get("client_id") != client_id or saved.get("client_secret") != client_secret:
        save_json(secrets_path(), {"client_id": client_id, "client_secret": client_secret})
    return client_id, client_secret


def authorize(client_id: str, client_secret: str) -> dict:
    state = secrets.token_urlsafe(24)
    params = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "scope": " ".join(SCOPES),
            "state": state,
            "show_dialog": "false",
        }
    )
    auth_url = f"https://accounts.spotify.com/authorize?{params}"
    print("Open this URL and approve access:")
    print(auth_url)
    print()
    print("When the browser fails to open the local callback, copy the full redirect URL and paste it here.")
    callback_url = input("Redirect URL: ").strip()
    parsed = urllib.parse.urlparse(callback_url)
    result = urllib.parse.parse_qs(parsed.query)
    error = result.get("error", [None])[0]
    code = result.get("code", [None])[0]
    returned_state = result.get("state", [None])[0]
    if error:
        raise RuntimeError(f"Spotify authorization failed: {error}")
    if not code:
        raise RuntimeError("No authorization code found in redirect URL.")
    if returned_state != state:
        raise RuntimeError("Invalid OAuth state returned by Spotify.")
    token_data = exchange_code_for_token(client_id, client_secret, code)
    save_token_payload(token_data)
    return token_data


def save_token_payload(token_data: dict):
    payload = {
        "access_token": token_data["access_token"],
        "expires_at": int(time.time()) + int(token_data.get("expires_in", 3600)) - 30,
    }
    if token_data.get("refresh_token"):
        payload["refresh_token"] = token_data["refresh_token"]
    else:
        existing = load_json(token_path()) or {}
        if existing.get("refresh_token"):
            payload["refresh_token"] = existing["refresh_token"]
    save_json(token_path(), payload)


def ensure_access_token(client_id: str, client_secret: str) -> str:
    token_data = load_json(token_path()) or {}
    if token_data.get("access_token") and token_data.get("expires_at", 0) > time.time():
        return token_data["access_token"]
    if token_data.get("refresh_token"):
        refreshed = refresh_access_token(client_id, client_secret, token_data["refresh_token"])
        save_token_payload(refreshed)
        return load_json(token_path())["access_token"]
    fresh = authorize(client_id, client_secret)
    return fresh["access_token"]


def get_active_device_id(token: str) -> str | None:
    status, body = api_request(
        "GET",
        "https://api.spotify.com/v1/me/player/devices",
        headers={"Authorization": f"Bearer {token}"},
    )
    if status != 200:
        return None
    devices = json.loads(body).get("devices", [])
    for device in devices:
        if device.get("is_active"):
            return device["id"]
    return None


def search_track_uri(token: str, artist: str, track: str) -> tuple[str | None, dict | None]:
    query = f'track:"{track}" artist:"{artist}"'
    params = urllib.parse.urlencode({"q": query, "type": "track", "limit": 5})
    status, body = api_request(
        "GET",
        f"https://api.spotify.com/v1/search?{params}",
        headers={"Authorization": f"Bearer {token}"},
    )
    if status != 200:
        return None, None
    items = json.loads(body).get("tracks", {}).get("items", [])
    if not items:
        return None, None
    exact = next(
        (
            item
            for item in items
            if item.get("name", "").casefold() == track.casefold()
            and any(a.get("name", "").casefold() == artist.casefold() for a in item.get("artists", []))
        ),
        None,
    )
    chosen = exact or items[0]
    return chosen["uri"], chosen


def queue_track(token: str, uri: str, device_id: str | None):
    params = {"uri": uri}
    if device_id:
        params["device_id"] = device_id
    query = urllib.parse.urlencode(params)
    api_request(
        "POST",
        f"https://api.spotify.com/v1/me/player/queue?{query}",
        headers={"Authorization": f"Bearer {token}"},
    )


def parse_track_arg(value: str) -> tuple[str, str]:
    if "|" not in value:
        raise argparse.ArgumentTypeError("Track must use the format Artist|Title")
    artist, title = value.split("|", 1)
    artist = artist.strip()
    title = title.strip()
    if not artist or not title:
        raise argparse.ArgumentTypeError("Track must use the format Artist|Title")
    return artist, title


def parse_args():
    parser = argparse.ArgumentParser(description="Queue Spotify tracks on the active device.")
    parser.add_argument("--device-id", default=os.getenv("SPOTIFY_DEVICE_ID"))
    parser.add_argument("--track", action="append", type=parse_track_arg, default=[])
    parser.add_argument("--reauthorize", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    client_id, client_secret = ensure_credentials()
    if args.reauthorize:
        if token_path().exists():
            token_path().unlink()
    token = ensure_access_token(client_id, client_secret)
    device_id = args.device_id or get_active_device_id(token)
    if not device_id:
        print("No active Spotify device found. Start playback first or pass --device-id.")
        return 2

    tracks = args.track or DEFAULT_TRACKS
    failures = []
    for artist, title in tracks:
        uri, item = search_track_uri(token, artist, title)
        if not uri:
            failures.append(f"{artist} - {title}: not found")
            continue
        try:
            queue_track(token, uri, device_id)
            found_artists = ", ".join(a["name"] for a in item.get("artists", []))
            print(f"Queued: {found_artists} - {item['name']}")
        except RuntimeError as exc:
            failures.append(f"{artist} - {title}: {exc}")

    if failures:
        print()
        print("Some tracks were not queued:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
