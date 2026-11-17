# API — version 0.1

Service local : `http://127.0.0.1:5000`. Aucun mécanisme d'authentification ; ne pas publier.

| Méthode | Route | Résultat |
|---|---|---|
| GET | `/` | Dashboard HTML |
| GET | `/health` | JSON `status`, `version` |
| POST | `/scan` | Rapport de métadonnées |

## Exemple PowerShell

```powershell
$body = @{path = (Resolve-Path ./demo).Path} | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:5000/scan -Method Post -ContentType application/json -Body $body
```

Entrée : objet JSON avec `path`, chaîne absolue d'un dossier existant autorisé.
La liste blanche vient du serveur, jamais du navigateur.

```json
{"folder":"/example/demo","total_files":1,"total_size_bytes":3,
 "categories":{"document":{"count":1,"size_bytes":3}},
 "files":[{"path":"notes.txt","name":"notes.txt","extension":".txt","size_bytes":3,
 "category":"document","modified_at":"2026-11-16T12:00:00+00:00",
 "accessed_at":"2026-11-16T12:00:00+00:00"}],"warnings":[],"truncated":false}
```

200 : analyse terminée, éventuellement partielle (consulter `warnings` et `truncated`).
400 : corps ou chemin invalide/inexistant. 403 : racine interdite, lien ou accès refusé.
413 : corps dépassant 16 Kio (réponse HTML Flask standard). 405 : mauvaise méthode.
`/prompt`, `/clean`, `/organize`, `/rename`, `/undo`, `/history`, `/settings` ne sont pas
encore implémentées et renvoient 404. Le cahier des charges ne constitue pas une API disponible.
