# 🚀 Déploiement Natif VM_Manager (Sans Docker)

## Architecture

```
Internet → Traefik (HTTPS) → Flask/Gunicorn (localhost:5000) → Vagrant → libvirt → KVM
```

## Prérequis sur le serveur

- Ubuntu 22.04+ / Debian 12+
- Python 3.10+
- Vagrant avec plugin vagrant-libvirt
- libvirt / KVM configuré
- Traefik installé

## Installation sur le serveur iris.a3n.fr

### 1. Connexion SSH

```bash
ssh -i ~/.ssh/mediaschool edib@37.64.159.66 -p 2222
```

### 2. Cloner le projet

```bash
cd /home/iris/sisr
git clone https://github.com/Mediaschool-BTS-SISR-2025/edib_ansible.git vm_manager
cd vm_manager
```

### 3. Exécuter le script de déploiement

```bash
chmod +x deploy-native.sh
./deploy-native.sh
```

Le script va automatiquement :
- ✅ Créer le virtualenv Python
- ✅ Installer les dépendances
- ✅ Configurer le service systemd
- ✅ Démarrer l'application

### 4. Configurer Traefik

#### Option A : Configuration dynamique (recommandé)

```bash
# Copier la configuration Traefik
sudo cp traefik-config.yml /etc/traefik/dynamic/vm_manager.yml

# Recharger Traefik (ou attendre le rechargement automatique)
docker restart traefik  # Si Traefik est en Docker
# OU
sudo systemctl reload traefik  # Si Traefik est en systemd
```

#### Option B : Labels Docker (si Traefik surveille Docker)

Si impossible d'utiliser la config fichier, créer un conteneur "dummy" avec les labels :

```bash
docker run -d \
  --name vm_manager_traefik_bridge \
  --network admin_proxy \
  --label "traefik.enable=true" \
  --label "traefik.http.routers.vm-manager.rule=Host(\`vm-manager.iris.a3n.fr\`)" \
  --label "traefik.http.routers.vm-manager.entrypoints=websecure" \
  --label "traefik.http.routers.vm-manager.tls.certresolver=letsencrypt" \
  --label "traefik.http.services.vm-manager.loadbalancer.server.url=http://host.docker.internal:5000" \
  alpine sleep infinity
```

### 5. Configurer l'environnement

```bash
cd /home/iris/sisr/vm_manager

# Éditer le fichier .env avec vos vraies valeurs
nano .env

# Générer une SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 6. Vérifier le fonctionnement

```bash
# Statut du service
sudo systemctl status vm_manager.service

# Logs en temps réel
sudo journalctl -u vm_manager.service -f

# Test local
curl http://localhost:5000/api/vms

# Test depuis l'extérieur
curl https://vm-manager.iris.a3n.fr
```

## Gestion du service

### Commandes systemd

```bash
# Démarrer
sudo systemctl start vm_manager.service

# Arrêter
sudo systemctl stop vm_manager.service

# Redémarrer
sudo systemctl restart vm_manager.service

# Recharger (sans coupure)
sudo systemctl reload vm_manager.service

# Voir le statut
sudo systemctl status vm_manager.service

# Activer au démarrage
sudo systemctl enable vm_manager.service

# Désactiver au démarrage
sudo systemctl disable vm_manager.service
```

### Logs

```bash
# Logs systemd (temps réel)
sudo journalctl -u vm_manager.service -f

# Logs systemd (dernières 100 lignes)
sudo journalctl -u vm_manager.service -n 100

# Logs Gunicorn
tail -f /var/log/vm_manager/access.log
tail -f /var/log/vm_manager/error.log
```

## Mise à jour

```bash
cd /home/iris/sisr/vm_manager

# Récupérer les dernières modifications
git pull origin main

# Réinstaller les dépendances si nécessaire
source .venv/bin/activate
pip install -r backend/requirements.txt
deactivate

# Redémarrer le service
sudo systemctl restart vm_manager.service
```

## Dépannage

### Le service ne démarre pas

```bash
# Vérifier les logs détaillés
sudo journalctl -u vm_manager.service -n 200

# Vérifier que le port 5000 n'est pas utilisé
sudo ss -tlnp | grep :5000

# Tester manuellement
cd /home/iris/sisr/vm_manager/backend
source ../.venv/bin/activate
gunicorn --bind 127.0.0.1:5000 main:app
```

### Permission denied sur libvirt

```bash
# Ajouter l'utilisateur au groupe libvirt
sudo usermod -aG libvirt iris

# Redémarrer la session ou redémarrer le service
sudo systemctl restart vm_manager.service
```

### Vagrant ne fonctionne pas

```bash
# Vérifier l'installation
vagrant --version
vagrant plugin list

# Installer le plugin si manquant
vagrant plugin install vagrant-libvirt

# Vérifier libvirt
virsh -c qemu:///system list --all
```

## Comparaison Docker vs Natif

| Aspect | Docker | Natif |
|--------|--------|-------|
| Installation | `docker-compose up` | Script + systemd |
| Performance | Overhead conteneur | Performance maximale |
| Virtualisation | Imbriquée (complexe) | Directe (simple) |
| Maintenance | Rebuild image | `git pull` + restart |
| Logs | `docker logs` | `journalctl` |
| Débogage | Plus complexe | Direct |
| Ressources | Plus gourmand | Optimal |

## Sécurité

### Firewall

```bash
# Flask écoute uniquement sur localhost (127.0.0.1:5000)
# Pas besoin d'ouvrir le port dans le firewall
# Traefik gère l'exposition publique
```

### Utilisateur non-root

Le service s'exécute sous l'utilisateur `iris` (non-root) pour limiter les privilèges.

### Variables d'environnement

Toujours stocker les secrets dans `.env` (jamais commiter ce fichier).

## Architecture réseau

```
┌─────────────────────────────────────────────┐
│ Internet                                    │
└──────────────────┬──────────────────────────┘
                   │ HTTPS (443)
                   ▼
┌─────────────────────────────────────────────┐
│ Traefik (Reverse Proxy)                     │
│ - SSL/TLS termination                       │
│ - Routing par domaine                       │
└──────────────────┬──────────────────────────┘
                   │ HTTP (5000)
                   │ localhost only
                   ▼
┌─────────────────────────────────────────────┐
│ Gunicorn + Flask (Backend)                  │
│ User: iris                                  │
│ Bind: 127.0.0.1:5000                        │
└──────────────────┬──────────────────────────┘
                   │ API calls
                   ▼
┌─────────────────────────────────────────────┐
│ Vagrant + libvirt                           │
│ - Création VMs                              │
│ - Gestion cycle de vie                      │
└──────────────────┬──────────────────────────┘
                   │ qemu:///system
                   ▼
┌─────────────────────────────────────────────┐
│ KVM/QEMU (Hyperviseur)                      │
│ - VMs étudiantes                            │
│ - Réseau NAT (virbr0)                       │
└─────────────────────────────────────────────┘
```

## Support

Pour toute question, consulter les logs ou ouvrir une issue sur GitHub.
