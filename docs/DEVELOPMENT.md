# Développement

## Organisation

```text
app.py                    Entrée Flask / Waitress
smartfiles/__init__.py     Fabrique et configuration
smartfiles/routes.py       Adaptateurs HTTP
smartfiles/safety.py       Validation des chemins
smartfiles/scanner.py      Métier en lecture seule
smartfiles/templates/     Interface Jinja
smartfiles/static/        JavaScript et CSS locaux
tests/                    Tests isolés dans des dossiers temporaires
demo/                     Petits exemples fictifs
docs/                     Architecture, API, roadmap, validation, commits
.github/workflows/        Contrôles Windows et Linux
```

`uv sync --frozen` installe le lock existant. Après modification volontaire des dépendances,
exécuter `uv lock`, puis `uv sync` et valider le changement de `uv.lock` dans le même commit.
Éviter de mélanger pip et uv dans le même environnement. Les tests n'utilisent aucun dossier personnel.
Pour les liens Windows, le test est sauté si le compte ne dispose pas du droit nécessaire.

## Avant chaque commit

1. `uv run ruff check .` et `uv run pytest -q`.
2. `git diff --check` puis relire `git diff` et `git diff --cached`.
3. Vérifier qu'aucun `.env`, document personnel, log ou environnement n'est suivi.
4. Mettre à jour les docs si le comportement change. Voir `COMMITS.md` pour les lots initiaux.

## Relation avec GameScope

GameScope sert d'exemple pédagogique pour la distribution, les tests et l'explication du déploiement.
SmartFiles conserve son domaine propre et son framework Flask. Aucun fichier SQLite, artefact ML,
document Office temporaire ou configuration IDE de GameScope n'est importé.
