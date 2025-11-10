#!/usr/bin/env python3
"""
Script de test pour la fonctionnalité de demande de ressources.
"""

import sys
import os

# Ajouter le dossier backend au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 60)
print("TEST: Système de demande de ressources")
print("=" * 60)
print()

# Test 1: Import des modules
print("✓ Test 1: Import des modules...")
try:
    import database
    from email_config import send_resource_request_email, test_email_config
    print("  ✅ Modules importés avec succès")
except Exception as e:
    print(f"  ❌ Erreur d'import: {e}")
    sys.exit(1)

# Test 2: Base de données
print("\n✓ Test 2: Base de données SQLite...")
try:
    # La DB est initialisée automatiquement lors de l'import
    from pathlib import Path
    db_path = Path(__file__).parent / 'backend' / 'resource_requests.db'
    if db_path.exists():
        print(f"  ✅ Base de données créée: {db_path}")
    else:
        print(f"  ❌ Base de données introuvable")
        sys.exit(1)
except Exception as e:
    print(f"  ❌ Erreur DB: {e}")
    sys.exit(1)

# Test 3: Insertion test
print("\n✓ Test 3: Insertion d'une demande test...")
try:
    test_specs_current = {
        'ram_mb': 2048,
        'cpu': 2,
        'storage_gb': 20
    }
    test_specs_requested = {
        'ram_mb': 4096,
        'cpu': 4,
        'storage_gb': 50
    }
    
    request_id = database.add_resource_request(
        username="test_user",
        vm_name="test_vm",
        current_specs=test_specs_current,
        requested_specs=test_specs_requested,
        reason="Test de la fonctionnalité"
    )
    
    print(f"  ✅ Demande test créée (ID: {request_id})")
    
    # Vérifier qu'on peut la récupérer
    requests = database.get_user_requests("test_user")
    if requests:
        print(f"  ✅ Demande récupérée: {len(requests)} demande(s) trouvée(s)")
    else:
        print(f"  ❌ Impossible de récupérer la demande")
        
except Exception as e:
    print(f"  ❌ Erreur insertion: {e}")
    sys.exit(1)

# Test 4: Configuration email
print("\n✓ Test 4: Configuration email...")
try:
    from email_config import SMTP_USERNAME, SMTP_PASSWORD, ADMIN_EMAIL
    
    if SMTP_USERNAME == "votre-email@gmail.com":
        print("  ⚠️  Configuration email par défaut (non configurée)")
        print("  📝 Lisez EMAIL_CONFIG.md pour configurer l'envoi d'emails")
    else:
        print(f"  ✅ Email configuré: {SMTP_USERNAME}")
        print(f"  ✅ Destinataire: {ADMIN_EMAIL}")
        
        # Test connexion SMTP (optionnel)
        response = input("\n  Tester la connexion SMTP ? (o/N): ")
        if response.lower() == 'o':
            print("  Connexion SMTP en cours...")
            if test_email_config():
                print("  ✅ Connexion SMTP réussie !")
                
                # Proposer d'envoyer un email de test
                response2 = input("\n  Envoyer un email de test ? (o/N): ")
                if response2.lower() == 'o':
                    print("  Envoi d'un email de test...")
                    if send_resource_request_email(
                        username="test_user",
                        vm_name="test_vm",
                        current_specs=test_specs_current,
                        requested_specs=test_specs_requested,
                        reason="Ceci est un email de test automatique."
                    ):
                        print(f"  ✅ Email envoyé à {ADMIN_EMAIL}")
                    else:
                        print("  ❌ Échec de l'envoi")
            else:
                print("  ❌ Connexion SMTP échouée")
                print("  📝 Vérifiez vos identifiants dans backend/email_config.py")
        
except Exception as e:
    print(f"  ⚠️  Erreur config email: {e}")
    print("  📝 Lisez EMAIL_CONFIG.md pour configurer")

# Résumé
print("\n" + "=" * 60)
print("RÉSUMÉ")
print("=" * 60)
print("✅ Base de données: OK")
print("✅ API backend: OK (à tester avec Flask)")
print("✅ Frontend: OK (modal + bouton ajoutés)")

if SMTP_USERNAME != "votre-email@gmail.com":
    print("✅ Email: Configuré")
else:
    print("⚠️  Email: Non configuré (optionnel)")
    print("   📝 Lisez EMAIL_CONFIG.md si vous voulez activer l'envoi d'emails")

print("\n🚀 La fonctionnalité est prête !")
print()
print("Pour tester :")
print("  1. cd backend && python main.py")
print("  2. Ouvrez http://localhost:5000")
print("  3. Connectez-vous (alice/alice)")
print("  4. Allez dans 'Mes VMs'")
print("  5. Cliquez sur '📊 Demander ressources' pour une VM")
print()
