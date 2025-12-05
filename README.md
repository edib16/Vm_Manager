# VM_Manager 🖥️

**Gestionnaire de machines virtuelles étudiantes** - Interface web pour la création et la gestion de VMs via Vagrant/libvirt avec accès console VNC intégré.

[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
  - [Développement Local](#développement-local)
  - [Production (Serveur)](#production-serveur)
- [Utilisation](#-utilisation)
- [Configuration](#-configuration)
- [Structure du Projet](#-structure-du-projet)
- [Technologies](#-technologies)

---

## ✨ Fonctionnalités

- ✅ **Création de VMs asynchrone** : Debian 12 (client/serveur) et Windows Server 2022
  - Interface réactive : retour immédiat pendant la création
  - Actualisation automatique toutes les 5 secondes
  - Suivi des logs en temps réel via journalctl
- ✅ **Gestion complète** : Démarrer, arrêter, supprimer les VMs
- ✅ **Console VNC intégrée** : Accès graphique direct via noVNC dans le navigateur
- ✅ **Isolation multi-utilisateurs** : Chaque étudiant gère uniquement ses VMs
- ✅ **Interface moderne** : Design responsive avec animations
- ✅ **Configuration automatisée** : Clavier français, locale FR, utilisateurs préconfigurés

---

## 🏗️ Architecture

### Architecture de Déploiement (Production - Mode Natif)

```
Internet
   │
   ▼
┌────────────────────────────────────────┐
│   Traefik (Reverse Proxy)              │
│   vm-manager.iris.a3n.fr               │
│   ✅ SSL/TLS automatique (Let's Encrypt)│
└──────────────┬─────────────────────────┘
               │ HTTP (localhost:5000)
               ▼
┌────────────────────────────────────────┐
│   Flask + Gunicorn (Natif)             │
│   • systemd service                    │
│   • Python virtualenv                  │
│   • User: iris (non-root)              │
│   • Bind: 127.0.0.1:5000               │
└──────────────┬─────────────────────────┘
               │ Appels système
               ▼
┌────────────────────────────────────────┐
│   Vagrant + Plugin libvirt             │
│   • Orchestration VMs                  │
│   • Génération Vagrantfile             │
└──────────────┬─────────────────────────┘
               │ qemu:///system
               ▼
┌────────────────────────────────────────┐
│   Libvirt (API virtualisation)         │
│   • Gestion domaines (VMs)             │
│   • Réseau NAT (virbr0)                │
│   • Ports VNC                          │
└──────────────┬─────────────────────────┘
               │ Hyperviseur
               ▼
┌────────────────────────────────────────┐
│   KVM/QEMU (Accès direct matériel)    │
│   ⚡ Performance maximale                │
│   ❌ Pas de virtualisation imbriquée    │
│                                        │
│   ┌────────┐ ┌────────┐ ┌────────┐   │
│   │ VM 1   │ │ VM 2   │ │ VM 3   │   │
│   │ Debian │ │Windows │ │ Debian │   │
│   └────────┘ └────────┘ └────────┘   │
└────────────────────────────────────────┘
```

**Avantages Mode Natif** :
- ⚡ **Performance maximale** : Pas d'overhead Docker
- ✅ **Architecture simplifiée** : Pas de virtualisation imbriquée
- 🔧 **Maintenance facile** : `git pull` + `systemctl restart`
- 📊 **Logs unifiés** : `journalctl` intégré
- 🔒 **Sécurité** : Service sous utilisateur non-root

### Architecture de Développement (Local)

```
localhost:8080
      │
      ▼
┌─────────────┐
│   nginx     │  Reverse Proxy
│  (frontend) │  + Fichiers statiques
└─────┬───────┘
      │ /api/* → proxy_pass
      ▼
┌─────────────┐
│   Backend   │
│ Flask:5000  │
│  (interne)  │
└─────────────┘
```

---

## 🔧 Prérequis

### Serveur (Production)
- Ubuntu 22.04+ / Debian 12+
- Docker + Docker Compose
- Traefik (déjà configuré)
- KVM/QEMU + libvirt
- Vagrant avec plugin libvirt

### Local (Développement)
- Docker + Docker Compose
- KVM/QEMU + libvirt
- Vagrant avec plugin libvirt
- Git

---

## 🚀 Installation

### Développement Local (Docker)

> ⚠️ **Note** : Le mode Docker est **uniquement pour le développement local**. En production, utilisez le déploiement natif.

#### 1. Cloner le projet

```bash
git clone https://github.com/Mediaschool-BTS-SISR-2025/edib_ansible.git
cd edib_ansible/Vm_Manager
```

#### 2. Configurer l'environnement

```bash
# Copier le fichier d'environnement
cp .env.example .env

# Éditer les variables si nécessaire
nano .env
```

#### 3. Démarrer les conteneurs

```bash
docker-compose up -d --build
```

#### 4. Accéder à l'application

Ouvrir dans le navigateur : **http://localhost:8080**

**Identifiants de test** :
- Utilisateur : `alice` / Mot de passe : `test`
- Admin : `admin` / Mot de passe : `test`

#### 5. Arrêter les conteneurs

```bash
docker-compose down
```

---

### Production (Serveur) - Mode Natif ⚡

> ✅ **Recommandé** : Déploiement natif pour performance maximale et architecture simplifiée.

#### 1. Se connecter au serveur

```bash
ssh -i ~/.ssh/mediaschool edib@37.64.159.66 -p 2222
```

#### 2. Cloner ou mettre à jour le projet

```bash
# Première installation
cd ~
git clone https://github.com/Mediaschool-BTS-SISR-2025/edib_ansible.git Vm_Manager
cd Vm_Manager

# OU mise à jour
cd ~/Vm_Manager
git pull origin main
```

#### 3. Exécuter le script de déploiement

```bash
chmod +x deploy-native.sh
./deploy-native.sh
```

Le script va automatiquement :
- ✅ Créer le virtualenv Python
- ✅ Installer les dépendances (Flask, Gunicorn, libvirt-python, etc.)
- ✅ Configurer le service systemd
- ✅ Démarrer l'application

#### 4. Installer noVNC

```bash
# Sur Debian/Ubuntu
sudo apt install novnc

# Sur Arch Linux
sudo git clone https://github.com/novnc/noVNC /usr/share/novnc
```

#### 5. Configurer Traefik

```bash
# Copier la configuration Traefik
sudo cp traefik-config.yml /etc/traefik/dynamic/vm_manager.yml

# Recharger Traefik (si nécessaire)
docker restart traefik  # Si Traefik est en Docker
```

#### 6. Configurer l'environnement

```bash
# Éditer le fichier .env avec vos vraies valeurs
nano .env

# Générer une SECRET_KEY sécurisée
python3 -c "import secrets; print(secrets.token_hex(32))"
```

#### 7. Configurer les permissions sudo (requis)

```bash
# Ajouter l'utilisateur au groupe libvirt
sudo usermod -aG libvirt iris

# Permettre à libvirt d'utiliser sudo sans mot de passe pour Vagrant
echo '%libvirt ALL=(root) NOPASSWD: /usr/bin/virsh, /usr/bin/qemu-system-x86_64' | sudo tee /etc/sudoers.d/vagrant-libvirt
sudo chmod 440 /etc/sudoers.d/vagrant-libvirt

# Démarrer le réseau libvirt par défaut
sudo virsh net-start default
sudo virsh net-autostart default
```

#### 8. Vérifier le déploiement

```bash
# Statut du service
sudo systemctl status vm_manager.service

# Logs en temps réel
sudo journalctl -u vm_manager.service -f

# Test local
curl http://localhost:5000/api/vms
```

#### 9. Accéder à l'application

**URL** : https://vm-manager.iris.a3n.fr

---

### 📋 Documentation Complète

Pour plus de détails sur le déploiement natif, consultez [DEPLOYMENT_NATIVE.md](DEPLOYMENT_NATIVE.md)

---

## 📖 Utilisation

### Créer une VM

1. Se connecter avec ses identifiants
2. Cliquer sur **"Créer une nouvelle VM"**
3. Remplir le formulaire :
   - **Nom** : Nom unique de la VM
   - **Type** : Client (GUI) ou Serveur (CLI)
   - **OS** : Debian 12 ou Windows Server 2022
   - **Utilisateur/Mot de passe** : Identifiants de la VM
   - **Mot de passe root** : (Debian uniquement)
4. Cliquer sur **"Créer"**

⏱️ La création prend 5-15 minutes selon le type de VM.

### Gérer une VM

- **▶️ Démarrer** : Lance la VM
- **⏸️ Arrêter** : Arrête proprement la VM
- **🖥️ Console VNC** : Ouvre la console graphique dans le navigateur
- **🗑️ Supprimer** : Supprime définitivement la VM

### Console VNC

La console VNC s'ouvre dans un nouvel onglet avec :
- Redimensionnement automatique
- Clavier AZERTY configuré
- Presse-papier partagé
- Mode plein écran disponible

---

## ⚙️ Configuration

### Variables d'environnement (.env)

```bash
# Clé secrète Flask (générer avec: python -c "import secrets; print(secrets.token_hex(32))")
SECRET_KEY=votre_clé_secrète_ici

# Configuration LDAP (pour authentification production)
LDAP_HOST=ldap://localhost:389
LDAP_BASE_DN=dc=example,dc=com
LDAP_USER_DN=ou=users,dc=example,dc=com
LDAP_GROUP_DN=ou=groups,dc=example,dc=com

# Email (pour demandes d'augmentation de capacité)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=noreply@example.com
SMTP_PASSWORD=votre_mot_de_passe
SMTP_FROM=VM Manager <noreply@example.com>
ADMIN_EMAILS=admin@example.com
```

### Utilisateurs de test (backend/test_auth.py)

En mode développement, les utilisateurs suivants sont disponibles :

```python
TEST_USERS = {
    "alice": "test",    # Utilisateur standard
    "bob": "test",      # Utilisateur standard
    "admin": "test"     # Administrateur
}
```

---

## 📁 Structure du Projet

```
Vm_Manager/
├── backend/                      # Backend Flask
│   ├── main.py                   # Application principale (API REST)
│   ├── config.py                 # Configuration LDAP/Email
│   ├── test_auth.py              # Authentification de test
│   ├── requirements.txt          # Dépendances Python
│   └── Dockerfile                # Image Docker backend
│
├── frontend/                     # Frontend statique
│   ├── index.html                # Page principale SPA
│   ├── nginx.conf                # Configuration nginx (dev)
│   ├── Dockerfile                # Image Docker nginx (dev)
│   └── static/
│       ├── app.js                # Logique JavaScript
│       └── styles.css            # Styles CSS
│
├── noVNC/                        # Client noVNC (console VNC web)
│
├── docker-compose.yml            # Docker Compose (développement local)
├── docker-compose.traefik.yml    # Docker Compose (production avec Traefik)
├── .env                          # Variables d'environnement
├── .gitignore                    # Fichiers ignorés par Git
└── README.md                     # Ce fichier
```

---

## 🛠️ Technologies

### Backend
- **Python 3.11** - Langage de programmation
- **Flask** - Framework web
- **Gunicorn** - Serveur WSGI production
- **libvirt-python** - Interaction avec libvirt
- **flask-login** - Gestion des sessions
- **flask-ldap3-login** - Authentification LDAP

### Frontend
- **HTML5/CSS3/JavaScript** - Technologies web standard
- **noVNC** - Console VNC dans le navigateur

### Infrastructure
- **Docker** - Conteneurisation
- **Docker Compose** - Orchestration multi-conteneurs
- **nginx** - Serveur web / Reverse proxy (dev)
- **Traefik** - Reverse proxy / Load balancer (prod)

### Virtualisation
- **KVM/QEMU** - Hyperviseur type 1
- **libvirt** - API de gestion de VMs
- **Vagrant** - Automatisation de la création de VMs
- **vagrant-libvirt** - Plugin Vagrant pour libvirt

---

## 📝 Commandes Utiles

### Docker Compose (Développement)

```bash
# Démarrer
docker-compose up -d --build

# Arrêter
docker-compose down

# Logs
docker-compose logs -f

# Rebuild sans cache
docker-compose build --no-cache
docker-compose up -d
```

### Docker Compose (Production)

```bash
# Démarrer
docker-compose -f docker-compose.traefik.yml up -d --build

# Arrêter
docker-compose -f docker-compose.traefik.yml down

# Logs
docker-compose -f docker-compose.traefik.yml logs -f backend

# Redéployer après modification
git pull origin main
docker-compose -f docker-compose.traefik.yml up -d --build
```

### Vagrant (Debug)

```bash
# Lister les VMs Vagrant
vagrant global-status

# Supprimer une VM orpheline
vagrant destroy <vm_id> -f

# Nettoyer les entrées invalides
vagrant global-status --prune
```

### Libvirt (Debug)

```bash
# Lister les VMs
virsh -c qemu:///system list --all

# État d'une VM
virsh -c qemu:///system domstate <vm_name>_default

# Arrêter une VM
virsh -c qemu:///system destroy <vm_name>_default

# Supprimer une VM
virsh -c qemu:///system undefine <vm_name>_default --remove-all-storage
```

---

## 🐛 Dépannage

### La VM ne démarre pas

1. Vérifier que KVM est activé : `lsmod | grep kvm`
2. Vérifier que libvirt est actif : `systemctl status libvirtd`
3. Vérifier le réseau libvirt : `virsh net-list --all`

### Erreur "Permission denied" Docker

```bash
# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER

# Redémarrer la session
newgrp docker
```

### Le backend ne communique pas avec libvirt

Vérifier que le conteneur backend a accès au socket libvirt :

```bash
docker exec vm_manager_backend virsh -c qemu:///system list
```

---

## 👨‍💻 Auteur

**Edib** - Projet réalisé dans le cadre du BTS SISR 2025

**Établissement** : Mediaschool

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 🔗 Liens Utiles

- [Documentation Flask](https://flask.palletsprojects.com/)
- [Documentation Vagrant](https://www.vagrantup.com/docs)
- [Documentation libvirt](https://libvirt.org/docs.html)
- [Documentation noVNC](https://github.com/novnc/noVNC)
- [Documentation Traefik](https://doc.traefik.io/traefik/)

```bash
docker ps --filter name=vm_manager
```

### Configuration Traefik

Les labels Traefik dans `docker-compose.traefik.yml` configurent automatiquement le routage :

- **Application web** : HTTP sur `vm-manager.iris.a3n.fr`
- Traefik route vers le conteneur nginx (frontend)
- nginx proxifie les appels API (`/api/*`) vers Flask en interne
- Le backend n'est pas exposé publiquement (sécurité)

Les deux services sont connectés au réseau Docker `admin_proxy`.

## 🔧 Technologies utilisées

### Backend
- **Python 3.11** + **Flask** : Framework web
- **Gunicorn** : Serveur WSGI
- **Flask-Login** : Gestion de session
- **flask-ldap3-login** : Authentification LDAP (optionnel)
- **libvirt-python** : Interaction avec libvirt/virsh
- **websockify** : Proxy WebSocket pour noVNC

### Frontend
- **HTML/CSS/JavaScript Vanilla**
- **nginx** : Serveur web (conteneur Docker)
- **Formspree** : Formulaire de demande de ressources (service tiers)

### Infrastructure
- **Docker** : Containerisation
- **Docker Compose** : Orchestration
- **Traefik** : Reverse proxy + TLS automatique
- **Ansible** : Automatisation du déploiement (alternative documentée)

## 📋 Variables d'environnement

Le fichier `.env` à la racine contient :

```bash
DOMAIN_NAME=iris.a3n.fr
```

Variables optionnelles pour le backend (dans le conteneur) :
- `SECRET_KEY` : Clé secrète Flask
- `LDAP_HOST`, `LDAP_BASE_DN`, etc. : Configuration LDAP

## 🎓 Déploiement Ansible (Alternative documentée)

Le projet inclut une configuration Ansible complète pour un déploiement alternatif sans Docker.

### Commande de déploiement

```bash
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml -e non_root_deploy=true
```

### Ce que fait Ansible

1. Crée un environnement virtuel Python sur le serveur
2. Installe les dépendances backend
3. Génère des scripts de démarrage (`start_backend.sh`, `start_websockify.sh`)
4. Démarre les services en arrière-plan avec `nohup`

**Mode non-root** : Utilisé car les droits sudo sont limités (uniquement `apt`/`apt-get`).

### Fichiers Ansible

- `ansible/deploy.yml` : Playbook principal avec logique conditionnelle (root/non-root)
- `ansible/inventory.ini` : Configuration serveur cible
- `ansible/templates/` : Templates systemd pour le mode privilégié

## 🖥️ noVNC et websockify

Le dossier `noVNC/` contient les fichiers statiques de noVNC pour l'accès aux consoles VNC des VMs.

- Télécharger noVNC : https://github.com/novnc/noVNC
- Le backend démarre automatiquement `websockify` sur un port libre (6080-6180)

## 🎯 Ports utilisés

- **5000** : Backend Flask (dans le conteneur)
- **80** : Frontend nginx (dans le conteneur)
- **6080+** : websockify/noVNC (cherche port libre automatiquement)
- **5900+** : Ports VNC internes des VMs

## 🔐 Windows VMs (notes)

### Comptes créés
- `Administrator` (mot de passe root)
- Compte utilisateur personnalisé (défini à la création)
- `vagrant` (pour compatibilité)

### Exigences mot de passe
Minimum 8 caractères : 1 majuscule, 1 minuscule, 1 chiffre (ex: `Azerty123`)

### Configuration
- Clavier : AZERTY (français)
- Temps de provisioning : 5-10 minutes (premier boot)
- Arrêt : tentative graceful (`vagrant halt`) puis forcé (`virsh destroy`) si timeout

## 🛠️ Développement local

### Prérequis
- Python 3.11+
- Docker (pour tester les conteneurs)

### Installation des dépendances

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### Lancer en mode développement

```bash
export FLASK_APP=backend/main.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

### Construire les images Docker localement

```bash
docker build -t vm_manager_backend:local ./backend
docker build -t vm_manager_frontend:local ./frontend
```

## 📊 Monitoring et logs

### Logs des conteneurs

```bash
# Tous les services
docker-compose -f docker-compose.traefik.yml logs -f

# Backend uniquement
docker logs vm_manager_backend -f

# Frontend uniquement
docker logs vm_manager_frontend -f
```

### État des conteneurs

```bash
docker ps --filter name=vm_manager
docker stats vm_manager_backend vm_manager_frontend
```

## 🐛 Dépannage

### Les conteneurs ne démarrent pas

```bash
# Vérifier les logs
docker-compose -f docker-compose.traefik.yml logs

# Vérifier la configuration
docker-compose -f docker-compose.traefik.yml config

# Reconstruire les images
docker-compose -f docker-compose.traefik.yml build --no-cache
docker-compose -f docker-compose.traefik.yml up -d
```

### Le site n'est pas accessible

1. Vérifier que les conteneurs tournent :
   ```bash
   docker ps --filter name=vm_manager
   ```

2. Vérifier le réseau Traefik :
   ```bash
   docker network inspect admin_proxy
   ```

3. Vérifier les logs Traefik (si accès) :
   ```bash
   docker logs traefik
   ```

### noVNC ne fonctionne pas

1. Vérifier que `noVNC/` existe dans le projet
2. Vérifier que `websockify` est installé dans le backend
3. Vérifier les logs backend pour les erreurs de démarrage websockify

## 🔒 Sécurité

### Recommandations production

- ✅ Traefik gère automatiquement le TLS avec Let's Encrypt
- ✅ Backend exposé uniquement via reverse proxy
- ✅ Conteneurs isolés dans un réseau Docker dédié
- ⚠️ Protéger l'accès noVNC avec authentification
- ⚠️ Configurer les limites de ressources dans docker-compose
- ⚠️ Sauvegarder régulièrement les VMs et données

### Variables sensibles

- Ne jamais commit `.env` avec des secrets réels
- Utiliser Ansible Vault pour les secrets en production
- Rotate les clés API et tokens régulièrement

## 📚 Documentation supplémentaire

- **DEPLOYMENT_REVIEW.md** : Guide détaillé pour le professeur
- **ansible/deploy.yml** : Playbook commenté avec explications

## 🤝 Contribution

Projet réalisé dans le cadre du BTS SISR à Mediaschool.

### Auteur
- **edib** - Étudiant BTS SISR 2025

### Serveur
- Hébergé sur iris.a3n.fr
- Gestion : Mediaschool-BTS-SISR-2025

---

Pour toute question ou problème, consulter les logs ou contacter l'administrateur système.
