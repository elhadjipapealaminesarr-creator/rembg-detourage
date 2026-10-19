# Service de détourage rembg (gratuit & illimité)

Petit service HTTP qui enlève le fond d'une image produit (modèle `u2netp` par défaut).
Conçu pour être hébergé **gratuitement sur Render** (Docker), et appelé par l'application
« Électroménager Dakar ». Voir **DEPLOY.md** pour le déploiement pas à pas.

## Points d'accès

- `GET /` → état du service (`{ ok, service, model, auth }`).
- `POST /remove` → détoure une image.
  - Corps : `multipart/form-data`, champ **`file`** (l'image JPEG/PNG).
  - En-tête optionnel : **`X-Token`** (si `REMBG_TOKEN` est défini côté service).
  - Réponse : un **PNG** à fond transparent.

Exemple :

```bash
curl -s -F "file=@produit.jpg" -H "X-Token: MON_JETON" \
  https://rembg-detourage.onrender.com/remove -o detoure.png
```

## Variables d'environnement

- `REMBG_MODEL` (défaut `u2netp`, léger) — sinon `u2net`, `isnet-general-use`, `birefnet-general`.
- `REMBG_ALPHA` (défaut `0`) — `1` active l'alpha matting (bords plus fins, plus lent).
- `REMBG_TOKEN` (optionnel, recommandé) — jeton partagé exigé via l'en-tête `X-Token`.
- `PORT` — fourni automatiquement par Render.
