# 🎉 Fonctionnalité de demande de ressources - TERMINÉE !

## ✅ Ce qui a été ajouté

### 📦 Backend (Python/Flask)

1. **`backend/database.py`** (159 lignes)
   - Gestion SQLite pour stocker les demandes
   - Fonctions: `add_resource_request()`, `get_user_requests()`, `get_all_requests()`
   - Table auto-créée au démarrage

2. **`backend/email_config.py`** (105 lignes)
   - Configuration SMTP Gmail
   - Email formaté avec toutes les infos
   - Fonction de test: `test_email_config()`

3. **`backend/main.py`** (modifications)
   - Route `POST /api/request_resources` - Soumettre une demande
   - Route `GET /api/get_vm_specs/<vm_name>` - Récupérer specs actuelles
   - Import des modules database et email

4. **`backend/resource_requests.db`** (SQLite)
   - Base de données créée automatiquement
   - 1 table avec 13 colonnes
   - Stockage des demandes (pending/approved/rejected)

### 🎨 Frontend (HTML/CSS/JS)

1. **`frontend/index.html`** (v15)
   - Modal complet avec formulaire de demande
   - Champs: VM, RAM, CPU, Stockage, Motif
   - Affichage des specs actuelles

2. **`frontend/static/app.js`** (v15, +150 lignes)
   - Validation en temps réel du formulaire
   - Récupération des specs via API
   - Soumission et gestion des réponses
   - Bouton "📊 Demander ressources" ajouté aux VM cards

3. **`frontend/static/styles.css`** (+92 lignes)
   - Styles du modal (fond noir transparent)
   - Bouton orange pour la demande
   - Responsive design

### 📚 Documentation

1. **`EMAIL_CONFIG.md`** (guide complet)
   - Configuration Gmail étape par étape
   - Mots de passe d'application
   - Sécurité et variables d'environnement

2. **`QUICK_EMAIL_SETUP.md`** (guide rapide 5 min)
   - Version courte pour configuration express

3. **`RESOURCE_REQUESTS.md`** (documentation complète)
   - Architecture de la fonctionnalité
   - Utilisation côté élève et admin
   - Structure de la base de données
   - FAQ et dépannage

4. **`test_resource_requests.py`** (script de test)
   - Test automatisé de tous les composants
   - Insertion test dans la DB
   - Vérification de la config email

## 🎯 Comment ça marche ?

### Côté élève :

```
1. Connexion sur http://localhost:5000
2. Clic sur "Mes VMs"
3. Clic sur "📊 Demander ressources" pour une VM
4. Formulaire s'ouvre avec :
   - Specs actuelles (lecture seule)
   - Nouveaux besoins (RAM/CPU/Stockage)
   - Motif (minimum 10 caractères)
5. Clic sur "📧 Envoyer la demande"
6. ✅ Confirmation affichée
```

### Côté admin :

```
📧 Email reçu à edib.1605@gmail.com avec :
   - Qui demande (username)
   - Quelle VM
   - Ressources avant/après (avec différence)
   - Motif complet

💾 Base de données SQLite contient tout l'historique
```

## 🚀 Démo rapide

```bash
# 1. Tester la DB et l'email
cd /home/edib/Vm_Manager
python3 test_resource_requests.py

# 2. Lancer Flask
cd backend
python main.py

# 3. Ouvrir http://localhost:5000
#    - Login: alice / alice
#    - Aller dans "Mes VMs"
#    - Cliquer "📊 Demander ressources"
#    - Remplir et envoyer
```

## 📊 Exemple de demande

**Interface élève :**
```
┌─────────────────────────────────────────┐
│ 📊 Demander plus de ressources         │
├─────────────────────────────────────────┤
│                                         │
│ Machine virtuelle: debian-client-01     │
│                                         │
│ Ressources actuelles :                  │
│   💾 RAM : 4.0 GB                       │
│   ⚙️ CPU : 2 vCPU(s)                    │
│   💿 Stockage : 20 GB                   │
│                                         │
│ 💾 RAM souhaitée (GB): [8]             │
│ ⚙️ CPU souhaités (vCPU): [4]           │
│ 💿 Stockage souhaité (GB): [50]        │
│                                         │
│ 📝 Motif:                               │
│ ┌─────────────────────────────────────┐ │
│ │ J'ai besoin de compiler mon projet  │ │
│ │ React qui nécessite beaucoup de     │ │
│ │ ressources pendant le build.        │ │
│ └─────────────────────────────────────┘ │
│                                         │
│       [📧 Envoyer la demande]          │
└─────────────────────────────────────────┘
```

**Email reçu :**
```
De: TON-EMAIL@gmail.com
À: edib.1605@gmail.com
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

J'ai besoin de compiler mon projet React qui 
nécessite beaucoup de ressources pendant le build.
```

## 🗄️ Base de données

```bash
# Consulter les demandes
cd backend
sqlite3 resource_requests.db

# Voir toutes les demandes
SELECT username, vm_name, requested_ram_mb/1024 as ram_gb, 
       requested_cpu, requested_storage_gb, status, created_at
FROM resource_requests 
ORDER BY created_at DESC;

# Résultat:
alice|debian-client-01|8|4|50|pending|2025-11-10 15:30:22
```

## ⚙️ Configuration requise

### Obligatoire ✅
- Python 3.x
- Flask (déjà installé)
- SQLite (inclus avec Python)

### Optionnel 📧
- Compte Gmail avec validation 2 étapes
- Mot de passe d'application Gmail

**Sans configuration email :**
- ✅ Formulaire fonctionne
- ✅ Demandes enregistrées en DB
- ❌ Pas d'email envoyé

**Avec configuration email :**
- ✅ Formulaire fonctionne
- ✅ Demandes enregistrées en DB
- ✅ Email envoyé automatiquement

## 🔒 Sécurité

- ✅ Authentification requise (`@login_required`)
- ✅ Vérification propriété de la VM
- ✅ Validation backend ET frontend
- ✅ Les nouvelles valeurs >= actuelles (pas de diminution)
- ⚠️ Penser à ajouter `email_config.py` au `.gitignore`

## 📝 À faire (optionnel)

Améliorations possibles pour plus tard :

- [ ] Interface admin pour approuver/refuser
- [ ] Notification élève quand demande traitée
- [ ] Historique visible dans l'UI élève
- [ ] Application automatique après approbation
- [ ] Quotas et limites par utilisateur

## 🎓 Notes pédagogiques

Cette fonctionnalité montre aux élèves :
- Workflow de demande/validation
- Gestion de base de données relationnelle
- Envoi d'emails automatisés
- Validation côté client et serveur
- Architecture REST API

## 🏆 Résumé

✅ **6 fichiers créés**
✅ **3 fichiers modifiés**
✅ **450+ lignes de code ajoutées**
✅ **Documentation complète**
✅ **Testé et fonctionnel**

🚀 **Prêt à l'emploi !**
