# Plan de réalisation

## Phase 1 — livrée

- [x] Structure Flask, uv, configuration et démo.
- [x] Scanner récursif, catégorisation, tailles, dates, limite et avertissements.
- [x] Dashboard, API, tests, CI et documentation d'architecture.
- [x] Fichiers Docker pour une démonstration locale.

## Phase 2 — intelligence

- [ ] Routeur Groq/Ollama, paramètres serveur et tests avec faux client.
- [ ] Consentement explicite avant transmission cloud de métadonnées.
- [ ] `/prompt` en streaming et interface de chat, gestion timeout et erreurs.
- [ ] SHA-256 des doublons (sur fichiers de même taille), EXIF optionnel.

Acceptation : démo testée avec chaque fournisseur ; indisponibilité gérée ; aucune opération disque
déclenchée par une réponse du modèle ; limites du contexte documentées.

## Phase 3 — opérations sécurisées

- [ ] Plans de nettoyage, tri et renommage prévisualisés sans modification.
- [ ] Confirmation liée au plan serveur, expiration et revalidation des sources.
- [ ] Corbeille privée, collisions refusées, exclusions système et extensions protégées.
- [ ] Journal durable, erreurs partielles explicites, restauration sans écrasement.

Acceptation : tests de traversée, liens, collisions, fichiers modifiés depuis le scan,
double confirmation, échec en milieu de lot et annulation. Aucun fichier réel utilisé en test.

## Phase 4 — finitions

- [ ] Historique, annulation depuis l'interface, paramètres, filtres et pagination.
- [ ] Limites temporelles et traitement asynchrone des grands dossiers.
- [ ] Accessibilité, tests navigateur, démonstration et rapport de soutenance.

Un hébergement public nécessitera une conception spécifique : authentification, isolation des
racines par utilisateur, CSRF pour les mutations, TLS, quotas et supervision. Ce n'est pas
une simple modification de l'adresse d'écoute du serveur local.
