# Revue de déploiement pour le professeur

## Aperçu du projet

**VM_Manager** est une application web basée sur Flask pour gérer des machines virtuelles (Vagrant/libvirt) avec un simple formulaire de demande de ressources. Le projet est maintenant prêt pour un déploiement automatisé utilisant Ansible avec containerisation Docker pour le frontend.

## Architecture

- **Backend** : Python 3 + Flask + Gunicorn (service systemd sur port 5000)
- **Frontend** : HTML/CSS/JS statique avec intégration Formspree (conteneur Docker sur port 8080)
- **Orchestration** : playbook Ansible pour automatiser le déploiement complet
- **Gestion des secrets** : Ansible Vault pour les variables sensibles (ex: `SECRET_KEY`)

## Fichiers clés pour examen

### 1. **ansible/deploy.yml** - Playbook principal
**Objectif** : Automatiser le déploiement complet (backend + frontend).

**Tâches** :
- Installer les dépendances système (git, python3-venv, docker.io)
- Cloner/mettre à jour le dépôt depuis GitHub
- Rendre deploy.sh exécutable
- Exécuter deploy.sh (crée venv, installe requirements, génère l'unité systemd)
- Templater l'environnement Flask et le service systemd
- Redémarrer le service systemd
- Construire l'image Docker du frontend (idempotente)
- Gérer le conteneur frontend (ancien conteneur supprimé, nouveau démarré)
- Collecter et afficher les faits du service

**Idempotence** : 
- Utilise la clause `creates` sur deploy.sh pour éviter les ré-exécutions
- Les tâches Docker image/container sont idempotentes (basées sur état)
- Les tâches template se mettent à jour seulement quand le contenu change
- Les tâches systemd utilisent la gestion d'état

### 2. **ansible/inventory.ini** - Hôtes cibles
```ini
[vmhosts]
localhost ansible_connection=local
```
Configuré pour tests locaux ; remplacer par l'adresse IP/nom d'hôte du serveur cible pour la production.

### 3. **ansible/templates/** - Templates de configuration
- `vm_manager.service.j2` : unité systemd avec utilisateur, chemins, workers, port configurables
- `env.j2` : template Flask .env avec SECRET_KEY et variables LDAP optionnelles

### 4. **ansible/group_vars/all/vault.yml.example** - Template des secrets
Fournit un modèle sûr pour stocker les données sensibles :
```yaml
secret_key: "change_me_super_secret"
```
Doit être chiffré avec `ansible-vault` avant utilisation en production.

### 5. **ansible/README.md** - Guide d'utilisation
Contient :
- Prérequis et commandes de démarrage rapide
- Configuration Ansible Vault et meilleures pratiques
- Notes d'intégration

## Considérations de sécurité

✅ **Implémenté** :
- Aucun secret en clair dans le dépôt (exemple vault.yml fourni)
- Chiffrement `ansible-vault` recommandé pour les variables sensibles
- Les secrets sont injectés à l'exécution via variables Ansible, pas hardcodés
- Le service s'exécute sous un utilisateur non-root (configurable via `service_user`)
- Service systemd avec politique de redémarrage pour la fiabilité

⚠️ **Recommandations pour le professeur** :
1. Chiffrer `vault.yml` avant le déploiement sur le serveur de l'école
2. Utiliser `--ask-vault-pass` ou un `--vault-password-file` sécurisé à l'exécution
3. Auditer `deploy.sh` pour s'assurer qu'il respecte vos politiques de sécurité
4. Vérifier que l'authentification par clé SSH est configurée pour la machine de contrôle Ansible

## Idempotence et répétabilité

✅ **Caractéristiques** :
- Les tâches `command` utilisent `creates` pour sauter si déjà faites
- Les tâches Docker image/container utilisent des modules basés sur l'état (idempotentes)
- Les tâches template ne modifient que si la source change
- systemd daemon_reload assure que la configuration est à jour
- Exécuter le playbook plusieurs fois ne produit aucun changement indésirable

## Checklist de déploiement

**Avant la production** :
- [ ] Réviser et approuver `ansible/deploy.yml`
- [ ] Réviser la gestion sécurité/secrets
- [ ] Vérifier les prérequis de l'hôte cible (Debian/Ubuntu, accès SSH, sudo)
- [ ] Configurer le mot de passe Vault (lieu sécurisé)
- [ ] Exécuter `ansible-lint` sur la machine de contrôle (optionnel mais recommandé)
- [ ] Vérification syntaxe : `ansible-playbook --syntax-check -i ansible/inventory.ini ansible/deploy.yml`
- [ ] Exécuter dry-run : `ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --check --ask-vault-pass`

**Vérifications post-déploiement** :
```bash
# Sur le serveur cible :
systemctl status vm_manager.service
curl -fsS http://localhost:5000/
docker ps --filter name=vm_frontend
journalctl -u vm_manager.service -n 50
```

## Fichiers inclus dans la revue

```
ansible/
├── deploy.yml                    # Playbook principal
├── inventory.ini                 # Hôtes cibles
├── README.md                     # Guide utilisation & Vault
├── group_vars/
│   └── all/
│       └── vault.yml.example     # Template des secrets
└── templates/
    ├── vm_manager.service.j2     # Template unité systemd
    └── env.j2                    # Template environnement Flask
```

Plus ces fichiers support dans la racine du dépôt :
- `deploy.sh` - Script de configuration locale (appelé par le playbook)
- `frontend/Dockerfile` - Containerisation du frontend
- `backend/requirements.txt` - Dépendances Python
- `README.md` - Aperçu du projet (branche main)

## Prochaines étapes (Après approbation)

1. **Chiffrer le fichier Vault** (sur votre machine) :
   ```bash
   cp ansible/group_vars/all/vault.yml.example ansible/group_vars/all/vault.yml
   ansible-vault encrypt ansible/group_vars/all/vault.yml
   # Définir un mot de passe fort
   ```

2. **Tester sur le serveur de staging** :
   ```bash
   ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --ask-vault-pass
   ```

3. **Vérifier le déploiement** :
   - Vérifier l'état systemd
   - Tester l'API backend
   - Vérifier que le conteneur frontend s'exécute
   - Vérifier les journaux pour les erreurs

4. **Déploiement final en production** (après validation de staging) :
   - Mettre à jour `inventory.ini` avec les hôtes de production
   - Exécuter le playbook avec le mot de passe Vault approprié

## Questions ou problèmes ?

- Modules playbook : voir `ansible/README.md`
- Gestion des secrets : section "Ansible Vault" dans `ansible/README.md`
- Journaux du service : `journalctl -u vm_manager.service` sur le serveur cible
- Journaux Docker : `docker logs vm_frontend` sur le serveur cible

---

**État** : ✅ Prêt pour revue du professeur
**Dernière mise à jour** : 27 novembre 2025
