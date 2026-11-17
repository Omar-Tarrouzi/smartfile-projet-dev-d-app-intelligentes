# SmartFiles

Assistant local de gestion de stockage — projet Déploiement Développement Web, 5IAD G1.

## État actuel : phase 1, fondations

Fonctionnels : application Flask, dashboard français responsive, analyse récursive en lecture seule,
statistiques par catégorie, inventaire, racines autorisées, exclusions et limite de fichiers.
Pas encore disponibles : LLM, doublons, EXIF, suppression, tri, renommage, historique et annulation.
La spécification décrit la cible complète ; ce README décrit ce qui est réellement livré.

## Démarrage Windows

Prérequis : Python 3.11+ et uv. Python 3.12 recommandé ; 3.14 est une cible de CI.
Depuis ce dossier dans PowerShell :

```powershell
uv sync --frozen
uv run python app.py
```

Ouvrir http://127.0.0.1:5000 puis cliquer sur **Analyser le dossier**.
Le chemin prérempli pointe vers `demo/`. Aucun compte ni clé API nécessaire.
Arrêter avec Ctrl+C. Pour un serveur local sans serveur de développement Flask :

```powershell
uv run waitress-serve --host=127.0.0.1 --port=5000 app:app
```

## Autoriser un autre dossier

Copier `.env.example` vers `.env`, puis renseigner une liste JSON de chemins absolus :

```dotenv
SMARTFILES_ALLOWED_ROOTS=["C:/Users/votre-nom/Downloads"]
SMARTFILES_MAX_FILES=10000
```

Redémarrer le serveur. Un chemin saisi dans l'interface ne devient jamais une autorisation.
Le navigateur analyse les dossiers de la machine où tourne Flask, pas ceux d'un visiteur distant.
Ne pas autoriser une racine disque ou un dossier système. Les fichiers cachés et dossiers techniques
sont exclus, les liens et jonctions sont refusés. Un résultat plafonné est signalé comme partiel.

## Vérifications

```powershell
uv run pytest -q
uv run ruff check .
```

Le rapport réel de validation se trouve dans `docs/VALIDATION.md`.

## Docker local

```powershell
docker compose up --build -d
docker compose down
```

Même URL ; saisir `/data` dans l'interface. Seul `demo/` est monté, en lecture seule.
Un autre montage doit être autorisé explicitement dans Compose. Ne pas exposer cette application
sur Internet : pas d'authentification et accès aux métadonnées locales.

## Architecture et guides

- `docs/ARCHITECTURE.md` : couches, flux, décisions et limites.
- `docs/API.md` : routes livrées et exemples PowerShell.
- `docs/DEVELOPMENT.md` : organisation et contributions.
- `docs/ROADMAP.md` : étapes restantes et critères d'acceptation.
- `docs/COMMITS.md` : lots et commandes de commits préparés.
- `SPECIFICATION.md` : cahier des charges original conservé.

Inspiration GameScope : séparation du métier et du web, environnement reproductible,
tests, démonstration Docker locale et documentation de validation. Flask et uv sont conservés
selon le cahier des charges ; Django, Streamlit, le dataset et le modèle GameScope ne sont pas repris.

## Aide-mémoire du cours

- [Fiche PDF (5 pages)](docs/AIDE_MEMOIRE_COURS.pdf) : syntaxes Streamlit, Gradio, Flask, JSON, API et commandes uv/Git/Docker.
- [Version Markdown modifiable](docs/AIDE_MEMOIRE_COURS.md) : mêmes exemples et références officielles.

Ces exemples de révision sont à lancer dans un dossier séparé ; Streamlit et Gradio ne sont pas des dépendances de SmartFiles. Le lot de commit documentation de `docs/COMMITS.md` inclut ces fichiers.
