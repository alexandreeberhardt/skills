---
name: plan-strategique
description: Construit ou met à jour un plan stratégique avec la méthode d'Arthur Perticoz en 7 étapes - partir de l'objectif, décrire froidement le point de départ, poser les jalons en remontant de l'objectif, détailler chaque saut en plan d'action, exécuter, faire le bilan, refaire le plan. Utiliser dès que l'utilisateur veut atteindre un objectif ambitieux et demande une stratégie, un plan, une feuille de route, des étapes ou « par où commencer » (startup, levée de fonds, projet perso, carrière, études, contenu), quand il veut faire le point sur un plan existant, ou quand il invoque /plan-strategique, même s'il ne cite pas la méthode.
---

# Plan stratégique, méthode Perticoz

La plupart des gens partent de leur situation actuelle et se fixent un objectif à sa mesure. Ici, on part de l'objectif, on remonte jusqu'à aujourd'hui, puis on avance saut par saut en corrigeant le plan à chaque bilan. Le plan sert autant à décider qu'à raconter : où je vais, d'où je pars, par quelles étapes.

## Deux cas

- **Nouveau plan** : dérouler les étapes 1 à 4, puis préparer 5 et 6.
- **Plan existant** (l'utilisateur revient avec des résultats, ou un fichier de plan est déjà là) : faire directement les étapes 6 et 7.

## Avant de commencer

Récupérer ce qui est déjà connu : conversation, fichiers du dossier, mémoire. Le plan ne vaut que par l'exactitude du point de départ, donc ne rien inventer sur la situation de l'utilisateur. S'il manque l'objectif ou des faits essentiels sur le départ, les demander en une seule fois, en peu de questions. Pour le reste, poser une hypothèse raisonnable et la marquer comme telle.

## Les 7 étapes

### 1. Objectif
Fixer le point d'arrivée sans regarder la situation actuelle. C'est l'étape où l'on rêve : si l'objectif proposé semble dimensionné par les moyens du moment, le dire et proposer une version plus ambitieuse. Le formuler de façon vérifiable : un chiffre ou un état observable, et une échéance.

### 2. Point de départ
Décrire froidement où on en est par rapport à cet objectif : chiffres, acquis, ressources, manques. Ne pas embellir et ne pas ménager l'utilisateur, un départ flatté fausse tous les sauts qui suivent.

### 3. Jalons
Partir de l'objectif et remonter vers le départ : « qu'est-ce qui doit être vrai juste avant ? ». Garder 3 à 5 jalons qui s'enchaînent logiquement, chacun vérifiable. C'est la stratégie.

### 4. Sauts
Repartir dans l'autre sens, du départ vers l'objectif. Pour chaque passage d'un jalon au suivant :
- le critère de réussite, qualitatif et chiffré ;
- ce dont on a besoin (argent, personnes, compétences, temps) ;
- les actions concrètes ;
- l'échéance.

C'est le plan d'action, et l'étape qui demande le plus de précision. Détailler à fond le premier saut ; les suivants peuvent rester plus grossiers, ils seront refaits à l'étape 7. Si un saut paraît infaisable, c'est qu'il manque un jalon : revenir à l'étape 3.

### 5. Exécution
Seul le premier saut se travaille maintenant. Le traduire en actions de la semaine et du mois. Si l'utilisateur le demande, l'aider à les réaliser.

### 6. Bilan
À l'échéance du saut, comparer froidement le résultat au critère fixé : atteint ou non, et pourquoi. Distinguer ce qui vient de l'exécution, d'une hypothèse fausse, ou de l'extérieur. Être honnête et dur, sans chercher d'excuse ni de coupable.

### 7. Mise à jour
Prendre du recul et refaire le plan depuis le nouveau point de départ : l'objectif tient-il toujours (il peut changer), où en est-on, quels jalons restent valables. Puis recommencer à l'étape 4.

## Rendu

Écrire le plan dans un fichier `plan-<sujet>.md` dans le dossier courant, pour pouvoir y revenir au bilan. Court, sans paragraphe de remplissage :

```markdown
# Plan : <sujet>
Version <n>, <date>

## Objectif
## Point de départ
## Jalons
| # | Jalon | Critère | Échéance |
## Sauts
### Saut 1 : <départ> vers <jalon 1>
Critère, besoins, actions, échéance
### Saut 2 ...
## Prochain bilan
Date, et ce qu'on mesurera
## Hypothèses
Ce qui a été supposé faute d'information
```

Lors d'une mise à jour, garder le même fichier : incrémenter la version et ajouter en bas une section `## Bilan du <date>` avec le résultat, les causes et ce qui change dans le plan.

Dans la réponse, donner seulement l'objectif, les jalons, le premier saut et la date du prochain bilan.

## Limites à garder en tête

- Ce n'est pas une science exacte, et un plan sérieux pour une entreprise se travaille sur des semaines. Un premier jet sert de base, pas de vérité.
- Ne pas imposer la méthode à une demande qui n'en a pas besoin : une petite tâche ou une question ponctuelle se traite directement.
- Pour un pitch, le plan se résume en une dizaine de slides : objectif, départ, jalons, sauts, besoins.
