## Lancer avec systemd (service)

Si vous préférez contrôler l'application avec `systemctl` (démarrer/arrêter automatiquement au boot), voici une unité `systemd` incluse : `backend/vm_manager.service`.
## Configuration DNS pour `VM_Manager.a3n.fr`

1. Dans le panneau DNS de votre fournisseur de domaine `a3n.fr`, créez un enregistrement `A` :
## noVNC et websockify

Ce projet attend un dossier `noVNC/` (fichiers statiques de noVNC) à la racine du repo si vous voulez que la console web soit servie depuis le même serveur.
## Exécution en production (recommendé)

1. Installer et configurer `gunicorn` (déjà dans `requirements.txt`).
## Installer les dépendances

Créez un environnement virtuel (recommandé) et installez les dépendances :
## Démarrage en développement

Depuis la racine du projet :
## Points d'attention et recommandations

Le code interagit avec `libvirt` / `virsh` / `vagrant` et nécessite que ces outils soient installés et configurés correctement sur le serveur.
## Dépannage rapide

Si la console noVNC ne s'ouvre pas : vérifier que `noVNC/` existe, que `websockify` est installé et qu'un port libre est disponible.
## Exemple minimal de commande `gunicorn` :

```bash
cd backend
gunicorn --bind 0.0.0.0:5000 main:app
```
## Exemple `nginx` (reverse proxy + TLS)

- Le serveur Nginx sert `VM_Manager.a3n.fr` et reverse-proxy vers `http://127.0.0.1:5000`.
## Guide de démarrage complet et dépannage

Voici des instructions pas-à-pas pour préparer, lancer et diagnostiquer l'application en production (systemd + gunicorn), ainsi que des commandes de secours.
## Remarques de sécurité / production

- Préfère un reverse-proxy (nginx) devant gunicorn pour TLS, compression, gestion des en-têtes et accès public.
## Lancer avec systemd (service)

Si vous préférez contrôler l'application avec `systemctl` (démarrer/arrêter automatiquement au boot), voici une unité `systemd` incluse : `backend/vm_manager.service`.
## Configuration DNS pour `VM_Manager.a3n.fr`

1. Dans le panneau DNS de votre fournisseur de domaine `a3n.fr`, créez un enregistrement `A` :
## noVNC et websockify

Ce projet attend un dossier `noVNC/` (fichiers statiques de noVNC) à la racine du repo si vous voulez que la console web soit servie depuis le même serveur.
## Exécution en production (recommendé)

1. Installer et configurer `gunicorn` (déjà dans `requirements.txt`).
## Installer les dépendances

Créez un environnement virtuel (recommandé) et installez les dépendances :
## Démarrage en développement

Depuis la racine du projet :
## Points d'attention et recommandations

Le code interagit avec `libvirt` / `virsh` / `vagrant` et nécessite que ces outils soient installés et configurés correctement sur le serveur.
## Dépannage rapide

Si la console noVNC ne s'ouvre pas : vérifier que `noVNC/` existe, que `websockify` est installé et qu'un port libre est disponible.
## Exemple minimal de commande `gunicorn` :

```bash
cd backend
gunicorn --bind 0.0.0.0:5000 main:app
```
## Exemple `nginx` (reverse proxy + TLS)

- Le serveur Nginx sert `VM_Manager.a3n.fr` et reverse-proxy vers `http://127.0.0.1:5000`.
## Guide de démarrage complet et dépannage

Voici des instructions pas-à-pas pour préparer, lancer et diagnostiquer l'application en production (systemd + gunicorn), ainsi que des commandes de secours.
## Remarques de sécurité / production

- Préfère un reverse-proxy (nginx) devant gunicorn pour TLS, compression, gestion des en-têtes et accès public.
# VM_Manager

VM_Manager est une interface web simple pour gérer des machines virtuelles (création via Vagrant/libvirt, gestion via libvirt/virsh et accès via noVNC).

## Technologies utilisées

- Backend: Python + Flask
  - `Flask` pour l'application web
  - `Flask-Login` pour la gestion de session
  - `flask-ldap3-login` (optionnel) pour authentification LDAP
  - `libvirt-python` pour interagir avec libvirt/virsh
  - `websockify` + `noVNC` pour la console web VNC
  - `python-dotenv` pour charger les variables d'environnement
- Frontend: HTML/CSS/Vanilla JavaScript
  - `frontend/index.html`, `frontend/static/styles.css`, `frontend/static/app.js`
- Formulaire de demande de ressources: Formspree (service tiers)

## Ports utilisés (par défaut)

- `5000` — Flask (VM Manager)
- `6080` — noVNC / websockify (par défaut recherche de ports libres depuis 6080)
- `5900+` — ports VNC internes configurés par libvirt (dépend de la VM)

> Remarque: le port public réel pour noVNC dépendra du port libre trouvé par `websockify`. Le serveur cherche un port libre entre `6080` et `6180`.

## Structure du dépôt

- `backend/` : code Flask
  - `main.py` : application principale
  - `config.py` : configuration (lit les variables d'environnement)
  - `requirements.txt` : dépendances Python (core)
- `frontend/` : fichiers statiques et template
  - `index.html`
  - `static/` : `app.js`, `styles.css`
- `student_vms/` : dossiers VM par utilisateur (créés automatiquement)

## Variables d'environnement importantes

Vous pouvez définir ces variables dans un fichier `.env` à la racine du projet ou les exporter dans l'environnement de l'OS.

- `SECRET_KEY` — clé secrète Flask (par défaut: `dev-secret-change-me`)
- `LDAP_HOST`, `LDAP_BASE_DN`, `LDAP_BIND_USER_DN`, `LDAP_BIND_USER_PASSWORD` — paramètres LDAP (optionnels)

## Installer les dépendances

Créez un environnement virtuel (recommandé) et installez les dépendances :

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements.txt
```

## Démarrage en développement

Depuis la racine du projet :

```bash
export FLASK_APP=backend/main.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

L'interface sera accessible sur `http://localhost:5000`.

## Exécution en production (recommendé)

1. Installer et configurer `gunicorn` (déjà dans `requirements.txt`).
2. Mettre en place un reverse-proxy `nginx` devant l'application Flask.

Exemple minimal de commande `gunicorn` :

```bash
cd backend
. ../.venv/bin/activate
gunicorn --bind 0.0.0.0:5000 main:app
```

### Exemple `nginx` (reverse proxy + TLS)

- Le serveur Nginx sert `VM_Manager.a3n.fr` et reverse-proxy vers `http://127.0.0.1:5000`.
- Pour TLS, utilisez Let's Encrypt (certbot) et configurez automatiquement les certificats.

Extrait de configuration Nginx (à adapter) :

```
server {
    listen 80;
    server_name VM_Manager.a3n.fr;
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name VM_Manager.a3n.fr;

    ssl_certificate /etc/letsencrypt/live/VM_Manager.a3n.fr/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/VM_Manager.a3n.fr/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Exemple: rediriger /vnc proxies si nécessaire
}
```

## Configuration DNS pour `VM_Manager.a3n.fr`

1. Dans le panneau DNS de votre fournisseur de domaine `a3n.fr`, créez un enregistrement `A` :
   - Nom/Host: `VM_Manager` (ou `VM_Manager.a3n.fr` selon l'UI)
   - Type: `A`
   - Valeur: l'adresse IP publique de votre serveur
2. Attendre la propagation DNS (quelques minutes à quelques heures).
3. Configurer Nginx et Let's Encrypt pour activer HTTPS.

## noVNC et websockify

Ce projet attend un dossier `noVNC/` (fichiers statiques de noVNC) à la racine du repo si vous voulez que la console web soit servie depuis le même serveur.

- Téléchargez noVNC depuis : https://github.com/novnc/noVNC
- Placez le dossier `noVNC` à la racine du dépôt (même niveau que `backend/` et `frontend/`).

Le serveur démarre `websockify` automatiquement pour chaque VM et cherche un port libre entre `6080` et `6180`.

Si `noVNC/` est absent, `websockify` démarrera quand même mais la page `vnc.html` ne sera pas servie depuis ce dépôt — vous devrez alors héberger noVNC ailleurs ou copier les fichiers nécessaires.

## Formspree (formulaire de demande de ressources)

La fonctionnalité de demande de ressources utilise Formspree (service tiers) pour envoyer des emails sans backend local.

- Allez sur https://formspree.io et créez un formulaire.
- Remplacez l'endpoint dans `frontend/index.html` :

```html
<form action="https://formspree.io/f/<VOTRE_FORM_ID>" method="POST" id="resourceForm">
```

- Confirmez votre adresse email via le lien envoyé par Formspree (première utilisation).

## Points d'attention et recommandations

- Le code interagit avec `libvirt` / `virsh` / `vagrant` et nécessite que ces outils soient installés et configurés correctement sur le serveur.
- L'application doit être exécutée avec un utilisateur ayant les droits d'accès à `libvirt` (souvent `root` ou membre du groupe `libvirt`).
- Sauvegardez les VMs et configurations avant tests importants.

## Windows VMs (notes de provisioning)

- **Comptes créés** : après provisioning les VMs Windows fournissent trois comptes : `Administrator` (mot de passe root), un compte utilisateur personnalisé (celui indiqué lors de la création) et `vagrant` (conservé pour compatibilité). Le compte personnalisé et `vagrant` partagent le même mot de passe administrateur utilisateur.
- **Exigences de mot de passe** : minimum 8 caractères, au moins 1 majuscule, 1 minuscule et 1 chiffre (ex. `Azerty123`).
- **Clavier / Langue** : le provisioning configure la VM en français (AZERTY) — un redémarrage automatique applique la configuration.
- **Arrêt (halt)** : les VM Windows peuvent résister à un arrêt gracieux ; le serveur tente d'abord un `vagrant halt` puis effectue un arrêt forcé (`virsh destroy`) si nécessaire (après timeout) pour garantir que l'action "Arrêter" fonctionne.
- **Durée de provisioning** : prévoir 5–10 minutes pour le premier provisioning (premier boot et OOBE).

## Dépannage rapide

- Si la console noVNC ne s'ouvre pas : vérifier que `noVNC/` existe, que `websockify` est installé et qu'un port libre est disponible.
- Si un import LDAP pose problème, vérifiez vos variables d'environnement LDAP dans `.env`.

---

Si vous voulez, je peux :

- Nettoyer davantage `requirements.txt` et créer un script d'installation automatique.
- Générer une configuration `systemd` pour lancer `gunicorn` au démarrage.
- Préparer un `nginx` config complet et commandes `certbot` pour automatiser le TLS.

Dites-moi quel(s) point(s) vous voulez que j'implémente ensuite (ex: `systemd` service, configuration nginx prête à coller, scripts d'installation).

## Lancer avec systemd (service)

Si vous préférez contrôler l'application avec `systemctl` (démarrer/arrêter automatiquement au boot), voici une unité `systemd` incluse : `backend/vm_manager.service`.

Ce que fait cette unité :
 - Travaille depuis `/home/iris/sisr` en tant qu'utilisateur `edib` (modifiez `User=`/`Group=` si nécessaire).
- Tente d'utiliser `gunicorn` à l'intérieur d'un virtualenv (`.venv`) si présent : commande par défaut utilisée :

  `gunicorn --workers 3 --bind 0.0.0.0:5000 backend.main:app`

- Si vous préférez exécuter directement `python3 backend/main.py`, vous pouvez éditer le fichier et décommenter la ligne de fallback `ExecStart`.

Installation et commandes utiles :

```bash
# Copier l'unité dans systemd et recharger
sudo cp backend/vm_manager.service /etc/systemd/system/
sudo systemctl daemon-reload

# Activer au démarrage et lancer maintenant
sudo systemctl enable --now vm_manager.service

# Vérifier le statut
sudo systemctl status vm_manager.service

# Arrêter / démarrer
sudo systemctl stop vm_manager.service
sudo systemctl start vm_manager.service

# Voir les logs en temps réel
sudo journalctl -u vm_manager.service -f
```

Remarques :
- Assurez-vous que `gunicorn` est installé (ex: `pip install gunicorn`) si vous utilisez la ligne `ExecStart` par défaut.
- Si vous utilisez un virtualenv, créez-le à la racine du projet (`python -m venv .venv`) et installez les dépendances (`pip install -r backend/requirements.txt`).
- Modifiez la directive `User=` dans le fichier d'unité si vous voulez exécuter le service sous un autre compte système.

## Guide de démarrage complet et dépannage

Voici des instructions pas-à-pas pour préparer, lancer et diagnostiquer l'application en production (systemd + gunicorn), ainsi que des commandes de secours.

1) Préparer l'environnement (virtualenv recommandé)

```bash
# depuis la racine du projet
python3 -m venv .venv
# activer (bash)
source .venv/bin/activate
pip install -r backend/requirements.txt
pip install gunicorn
deactivate
```

2) Vérifier le fichier d'unité systemd

- Le fichier fourni est `backend/vm_manager.service` et, pour fonctionner correctement avec les imports du projet, il lance gunicorn depuis le dossier `backend`.
- Principales directives à contrôler avant installation :
  - `User=` : l'utilisateur système qui exécutera le service (par défaut `edib`). Changez si nécessaire.
  - `WorkingDirectory=` : doit pointer vers `/home/iris/sisr/backend` (c'est important pour que `import config` fonctionne).
  - `ExecStart=` : par défaut la commande essaie d'activer `.venv` puis lance `gunicorn main:app` depuis `backend`.

3) Installer et démarrer le service (systemd)

```bash
sudo cp backend/vm_manager.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now vm_manager.service
sudo systemctl status vm_manager.service
# suivre les logs
sudo journalctl -u vm_manager.service -f
```

4) Tester l'accès local

```bash
# depuis la même machine
curl -v http://127.0.0.1:5000/
# ou vérifier l'écoute du port
ss -ltnp | grep ':5000' || true
```

5) Comment arrêter proprement et empêcher les relances automatiques

Si tu veux arrêter le service et empêcher systemd de le relancer automatiquement :

```bash
sudo systemctl stop vm_manager.service
sudo systemctl disable vm_manager.service
# si tu veux forcer l'arrêt immédiat des processus encore présents
sudo systemctl kill vm_manager.service
sudo pkill -f gunicorn || true
```

6) Si le statut reste `activating` ou `active` alors que l'app est inaccessible

- Vérifie les logs :

```bash
sudo journalctl -u vm_manager.service -n 200 --no-pager
```

- Causes fréquentes et résolutions :
  - `ModuleNotFoundError: No module named 'config'` → solution : lancer gunicorn depuis le dossier `backend` (le fichier d'unité le fait), ou corriger les imports dans `backend/main.py`.
  - Workers qui plantent en boucle → regarde l'exception dans `journalctl` et corrige la cause (dépendances manquantes, erreurs d'import, variables d'environnement non définies).
  - Pare-feu (ufw/iptables) bloque le port 5000 → autoriser le port : `sudo ufw allow 5000/tcp`.
  - Le service tourne mais écoute sur `127.0.0.1` et tu y accèdes à distance → utiliser l'IP publique ou configurer un reverse-proxy (nginx) pour exposer sur 80/443.

7) Commandes utiles de dépannage rapide

```bash
# statut détaillé
sudo systemctl status vm_manager.service
# logs récents
sudo journalctl -u vm_manager.service -n 200 --no-pager
# suivre les logs
sudo journalctl -u vm_manager.service -f
# vérifier le port
ss -ltnp | grep ':5000' || true
# processus gunicorn
ps aux | egrep 'gunicorn|backend/main.py' || true
# réinitialiser les erreurs systemd
sudo systemctl reset-failed vm_manager.service
```

8) Lancer manuellement (pour debug)

- Gunicorn (depuis `backend` si tu utilises les imports tels quels) :

```bash
source .venv/bin/activate
cd backend
gunicorn --workers 3 --bind 0.0.0.0:5000 main:app
```

- Développement rapide (flask run) :

```bash
export FLASK_APP=backend/main.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

9) Remarques de sécurité / production

- Préfère un reverse-proxy (nginx) devant gunicorn pour TLS, compression, gestion des en-têtes et accès public.
- Protéger les accès noVNC/websockify (utiliser `wss://` ou reverse-proxy TLS + authentification côté application).
- Exécuter le service sous un compte non-root et limiter les permissions.

Si tu veux, je peux automatiser la préparation (création du `.venv`, installation des dépendances) et vérifier que le service démarre correctement sur ta machine. Veux-tu que j'exécute ces étapes maintenant ?
