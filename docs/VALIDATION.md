# Validation — 2026-11-16

## Exécuté localement

- Windows, CPython 3.11.9, environnement `.venv` géré par uv.
- `uv sync --frozen` : réussi, 16 paquets vérifiés.
- Flask 3.1.3, pytest 9.2.0, Ruff 0.17.5, Waitress 3.0.2 ; versions complètes dans `uv.lock`.
- `pytest -q` : **11 passed, 1 skipped**.
- Le test de liens est sauté : création de liens symboliques non autorisée pour ce compte Windows.
- `ruff check .` : réussi ; sources mises en forme avec Ruff.
- Test HTTP réel avec Waitress sur loopback : `/health`, `/`, CSS et JavaScript répondent 200 ;
  `POST /scan` retourne les 3 fichiers de démonstration. Serveur arrêté après vérification.
- `docker compose config --quiet` : réussi.
- Remote `origin` configuré vers le dépôt GitHub fourni, dépôt distant sans références au contrôle initial.
- Environnements, caches et fichiers `.env` exclus de Git ; `.env.example` inclus.

## Limites de validation

- Docker Desktop Linux Engine indisponible : image non construite et conteneur non exécuté.
- Matrice GitHub Actions fournie mais non exécutée : aucun push effectué.
- Python 3.12/3.14 et Linux non exécutés localement ; ils sont prévus dans la matrice CI.
- Interface servie par HTTP et ressources vérifiées ; pas de test visuel automatisé dans un navigateur.
- Aucun fournisseur IA testé : intégration prévue en phase 2.
- Aucun commit créé ; fichiers laissés non indexés pour revue et commits selon `COMMITS.md`.
