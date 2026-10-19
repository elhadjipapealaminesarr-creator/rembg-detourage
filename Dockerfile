# Image Docker du service de détourage rembg — pensée pour Render (offre gratuite : 512 Mo RAM).
# Écoute sur $PORT (fourni par Render) avec repli 7860. Modèle LÉGER u2netp (tient dans 512 Mo).
FROM python:3.11-slim

# Dépendances système requises par rembg / onnxruntime / opencv.
# libgomp1 = OpenMP, INDISPENSABLE à onnxruntime (sinon crash/segfault à l'inférence).
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 libgomp1 \
  && rm -rf /var/lib/apt/lists/*

# Utilisateur non-root (exigé par Hugging Face Spaces).
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    U2NET_HOME=/home/user/.u2net \
    REMBG_MODEL=u2netp \
    PORT=7860
WORKDIR /home/user/app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY --chown=user app.py .

# Pré-télécharge le modèle LÉGER DANS l'image → aucun délai de téléchargement au 1er appel.
RUN python -c "from rembg import new_session; new_session('u2netp')"

EXPOSE 7860
# Render fournit $PORT ; repli 7860 en local. Un seul worker (512 Mo).
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-7860} --workers 1"]
