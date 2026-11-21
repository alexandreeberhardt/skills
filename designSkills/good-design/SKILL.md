---
name: good-design
description: Conçoit ou relit n'importe quel objet de design (interface, page d'accueil, titre, produit, API, slide, document, schéma) avec 14 tests concrets tirés de « Taste for Makers » de Paul Graham - le bon design est simple, répond au vrai problème, laisse de la place à l'utilisateur, assume ses sacrifices, se refait, vieillit bien et se vérifie en regardant quelqu'un s'en servir. Utiliser dès que l'utilisateur demande « est-ce que c'est bien conçu », « c'est du bon design ? », un avis sur une page, un écran, un titre ou un produit, veut simplifier quelque chose, hésite entre deux versions, ou invoque /good-design. Ce skill juge le fond du design, pas le style visuel (polices, couleurs et animations relèvent des autres skills de design).
---

# Good design

Source : Paul Graham, « Taste for Makers » (2002), paulgraham.com/taste.html.

Idée centrale : le bon design est simple. La simplicité oblige à affronter le vrai problème, et ce qui a l'air rangé n'est pas forcément simple à utiliser.

Chaque test est une question avec une réponse observable. Ne pas dire « c'est plus clair » : dire ce que la personne fait, lit ou demande.

## Choisir les tests

Ne pas passer les 14 à chaque fois. Commencer par les tests du type d'objet, ajouter les autres seulement s'ils révèlent quelque chose.

| Objet | Tests à passer d'abord |
|---|---|
| Écran, interface, formulaire | 1, 3, 5, 8, 14 |
| Page d'accueil, titre, texte, slide | 2, 4, 6, 8, 9 |
| Produit, fonctionnalité, API | 1, 5, 7, 11, 14 |
| Choix entre deux versions | 1, 7, 9, 13 |
| Création à partir de rien | voir « Concevoir » plus bas |

## Les tests

### Le vrai problème

**1. Le bouton de la cuisinière : simple pour qui ?**
Quatre feux en carré. Des boutons en ligne font propre, mais il faut lire un schéma pour savoir lequel commande le feu du fond à gauche. Des boutons en carré comme les feux : on garde les yeux sur la casserole.
Test : pour chaque choix qui « fait propre », vérifier si l'utilisateur doit s'arrêter pour réfléchir. Si une légende, une infobulle ou un mode d'emploi est nécessaire, la disposition répond à la mauvaise question.

**2. Le g et le y : joli ou lisible ?**
Au milieu du vingtième siècle, la mode était au texte sans empattement. Pourtant un g minuscule en Times se distingue d'un y au premier coup d'œil.
Test : dire ce que l'objet doit faire en premier (être lu, être trouvé, être compris en trois secondes). Vérifier que le choix esthétique ne le dégrade pas.

**3. Peut-on changer la question ?**
En logiciel, un problème insoluble se remplace souvent par un problème équivalent facile à résoudre.
Test : avant d'améliorer un écran ou une étape, demander si l'utilisateur en a besoin. La meilleure correction supprime parfois l'étape entière.

### Simple

**4. Le dirais-tu à voix haute ?**
Un titre comme « Enable seamless collaboration across environments » ne se dit pas à la table de la cuisine. On dirait : « Ouvre ce dossier. Tu verras le fichier sur lequel je travaille. » Voilà le titre.
Test : lire chaque texte à voix haute comme à un ami. Si la phrase sonne faux, écrire ce qu'on dirait vraiment. Vaut pour les titres, boutons, messages d'erreur.

**5. Le col de dentelle : que reste-t-il sans l'ornement ?**
Une nature morte de quelques objets bien observés vaut mieux qu'un col de dentelle peint avec brio. L'ornement sert souvent à cacher une forme fade.
Test : retirer mentalement dégradés, icônes décoratives, adjectifs, animations. Si ce qui reste est vide, le problème est le fond. Quand on ne peut pas livrer d'ornement, on doit livrer de la substance.

**6. Jane Austen : faut-il vraiment tout décrire ?**
Ses romans ne contiennent presque aucune description, et chacun se fait sa propre histoire de la Joconde.
Test : repérer ce qui explique ce que la personne aurait compris seule (sous-titre qui répète le titre, texte qui décrit l'image). Le couper.

**7. Lego : y a-t-il un bouton « château » ?**
Une brique fait partie d'un château aujourd'hui et du nez d'un vaisseau demain. Lego n'a pas besoin d'un bouton château.
Test : repérer les fonctions faites pour un seul usage prévu d'avance. Les remplacer, quand c'est possible, par quelques éléments de base que la personne combine comme elle veut.

### Les décisions

**8. Porsche : qu'est-ce qui a été sacrifié ?**
Le prototype de 1960 avait quatre vraies places. Réduire les sièges arrière a permis d'abaisser le toit : cette décision se voit depuis le trottoir d'en face.
Test : nommer ce que le design a abandonné pour obtenir sa qualité principale. Si rien n'a été abandonné, aucune décision n'a été prise et le résultat sera moyen partout.

**9. Le sac du grimpeur : qu'est-ce qu'on jette ?**
En montagne, on se débarrasse de tout ce qui ne sert pas. Un terrain difficile ou un petit budget donnent souvent les bâtiments les plus élégants.
Test : imposer une contrainte dure (un seul écran, une seule phrase, moitié moins de champs) et voir ce qui survit. Ce qui tombe sans regret était de trop.

**10. La symétrie a-t-elle remplacé la réflexion ?**
La symétrie est un moyen d'être simple, mais elle peut dispenser de penser.
Test : pour chaque grille, répétition ou paire équilibrée (trois cartes, deux colonnes égales), vérifier que le contenu a vraiment cette forme. Trois cartes pour deux idées : en retirer une.

### Le travail

**11. Léonard : où est l'œil ?**
Dans certains croquis, on compte cinq ou six essais pour un seul trait. Déplacer une branche de cinq degrés ne change rien. Faire la même chose à un œil ruine le visage.
Test : trouver l'« œil » du design, l'endroit où une petite erreur se voit tout de suite (première phrase, action principale, écran d'arrivée). Le refaire plusieurs fois et comparer. Ne pas dépenser cet effort sur les « branches ».

**12. Copie-t-on sans le savoir ?**
Au dix-neuvième siècle, on imitait Raphaël à travers des imitateurs, sans s'en rendre compte. Les meilleurs prennent chez n'importe qui, en le sachant, et préfèrent avoir raison qu'être originaux.
Test : pour chaque élément repris d'ailleurs (section « héros », trois colonnes d'avantages, menu habituel), dire quel problème il règle ici. Sans réponse, c'est une imitation : l'enlever. Avec une réponse, le garder sans gêne. Ne pas gommer non plus ce qui est étrange mais juste.

### La vérification

**13. Est-ce que ça aurait marché en 1500 ?**
Montrer le travail à quelqu'un d'il y a cinq siècles : il raterait toutes les références à la mode. Qu'aimerait-il encore ?
Test : enlever mentalement ce qui tient à la mode du moment (effet visuel en vogue, jargon, référence d'actualité). S'il ne reste rien, le design vieillira mal.

**14. Trouver le bouton de cuisinière de son produit**
Donner à quelqu'un une vraie tâche. S'asseoir sur ses mains. Guetter la première fois où la personne se retourne et demande : « Lequel ? »
Test : le seul qui ne se fait pas de tête. Si un utilisateur réel est disponible, le proposer : une tâche, aucune aide, noter chaque hésitation. Sinon, dérouler la tâche pas à pas à la place d'un débutant et marquer chaque endroit où il faut choisir sans indice. Dire clairement que c'est une simulation.

## Relire un design existant

1. Regarder l'objet réel (capture, page ouverte, code lancé), pas sa description. S'il n'est pas accessible, le demander.
2. Dire en une phrase à quoi il sert et pour qui. Si c'est impossible, le problème est là : le signaler avant tout le reste.
3. Passer les tests choisis. Sauter ceux qui ne s'appliquent pas.
4. Rendre le résultat sous cette forme, sans rien ajouter :

```text
Sert à : <une phrase>

Le plus grave
<défaut> (test <n>)
Avant : <ce qui existe>
Après : <le changement proposé>

Ensuite
- <défaut> (test <n>) : <avant> -> <après>
- ...

À garder
- <ce qui est déjà bon>
```

5. Trois à cinq défauts au maximum, du plus grave au moins grave. Un défaut grave est un endroit où l'utilisateur se trompe ou abandonne ; un défaut mineur le ralentit seulement.
6. Si l'utilisateur demande d'appliquer : faire les changements, vérifier le résultat sur l'objet réel, repasser les tests concernés.

## Concevoir quelque chose de nouveau

1. Écrire la tâche principale de l'utilisateur en une phrase dite à voix haute (test 4).
2. Vérifier que c'est la bonne question (tests 1 et 3).
3. Choisir le sacrifice avant de dessiner (test 8) et le dire à l'utilisateur.
4. Faire la version la plus simple qui suit le geste de la personne (tests 5, 7, 9).
5. Refaire l'« œil » au moins trois fois et garder la meilleure version (test 11).
6. Vérifier avec les tests 13 et 14, puis livrer avec une ligne : ce qui a été sacrifié et pourquoi.

## Règles

- Pas de principe général sans exemple tiré de l'objet examiné. Citer le texte, l'élément ou l'étape en cause.
- Enlever avant d'ajouter. Si une correction ajoute un élément, vérifier d'abord qu'on ne peut pas régler le problème en supprimant ou en déplaçant.
- Ne pas confondre rangé et simple : alignement, symétrie et minimalisme visuel ne passent pas le test 1 à eux seuls.
- Ne pas inventer de réaction d'utilisateur. Une observation réelle et une simulation ne se présentent pas de la même façon.
- Partir d'un défaut que l'on voit, pas d'un idéal : il est plus facile de voir ce qui est laid que d'imaginer ce qui serait beau. Se demander « quel bricolage, il doit y avoir mieux », puis chercher ce mieux.
- Si tout passe, le dire en une ligne et ne rien proposer.
