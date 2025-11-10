# Configuration de l'envoi d'emails (Gmail)

Pour que le système puisse envoyer des emails de demande de ressources, vous devez configurer l'accès SMTP Gmail.

## 📋 Étapes de configuration

### 1. Activer l'authentification à 2 facteurs sur Gmail

1. Allez sur https://myaccount.google.com/security
2. Activez la **validation en deux étapes** si ce n'est pas déjà fait

### 2. Créer un mot de passe d'application

1. Allez sur https://myaccount.google.com/apppasswords
2. Connectez-vous si nécessaire
3. Dans "Sélectionnez l'application", choisissez **"Autre (nom personnalisé)"**
4. Entrez : `VM Manager`
5. Cliquez sur **Générer**
6. **Copiez le mot de passe de 16 caractères** (format: `xxxx xxxx xxxx xxxx`)

### 3. Configurer le fichier email_config.py

Éditez le fichier `/home/edib/Vm_Manager/backend/email_config.py` :

```python
# Configuration SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "votre-email@gmail.com"      # ← Remplacez par votre email
SMTP_PASSWORD = "xxxx xxxx xxxx xxxx"        # ← Collez le mot de passe d'application (SANS espaces)

# Destinataire des demandes
ADMIN_EMAIL = "edib.1605@gmail.com"  # ← Déjà configuré
```

**⚠️ Important :**
- Utilisez votre email Gmail personnel pour `SMTP_USERNAME`
- Utilisez le **mot de passe d'application** (PAS votre mot de passe Gmail normal)
- Retirez les espaces du mot de passe : `xxxx xxxx xxxx xxxx` → `xxxxxxxxxxxxxxxx`

### 4. Tester la configuration

```bash
cd /home/edib/Vm_Manager/backend
python3 -c "from email_config import test_email_config; test_email_config()"
```

Si tout fonctionne, vous verrez :
```
✅ Configuration SMTP valide
```

## 🔒 Sécurité

**⚠️ IMPORTANT :** Le fichier `email_config.py` contient des identifiants sensibles !

### Option 1 : Ajouter au .gitignore (RECOMMANDÉ)

```bash
echo "backend/email_config.py" >> /home/edib/Vm_Manager/.gitignore
```

### Option 2 : Utiliser des variables d'environnement

Créez un fichier `.env` :

```bash
# /home/edib/Vm_Manager/.env
SMTP_USERNAME=votre-email@gmail.com
SMTP_PASSWORD=xxxxxxxxxxxxxxxx
ADMIN_EMAIL=edib.1605@gmail.com
```

Puis modifiez `email_config.py` :

```python
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "edib.1605@gmail.com")
```

Et ajoutez `.env` au `.gitignore` :

```bash
echo ".env" >> /home/edib/Vm_Manager/.gitignore
```

## 📧 Format de l'email

Quand un élève fait une demande, tu recevras un email comme :

```
Sujet: [VM Manager] Demande de ressources - debian-client-01 (alice)

Nouvelle demande de ressources pour une VM

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INFORMATIONS GÉNÉRALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 Utilisateur : alice
🖥️  Machine virtuelle : debian-client-01

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESSOURCES ACTUELLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💾 RAM : 4096 MB (4.0 GB)
⚙️  CPU : 2 vCPU(s)
💿 Stockage : 20 GB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESSOURCES DEMANDÉES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💾 RAM : 8192 MB (8.0 GB)  [+4096 MB]
⚙️  CPU : 4 vCPU(s)  [+2 vCPU]
💿 Stockage : 50 GB  [+30 GB]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MOTIF DE LA DEMANDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

J'ai besoin de plus de ressources pour compiler mon projet 
et faire tourner plusieurs services en même temps.
```

## 🗃️ Base de données

Les demandes sont aussi enregistrées dans `/home/edib/Vm_Manager/backend/resource_requests.db` (SQLite).

Tu peux consulter la base :

```bash
cd /home/edib/Vm_Manager/backend
sqlite3 resource_requests.db "SELECT * FROM resource_requests ORDER BY created_at DESC LIMIT 10;"
```

## 🔧 Dépannage

### Erreur : "Authentication failed"
- Vérifiez que vous utilisez un **mot de passe d'application**, pas votre mot de passe Gmail
- Vérifiez que la validation en 2 étapes est activée

### Erreur : "SMTP connection failed"
- Vérifiez votre connexion internet
- Vérifiez que le port 587 n'est pas bloqué par un firewall

### L'email n'arrive pas
- Vérifiez les spams/courrier indésirable
- Vérifiez que `ADMIN_EMAIL` est correct dans `email_config.py`

## 🚀 Utilisation

Une fois configuré, les élèves peuvent :

1. Aller dans **"Mes VMs"**
2. Cliquer sur **"📊 Demander ressources"** pour une VM
3. Remplir le formulaire :
   - RAM souhaitée (GB)
   - CPU souhaités (vCPU)
   - Stockage souhaité (GB)
   - Motif de la demande
4. Cliquer sur **"📧 Envoyer la demande"**

Tu recevras alors un email à `edib.1605@gmail.com` avec tous les détails !
