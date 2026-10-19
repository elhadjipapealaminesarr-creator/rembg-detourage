# Déploiement du service de détourage sur Render (gratuit, sans carte bancaire)

Objectif : héberger `rembg` gratuitement sur **Render**, puis le brancher à l'app via `REMBG_URL`.
~15 minutes, une seule fois. (Offre gratuite : 512 Mo RAM, mise en veille après 15 min d'inactivité,
1er appel après réveil ~50 s. Illimité en nombre d'images.)

---

## 1) Mettre les fichiers du service sur GitHub

Render déploie à partir d'un dépôt GitHub. Les 5 fichiers de ce dossier doivent être dans un dépôt :
`Dockerfile`, `app.py`, `requirements.txt`, `render.yaml`, `README.md`.

> Claude peut créer ce dépôt et y déverser les fichiers via ton navigateur (compte GitHub connecté).

## 2) Créer le service sur Render

1. Va sur https://render.com → **Get Started** → **Sign in with GitHub** (autorise Render à voir tes dépôts).
2. Tableau de bord → **New +** → **Blueprint** (Render lit `render.yaml`) — ou **Web Service** si tu préfères.
3. Sélectionne le dépôt `rembg-detourage`.
4. Vérifie : **Runtime = Docker**, **Plan = Free**. Clique **Apply / Create**.
5. Render construit l'image (quelques minutes : logs → **Live**).

## 3) (Recommandé) Protéger par un jeton

1. Invente un jeton (longue chaîne au hasard).
2. Service Render → **Environment** → **Add Environment Variable** :
   - `REMBG_TOKEN` = ton jeton → **Save** (le service redémarre).

## 4) Récupérer l'URL

En haut du service Render : une URL du type `https://rembg-detourage.onrender.com`.
Ouvre-la dans le navigateur : `.../` doit répondre
`{"ok": true, "service": "rembg", "model": "u2netp", ...}`.

## 5) Brancher l'app (Vercel)

**Vercel → projet gestion-fournisseurs-web → Settings → Environment Variables** :

| Name          | Value                                                   |
|---------------|---------------------------------------------------------|
| `REMBG_URL`   | l'URL Render (ex. `https://rembg-detourage.onrender.com`)|
| `REMBG_TOKEN` | le même jeton qu'au §3 (si défini)                      |

> Si `REMBG_URL` existait déjà, **remplace** sa valeur. Puis **Redeploy** Vercel.

## 6) Vérifier

App → **Traitement d'image** → **Diagnostic remove.bg** : le service rembg doit apparaître
« joignable ✅ », et un détourage ne doit **plus consommer** tes appels remove.bg.

---

### Notes
- **Mise en veille** : après 15 min sans requête, l'instance gratuite s'endort. Le 1er appel la réveille
  (~50 s, toléré par l'app), puis c'est rapide.
- **Vitesse** : le CPU gratuit est modeste → compte quelques secondes à ~30 s par image. Gratuit et illimité.
- **Qualité** : modèle léger `u2netp` par défaut (bon). Si un jour tu as plus de RAM, mets
  `REMBG_MODEL=u2net` ou `isnet-general-use`, et `REMBG_ALPHA=1` pour des bords plus fins.
