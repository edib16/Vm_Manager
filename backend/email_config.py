"""
Configuration pour l'envoi d'emails.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "votre-email@gmail.com"  # À configurer
SMTP_PASSWORD = "votre-app-password"      # À configurer avec un mot de passe d'application Gmail

# Destinataire des demandes
ADMIN_EMAIL = "edib.1605@gmail.com"

def send_resource_request_email(username, vm_name, current_specs, requested_specs, reason):
    """
    Envoie un email à l'administrateur pour une demande de ressources.
    
    Args:
        username: Nom de l'utilisateur
        vm_name: Nom de la VM
        current_specs: Dict avec ram_mb, cpu, storage_gb actuels
        requested_specs: Dict avec ram_mb, cpu, storage_gb demandés
        reason: Motif de la demande
    
    Returns:
        True si envoi réussi, False sinon
    """
    try:
        # Créer le message
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = f"[VM Manager] Demande de ressources - {vm_name} ({username})"
        
        # Corps du message
        body = f"""
Nouvelle demande de ressources pour une VM

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INFORMATIONS GÉNÉRALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 Utilisateur : {username}
🖥️  Machine virtuelle : {vm_name}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESSOURCES ACTUELLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💾 RAM : {current_specs['ram_mb']} MB ({current_specs['ram_mb'] / 1024:.1f} GB)
⚙️  CPU : {current_specs['cpu']} vCPU(s)
💿 Stockage : {current_specs['storage_gb']} GB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESSOURCES DEMANDÉES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💾 RAM : {requested_specs['ram_mb']} MB ({requested_specs['ram_mb'] / 1024:.1f} GB)  [+{requested_specs['ram_mb'] - current_specs['ram_mb']} MB]
⚙️  CPU : {requested_specs['cpu']} vCPU(s)  [+{requested_specs['cpu'] - current_specs['cpu']} vCPU]
💿 Stockage : {requested_specs['storage_gb']} GB  [+{requested_specs['storage_gb'] - current_specs['storage_gb']} GB]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MOTIF DE LA DEMANDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{reason}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Cette demande a été enregistrée dans la base de données et attend votre traitement.

---
VM Manager - Plateforme de gestion des machines virtuelles
"""
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Connexion au serveur SMTP et envoi
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email envoyé à {ADMIN_EMAIL} pour {username}/{vm_name}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur envoi email: {e}")
        return False

def test_email_config():
    """
    Test la configuration SMTP.
    """
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
        print("✅ Configuration SMTP valide")
        return True
    except Exception as e:
        print(f"❌ Erreur configuration SMTP: {e}")
        return False
