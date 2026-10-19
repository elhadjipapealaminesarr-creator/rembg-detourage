# Service de détourage GRATUIT & ILLIMITÉ (rembg) — API HTTP simple pour l'app Électroménager Dakar.
# Déployé en Space Docker Hugging Face (CPU basic, 16 Go RAM, gratuit). L'app WooCommerce appelle
# POST /remove (image en multipart "file") et récupère un PNG détouré (fond transparent).
#
# Sécurité : si la variable REMBG_TOKEN est définie (côté Space ET côté app), chaque requête doit
# présenter l'en-tête X-Token correspondant → empêche que n'importe qui utilise ton service.
import os
import io
from fastapi import FastAPI, File, UploadFile, Header, HTTPException
from fastapi.responses import Response, JSONResponse
from rembg import remove, new_session

# Modèle de détourage. Par défaut "u2netp" (LÉGER : tient dans 512 Mo, offre gratuite Render).
# Si tu as plus de RAM : "u2net" (meilleur), "isnet-general-use" (très bon), "birefnet-general" (top).
MODEL = os.environ.get("REMBG_MODEL", "u2netp").strip()
TOKEN = os.environ.get("REMBG_TOKEN", "").strip()
# Alpha matting = bords plus fins (cheveux, fils) mais LENT sur CPU faible → désactivé par défaut.
# Mets REMBG_ALPHA=1 si ton hébergeur a un bon CPU.
ALPHA = os.environ.get("REMBG_ALPHA", "0").strip() == "1"

# Session chargée une seule fois au démarrage (le modèle est déjà pré-téléchargé dans l'image Docker).
_session = new_session(MODEL)

app = FastAPI(title="Rembg Détourage", version="1.0")


def _verifier(token: str):
    if TOKEN and token != TOKEN:
        raise HTTPException(status_code=401, detail="Jeton invalide.")


@app.get("/")
def sante():
    # Point de santé : l'app et toi pouvez vérifier que le service répond.
    return {"ok": True, "service": "rembg", "model": MODEL, "auth": bool(TOKEN)}


@app.post("/remove")
async def detourer(file: UploadFile = File(...), x_token: str = Header(default="")):
    _verifier(x_token)
    data = await file.read()
    if not data or len(data) < 100:
        return JSONResponse(status_code=400, content={"ok": False, "erreur": "Image vide."})
    try:
        if ALPHA:
            sortie = remove(data, session=_session, alpha_matting=True,
                            alpha_matting_foreground_threshold=240,
                            alpha_matting_background_threshold=15,
                            alpha_matting_erode_size=8)
        else:
            sortie = remove(data, session=_session)
        return Response(content=sortie, media_type="image/png")
    except Exception as e:
        return JSONResponse(status_code=500, content={"ok": False, "erreur": str(e)})
