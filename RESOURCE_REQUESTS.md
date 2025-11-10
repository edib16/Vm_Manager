# 📊 Fonctionnalité : Demande de ressources

## Vue d'ensemble

Les élèves peuvent demander une augmentation des ressources (RAM, CPU, stockage) pour leurs VMs via un formulaire dans l'interface web. Les demandes sont enregistrées dans une base de données SQLite et un email est envoyé automatiquement à l'administrateur.

## 🎯 Fonctionnalités

### Pour les élèves

1. **Bouton "📊 Demander ressources"** dans la liste des VMs
2. **Modal avec formulaire** contenant :
   - Nom de la VM (pré-rempli)
   - Ressources actuelles (affichage lecture seule)
   - RAM souhaitée (en GB)
   - CPU souhaités (nombre de vCPU)
   - Stockage souhaité (en GB)
   - Motif de la demande (minimum 10 caractères)
3. **Validation en temps réel** :
   - Les nouvelles valeurs doivent être >= aux valeurs actuelles
   - Le motif doit faire au moins 10 caractères
4. **Confirmation** après envoi réussi

### Pour l'administrateur

1. **Email automatique** à `edib.1605@gmail.com` avec :
   - Informations sur l'élève et la VM
   - Tableau comparatif (avant/après)
   - Motif détaillé de la demande
   
2. **Base de données SQLite** (`backend/resource_requests.db`) contenant :
   - Toutes les demandes (en attente, approuvées, refusées)
   - Horodatage de création et de traitement
   - Notes de l'admin (pour suivi)

## 📁 Fichiers créés/modifiés

### Nouveaux fichiers

- `backend/database.py` - Gestion de la base de données SQLite
- `backend/email_config.py` - Configuration SMTP et envoi d'emails
- `backend/resource_requests.db` - Base de données des demandes
- `EMAIL_CONFIG.md` - Guide de configuration des emails
- `RESOURCE_REQUESTS.md` - Ce fichier
- `test_resource_requests.py` - Script de test

### Fichiers modifiés

- `backend/main.py` - Ajout de 2 routes :
  - `POST /api/request_resources` - Soumettre une demande
  - `GET /api/get_vm_specs/<vm_name>` - Récupérer les specs d'une VM
  
- `frontend/index.html` - Ajout du modal de demande de ressources

- `frontend/static/app.js` (v15) - Ajout de la logique :
  - Ouverture du modal
  - Validation du formulaire
  - Soumission de la demande
  
- `frontend/static/styles.css` - Styles pour le modal et le bouton

## 🚀 Utilisation

### 1. Configuration (optionnelle)

Si vous voulez recevoir les emails, suivez le guide dans `EMAIL_CONFIG.md`.

**Sans configuration email :**
- Les demandes sont quand même enregistrées dans la base de données
- Aucun email n'est envoyé
- Vous pouvez consulter les demandes manuellement

### 2. Accès élève

1. Se connecter sur http://localhost:5000
2. Aller dans **"Mes VMs"**
3. Cliquer sur **"📊 Demander ressources"** pour une VM
4. Remplir le formulaire :
   - Augmenter RAM/CPU/Stockage selon le besoin
   - Expliquer pourquoi (motif obligatoire)
5. Cliquer sur **"📧 Envoyer la demande"**
6. Confirmation affichée

### 3. Consultation des demandes (admin)

#### Via SQLite (ligne de commande)

```bash
cd /home/edib/Vm_Manager/backend
sqlite3 resource_requests.db

# Voir toutes les demandes
SELECT * FROM resource_requests ORDER BY created_at DESC;

# Voir les demandes en attente
SELECT username, vm_name, reason, created_at 
FROM resource_requests 
WHERE status = 'pending' 
ORDER BY created_at DESC;

# Voir les demandes d'un utilisateur
SELECT * FROM resource_requests WHERE username = 'alice';
```

#### Via Python

```python
import sys
sys.path.insert(0, '/home/edib/Vm_Manager/backend')
import database

# Toutes les demandes en attente
pending = database.get_all_requests(status='pending')
for req in pending:
    print(f"{req['username']}: {req['vm_name']} - {req['reason']}")

# Demandes d'un utilisateur
user_reqs = database.get_user_requests('alice')
```

## 📊 Structure de la base de données

Table: `resource_requests`

| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER | ID unique (auto-incrémenté) |
| username | TEXT | Nom de l'utilisateur |
| vm_name | TEXT | Nom de la VM |
| current_ram_mb | INTEGER | RAM actuelle (MB) |
| current_cpu | INTEGER | CPU actuels |
| current_storage_gb | INTEGER | Stockage actuel (GB) |
| requested_ram_mb | INTEGER | RAM demandée (MB) |
| requested_cpu | INTEGER | CPU demandés |
| requested_storage_gb | INTEGER | Stockage demandé (GB) |
| reason | TEXT | Motif de la demande |
| status | TEXT | Statut: 'pending', 'approved', 'rejected' |
| created_at | TIMESTAMP | Date de création |
| processed_at | TIMESTAMP | Date de traitement (NULL si en attente) |
| admin_notes | TEXT | Notes de l'admin (NULL par défaut) |

## 📧 Format de l'email

```
Sujet: [VM Manager] Demande de ressources - <vm_name> (<username>)

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

## 🔐 Sécurité

- ✅ Authentification requise (`@login_required`)
- ✅ Vérification de propriété de la VM
- ✅ Validation des données (backend + frontend)
- ✅ Les nouvelles valeurs doivent être >= actuelles
- ⚠️ Le fichier `email_config.py` contient des identifiants → à ajouter au `.gitignore`

## 🎨 Personnalisation

### Changer l'email de destination

Éditez `backend/email_config.py` :

```python
ADMIN_EMAIL = "votre-email@example.com"
```

### Limiter les ressources maximales

Modifiez dans `frontend/index.html` :

```html
<input id="requestedRam" type="number" min="1" max="64" step="1">
<input id="requestedCpu" type="number" min="1" max="16" step="1">
<input id="requestedStorage" type="number" min="10" max="500" step="10">
```

### Ajouter un workflow d'approbation

Créez une interface admin pour approuver/refuser les demandes :

```python
# Exemple de fonction
database.update_request_status(
    request_id=1, 
    status='approved', 
    admin_notes='Augmentation autorisée'
)
```

## 🧪 Tests

```bash
# Test complet
cd /home/edib/Vm_Manager
python3 test_resource_requests.py

# Test manuel
cd backend
python main.py
# Puis via navigateur: http://localhost:5000
```

## 📝 TODO / Améliorations possibles

- [ ] Interface admin pour gérer les demandes (approuver/refuser)
- [ ] Notifications aux élèves quand leur demande est traitée
- [ ] Historique des demandes dans l'UI élève
- [ ] Appliquer automatiquement les changements après approbation
- [ ] Limites de quotas par utilisateur
- [ ] Dashboard admin avec statistiques

## ❓ FAQ

**Q: L'email ne part pas, que faire ?**
R: Lisez `EMAIL_CONFIG.md`. Sans configuration, les demandes sont quand même enregistrées en base.

**Q: Comment voir toutes les demandes ?**
R: `sqlite3 backend/resource_requests.db "SELECT * FROM resource_requests;"`

**Q: Un élève peut demander des ressources pour la VM d'un autre ?**
R: Non, vérification de propriété dans `check_vm_ownership()`.

**Q: Les demandes sont-elles appliquées automatiquement ?**
R: Non, c'est juste une demande. L'admin doit modifier le Vagrantfile manuellement.
