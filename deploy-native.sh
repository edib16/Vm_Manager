#!/bin/bash
# Script de déploiement VM_Manager en mode natif (sans Docker)
# À exécuter sur le serveur iris.a3n.fr

set -e

echo "🚀 Déploiement VM_Manager (mode natif)"
echo "======================================="

# Variables
APP_DIR="/home/iris/sisr/vm_manager"
VENV_DIR="$APP_DIR/.venv"
SERVICE_NAME="vm_manager.service"
LOG_DIR="/var/log/vm_manager"

# Vérifier qu'on est sur le serveur
if [[ ! -d "/home/iris" ]]; then
    echo "❌ Ce script doit être exécuté sur le serveur iris.a3n.fr"
    exit 1
fi

# Arrêter le service s'il existe
if systemctl is-active --quiet $SERVICE_NAME; then
    echo "⏸️  Arrêt du service existant..."
    sudo systemctl stop $SERVICE_NAME
fi

# Créer le répertoire de logs
echo "📁 Création du répertoire de logs..."
sudo mkdir -p $LOG_DIR
sudo chown iris:iris $LOG_DIR

# Mettre à jour le code depuis Git
echo "📥 Mise à jour du code..."
cd $APP_DIR
git pull origin main

# Créer le virtualenv s'il n'existe pas
if [[ ! -d "$VENV_DIR" ]]; then
    echo "🐍 Création du virtualenv..."
    python3 -m venv $VENV_DIR
fi

# Activer le virtualenv et installer les dépendances
echo "📦 Installation des dépendances Python..."
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
pip install gunicorn
deactivate

# Copier le fichier .env.example vers .env si nécessaire
if [[ ! -f "$APP_DIR/.env" ]]; then
    echo "⚙️  Création du fichier .env..."
    cp $APP_DIR/.env.example $APP_DIR/.env
    echo "⚠️  N'oubliez pas de modifier .env avec vos vraies valeurs !"
fi

# Installer le service systemd
echo "🔧 Installation du service systemd..."
sudo cp $APP_DIR/vm_manager.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME

# Démarrer le service
echo "▶️  Démarrage du service..."
sudo systemctl start $SERVICE_NAME

# Vérifier le statut
echo ""
echo "✅ Déploiement terminé !"
echo ""
echo "📊 Statut du service :"
sudo systemctl status $SERVICE_NAME --no-pager

echo ""
echo "📝 Commandes utiles :"
echo "  - Voir les logs       : sudo journalctl -u $SERVICE_NAME -f"
echo "  - Redémarrer          : sudo systemctl restart $SERVICE_NAME"
echo "  - Arrêter             : sudo systemctl stop $SERVICE_NAME"
echo "  - Voir le statut      : sudo systemctl status $SERVICE_NAME"
echo ""
echo "🌐 L'application est accessible via Traefik sur :"
echo "   https://vm-manager.iris.a3n.fr"
