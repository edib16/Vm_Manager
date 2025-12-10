# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# --- ÉTAPE 1 : Installation des dépendances système (Compilation et Clients Libvirt) ---
# CORRECTION DÉFINITIVE : Utilisation de libvirt-clients (avec 's') pour le binaire 'virsh'.
RUN apt-get update && apt-get install -y \
    pkg-config \
    libvirt-dev \
    gcc \
    curl \
    gnupg2 \
    libxslt-dev \
    zlib1g-dev \
    build-essential \
    libvirt-clients \
    # Nettoyage pour réduire la taille de l'image
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# --- ÉTAPE 2 : Installation de VAGRANT (Méthode robuste) ---
# Utilisation de la lecture de /etc/os-release pour obtenir le CODENAME
RUN DEBIAN_CODENAME=$(grep VERSION_CODENAME /etc/os-release | cut -d= -f2 | tr -d '"') && \
    curl -fsSL https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com ${DEBIAN_CODENAME} main" | tee /etc/apt/sources.list.d/hashicorp.list && \
    apt-get update && \
    apt-get install -y vagrant && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# --- ÉTAPE 3 : Installation des Dépendances Python ---
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn

# --- ÉTAPE 4 : Installation du Plugin Vagrant Libvirt (Permissions/Environnement) ---
# Création de l'utilisateur pour l'alignement des permissions de VAGRANT_HOME
USER root
RUN adduser --disabled-password --gecos "" appuser
ENV VAGRANT_HOME=/data/vagrant.d
RUN mkdir -p ${VAGRANT_HOME} && chown -R appuser:appuser ${VAGRANT_HOME}
# Installation du plugin en tant qu'utilisateur final
USER appuser
RUN vagrant plugin install vagrant-libvirt

# --- Le reste du Dockerfile ---
COPY backend/ ./backend

ENV PYTHONPATH=/app/backend
ENV PYTHONUNBUFFERED=1

EXPOSE 5000
# Rappel : La configuration 'user: 1000:0' dans docker-compose.yml DOIT être maintenue
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "backend.main:app"]
