# ⚡ Configuration rapide de l'email (5 minutes)

## 1️⃣ Créer un mot de passe d'application Gmail

1. Va sur https://myaccount.google.com/apppasswords
2. Connecte-toi avec ton compte Gmail
3. Dans "Sélectionnez l'application" → **Autre**
4. Tape `VM Manager` et clique sur **Générer**
5. **Copie le mot de passe de 16 caractères** (format: `xxxx xxxx xxxx xxxx`)

## 2️⃣ Configurer le fichier

Ouvre `/home/edib/Vm_Manager/backend/email_config.py` et modifie :

```python
SMTP_USERNAME = "TON-EMAIL@gmail.com"        # ← Change ici
SMTP_PASSWORD = "xxxxxxxxxxxxxxxx"           # ← Colle le mot de passe (sans espaces)
```

**Exemple :**
```python
SMTP_USERNAME = "edib.vm@gmail.com"
SMTP_PASSWORD = "abcdabcdabcdabcd"  # ← Les 16 caractères sans espaces
```

## 3️⃣ Tester

```bash
cd /home/edib/Vm_Manager/backend
python3 -c "from email_config import test_email_config; test_email_config()"
```

Si tu vois `✅ Configuration SMTP valide`, c'est bon ! 🎉

## ⚠️ Sécurité

**Important :** Ne commit pas ce fichier sur GitHub !

```bash
echo "backend/email_config.py" >> .gitignore
```

---

**Note :** Si tu ne configures pas l'email, ça fonctionne quand même ! Les demandes seront enregistrées dans la base de données SQLite (`backend/resource_requests.db`).
