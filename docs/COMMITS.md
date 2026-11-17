# Commits préparés

Le dépôt local utilise `main` et le remote `origin` vers le dépôt GitHub fourni.
Aucun commit ni push n'est effectué par l'initialisation. Vérifier d'abord `git status`.
Ces lots permettent de relire chaque responsabilité ; exécuter depuis la racine du projet.

## 1 — socle et scanner

```powershell
git add .gitignore .gitattributes .env.example pyproject.toml uv.lock app.py smartfiles demo tests
git diff --cached --stat
git commit -m "feat: initialize Flask app with safe read-only folder analysis"
```

## 2 — déploiement et contrôles

```powershell
git add Dockerfile compose.yaml .dockerignore .github
git diff --cached --stat
git commit -m "ci: add cross-platform checks and local Docker setup"
```

## 3 — documentation

```powershell
git add README.md SPECIFICATION.md docs CHANGELOG.md
git diff --cached --stat
git commit -m "docs: explain architecture setup API and implementation roadmap"
```

Après validation des trois lots : `git log --oneline`, `git status`, puis
`git push -u origin main` si vous souhaitez les publier. Les workflows GitHub ne tourneront
qu'après publication ; ne pas présenter leur configuration comme des tests déjà exécutés.
