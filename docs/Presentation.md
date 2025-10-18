# Presentation

<img style="float: right;" src="./assets/link.png" alt="link" width="200"/>

## whoami

Bonjour je m'appelle Simon Harvey.  Je travaille presenement chez Desjardins dans l'equipe de Securite Applicative (aka AppSec).  Precedamment, j'etais plutot dans l'industrie aerospatiale chez Pratt & Whitney Canada ainsi que Bombardier Aeronautique.

Aujourd'hui, je suis ici avec vous pour vous parler de DevSecOps, plus precisement comment on peut encourager les developpeurs a s'engager dans un mindset shift-left via l'utilisation de pre-commit hooks.  Je suis pas ici pour vous vendre un outil mais plutot partager des idees qui pourraient aider vos pratiques de developpement.

## Introduction

> Vaut mieux prevenir que guerir

Il est plus sage de prendre des mesures pour éviter un problème que d'attendre qu'il survienne pour essayer de le résoudre.  C'est essentiellement le concept des pre-commit hooks.  En utilisant des pre-commit hook, on active le shift-left en prevenant l'ajout de code possiblement problematique a l'histoire `git`.

![Shift-Left](./assets/shift-left.png)

Ce graphique provenant de [Applied Software Measurement: Global Analysis of Productivity and Quality](https://www.accessengineeringlibrary.com/binary/mheaeworks/829ef30c60b20d92/96af26c048a067d5d3bec53ac2b2c7ddc143c27fbf02f78bc72c6894d93f431a/book-summary.pdf) demontre les couts associes a l'introduction des defectuosites et ou ses introductions se produisent.[^1]

Des lors, l'idee du **shift-left** c'est de deplacer les capacites de detections "vers la gauche" plus pres des d'ou ses defectuosites sont crees et introduites dans le code.

On demande aux developpeurs soudainement d'inclure de nouveaux outils et pratiques dans leur flux de travail:

- Oublie pas d'executer les tests unitaires localement
- Fait un balayage de tes commits pour des fuites de secrets
- SVP lint le code selon nos obscures conventions
- Nouvelle politique que les CI actions doivent etre `SHA pinned`
- Et tout le reste qu'on veut bien inventer

Ces ajouts créent une charge mentale supplémentaire pour les développeurs.  Ceux-ci doivent maintenant considérer une checklist et une multitude de nouvelles tâches à faire mécaniquement.  Cette charge mentale accrue en plus de la complexité inhérente à leur travail rends l'acceptation du shift-left difficile.  Les devs ne sont pas paresseux et il faut les outiller avec des automatisations.

### pyquiz

Pour la presentation, j'ai decide de batir une petite application simple en `python`.  Cette application est un petit quiz dans un terminal.  Le but c'est que plutot d'observer passivement une presentation, je vous propose une demarche etape par etape.

Biensur, qu'aujourd'hui je presente des outils et une approche, l'utilisation de celle-ci reste a contextualiser selon vos besoins et votre realite.  C'est aussi un peu comme les show de cuisines, tout est preparer backstage.

## git

On estime qu'environ 83% des developpeurs utilisent le système `git` comme gestionnaire de version du code.  Dans sa sagesse infinie, Linus Torvalds a su inclure les fonctionnalité de `git hook` dès la première version de `git` en 2005.  À l'époque les `git hook` étaient des agent d'intégration continue (CI) minimaliste.

Les `git hooks` sont des points dans le cycle de vie du processus `git` qui avant ou après des actions permettent l'exécution de scripts.

![Lifecycle](./assets/lifecycle.png)

Il existe deux type de `git hooks`:

- Server-side: S'exécute sur le serveur du gestionnaire de code **DANGER**
- Client-side:S'exécute sur le poste du développeur après activation... Le dive du sujet aujourd'hui.

### `cd .git/hooks`

Regardons le fonctionnement des `git hooks` natifs.  Lorsqu'on initialise une nouveau dépot git (aka `git init`) par défault une pléthore de `git hooks` sont inclus comme exemple.  Ceux-ci possède l'extension `*.sample` qui désactive leur fonctionnement initialement, il suffit d'enleve cette extension pour les activer.

Voyons de plus près comment on fabriquer et utiliser notre premier **hooks**.

```bash
cp docs/prep/1.1/pre-commit .git/hooks
```

On voit dans notre exemple que certain de nos tests unitaires ne fonctionne pas.  Ici nous empêchons l'ajout d'un commit supplémentaire puisque le politiques du projet imposent le succès de ceux-ci via un `git hook`.

Voyons un deuxième exemple plus évolué...

```bash
cp docs/prep/1.2/pre-commit .git/hooks
```

Cette exemple est plus complexe, commence à inclure du error handling, des configurations diverses, etc... On peut donc s'imaginer que cette approche sera lourde à orchestrer si on souhaite appliquer toutes les politiques des pratiques de devs et de la sécurité applicative...

De plus, il y a un éléphant dans la pièce... Les `git hooks` natifs sont considéré un **objet** spéciale par `git` c'est-à-dire qu'ils ne sont pas sous controle des révisions ce qui amène plusieurs problèmes:

- La distribution est pénible
- La gestion des version
- Installation dans multiple dépots

## Frameworks

Une pléthore d'outils outils open-source tentent de résoudre ces problème avec différentes approches.  Sans tous les nommer:

- [Pre-Commit](https://pre-commit.com/) - A framework for managing and maintaining multi-language pre-commit hooks
- [Husky](https://typicode.github.io/husky/) - Git hooks made easy 🐶 woof!
- [CaptainHook](https://github.com/captainhook-git/captainhook) - Git hooks manager for PHP developers
- [Git Build Hook Maven Plugin](https://github.com/rudikershaw/git-build-hook) - Install Git hooks and config during a Maven build
- [Lefthook](https://github.com/evilmartians/lefthook) - Fast and powerful Git hooks manager for any type of projects
- [Overcommit](https://github.com/sds/overcommit) - A fully configurable and extendable git hook manager
- [Simple-git-hooks](https://github.com/toplenboren/simple-git-hooks) - A simple git hooks manager for small projects
- [Prek](https://github.com/j178/prek) - ⚡ Better `pre-commit`, re-engineered in Rust

### pre-commit.com

Pour les fins de la démonstration, utilisons le framework écrit en python `Pre-Commit.com` mais tous fonctionne sensiblement avec une méthodologie similaire avec des résultats équivalents.  L'objectif étant de créer un niveau d'abstraction entre le déploiement des `git hook` un et framework plus neutre et conviviable.

1. Pour installer `Pre-Commit`...

   ```bash
   pip install pre-commit
   uv tool install pre-commit
   ```

2. Installer le framework dans le dépot

   ```bash
   pre-commit --version
   pre-commit install --allow-missing-config
   ```

3. Configurer le fichier `pre-commit-config.yaml`

   ```bash
   cp docs/prep/2.1/not.pre-commit-config.yaml .pre-commit-config.yaml
   ```

On vient de déployer une configuration qui est facile à distribuer, versionner et qui s'installe facilement pour les utilisateurs.

### trufflehog

La fuite de secret est clairement un des enjeux les plus populaires des dernières années.  Par la nature de `git` un secret ajouté dans l'historique du gestionnaire de code qui fuit devient dangereux.  Un des `pre-commit hook` les plus pertinent à déployer touche la détection des secrets.

Pour des fin de démonstration, assumons que l'utilitaire de détection `trufflehog` est disponible pour balayer notre dépot de code.

1. Pour installer `trufflehog`...

   ```bash
    trufflehog --version
   ```

2. Configurer le fichier `pre-commit-config.yaml`

   ```bash
   cp docs/prep/2.2/not.pre-commit-config.yaml .pre-commit-config.yaml
   ```

Maintenant à chaque commits, nous sommes en mesure de scanner le dépot de code pour une fuite de secret directement sur le poste du déveleppeur.  En cas de fuite, le commit est omis et la fuite est contenu localement.  Le développeur peut ainsi résoudre le problème avant de polluer l'historique `git`.

### Linting, Skipping et Pinning

La prochaine charge mentale qui touche les développeurs est souvent en lien avec les conventions de code.  L'utilisation du `pre-commit` peut décharger mentalement ceux-ci et automatiser une tâche plutôt répétitive en action automagique.

1. Configurer le fichier `pre-commit-config.yaml`

   ```bash
   cp docs/prep/2.3/not.pre-commit-config.yaml .pre-commit-config.yaml &&
   cp -r docs/prep/2.3/.config .config/
   ```

2. Exécution **ad-hoc**

   ```bash
   pre-commit run --all-files
   SKIP=trufflehog pre-commit run --all-files
   ```

3. Ne pas exécuter le pre-commit

   ```bash
   touch demo/3
   git add .
   git commit -m "fix: do not run pre-commit" --no-verify
   ```

## CI et Scale

Avec notre nouveau modèle de `pre-commit hooks` nous sommes en mesure d'outiller les développeurs pour réduire le volume de bug en attrappant ceux-ci à la source même.  Il faut se rappeler que l'utilisation de `pre-commit` est vraiment un choix et non obligatoire.

![Distribution](./assets/distribution.png)

L'objectif à atteindre c'est la qualité du code et non d'exécuter des `pre-commit hooks`.  Pour certains les manoeuvres sont une deuxième nature, pour d'autre la raison pourquoi on demande cette qualité n'est pas pertinente...  Et il y a tout le monde entre les deux.

Comment on peut s'assurer que la qualité est atteinte ? On réplique les actions des `pre-commit hooks` dans le CI pipeline et on documente:

- `PULL_REQUEST_TEMPLATE.md`
- `CONTRIBUTING.md`
- GH Action

Maintenant si un dev oublie ou décide de ne pas exécuter le framework de `pre-commit` localement sur sa machine avant de pousser son code.  Le CI pipeline échoue et lorsqu'on fait notre **code review**, la première question devrait être... Pourquoi as-tu skip tes `pre-commit`.  Il peut avoir d'excellente raison:

- Une situation **break the glass**
- Contester certaines configuration relative aux `pre-commit`
- Et plusieurs autres... Mais une discussion s'ouvre...

Finalement, le `pre-commit` en mode CI devrait se faire de manière réfléchie.  Possiblement que certaines tâches ont avantages a être exécuter via des **actions** et scripts plus complexes et complete.

## Considération

Il y a plusieurs considérations lors de la mise en place d'une pratique de `pre-commit` dans une organisation

- Séurité
  - Êtes-vous prêt à exécuter des scripts arbitraire sur vos code sources ?
  - Traiter les `pre-commits hooks` comme les dépendences logicielles (proxy, hosting interne, audit pré-adoption, etc...)
- Performance
  - Êtes-vous prêt à **perdre** 5-10sec à chaque `git commit` ?
  - Réduire l'emprunte des hooks au minimum (sécurité, formattage), utiliser les `stage: manual` ou un framework plus performant (`prek`).
- Irritation
  - Êtes-vous prêt à irriter les devs à chaque `git commit` ?
  - Commencer à petits pas, l'embarquement de cette méthodologie prendra un peu de temps et surtout la rendre facultative.

## Q&A

---

## Reference

[^1]: This is the first footnote.
