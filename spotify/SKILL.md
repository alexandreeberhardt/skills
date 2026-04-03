---
name: spotify
description: Add tracks to the Spotify queue on the active device, using cached Spotify OAuth credentials to avoid reauthorizing each time. Use when the user asks to queue tracks, replay a saved playlist idea, or automate Spotify playback actions from Python.
---

# Spotify

Use this skill when the user wants to add tracks to Spotify from this machine without rebuilding the OAuth flow each time.

## History source

Use this folder as the canonical source for the user's extended Spotify history when recommendations should be based on real listening data:

`<SPOTIFY_EXTENDED_STREAMING_HISTORY_DIR>`

Prefer these files when building recommendations:

- `spotify_analysis_report.md` for high-level patterns and top artists/tracks
- `spotify_analysis_summary.json` for structured aggregates
- `Streaming_History_Audio_*.json` for raw listening history when a more precise or recent filter is needed

When the user asks for suggestions based on their own taste, start from this folder before using generic music knowledge.

## Hard exclusions

If needed, define user-specific artist exclusions in a local untracked note or inject them at runtime. Do not store personal taste filters directly in this repository.

## Workflow

1. Use `scripts/spotify_queue.py`.
2. On first use, let the script prompt for `client_id` and `client_secret`, then complete the Spotify authorization in the browser.
3. The script stores credentials and a refresh token in local files inside the skill folder with restrictive permissions.
4. On later runs, reuse the saved refresh token automatically.

## Requirements

- The Spotify app or another Spotify player must already be active and playing on the target device.
- The Spotify Developer app must allow this redirect URI exactly:
  `http://127.0.0.1:8888/callback`

## Common commands

Queue the default cleaning playlist:

```bash
python3 ~/.codex/skills/spotify/scripts/spotify_queue.py
```

Queue custom tracks:

```bash
python3 ~/.codex/skills/spotify/scripts/spotify_queue.py \
  --track "Artist One|Track One" \
  --track "Artist Two|Track Two"
```

## Notes

- Track arguments use the format `Artist|Title`.
- If token refresh fails, rerun the script and complete the authorization flow again.
