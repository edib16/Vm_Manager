# 📋 Checklist de Déploiement VM_Manager

## ✅ Préparation Locale (Terminée)

- [x] Service systemd utilisateur configuré et testé
- [x] Création de VM asynchrone implémentée
- [x] noVNC installé localement
- [x] Réseau libvirt `default` démarré
- [x] Permissions sudo configurées pour vagrant-libvirt
- [x] Documentation mise à jour (README.md, DEPLOYMENT_NATIVE.md)
- [x] Code nettoyé (dossiers inutiles supprimés)

## 📦 À Faire sur le Serveur iris.a3n.fr

### Étape 1 : Connexion et Préparation
```bash
ssh -i ~/.ssh/mediaschool edib@37.64.159.66 -p 2222
cd ~
git clone https://github.com/Mediaschool-BTS-SISR-2025/edib_ansible.git Vm_Manager
cd Vm_Manager
```

### Étape 2 : Installation et Configuration
```bash
# Exécuter le script de déploiement
chmod +x deploy-native.sh
./deploy-native.sh

# Installer noVNC
sudo apt install novnc || sudo git clone https://github.com/novnc/noVNC /usr/share/novnc

# Configurer les permissions libvirt
sudo usermod -aG libvirt iris
echo '%libvirt ALL=(root) NOPASSWD: /usr/bin/virsh, /usr/bin/qemu-system-x86_64' | sudo tee /etc/sudoers.d/vagrant-libvirt
sudo chmod 440 /etc/sudoers.d/vagrant-libvirt

# Démarrer le réseau libvirt
sudo virsh net-start default 2>/dev/null || true
sudo virsh net-autostart default

# Configurer l'environnement
nano .env  # Éditer avec les vraies valeurs
```

### Étape 3 : Configuration Traefik
```bash
# Copier la configuration Traefik
sudo cp traefik-config.yml /etc/traefik/dynamic/vm_manager.yml

# Recharger Traefik
docker restart traefik  # Si Traefik est en Docker
# OU
sudo systemctl reload traefik  # Si Traefik est en systemd
```

### Étape 4 : Vérifications
```bash
# Vérifier le service
sudo systemctl status vm_manager.service

# Voir les logs
sudo journalctl -u vm_manager.service -f

# Test local
curl http://localhost:5000/api/vms

# Test externe
curl https://vm-manager.iris.a3n.fr
```

## 🔧 Commandes Utiles en Production

### Gestion du Service
```bash
# Démarrer
sudo systemctl start vm_manager.service

# Arrêter
sudo systemctl stop vm_manager.service

# Redémarrer
sudo systemctl restart vm_manager.service

# Statut
sudo systemctl status vm_manager.service

# Logs temps réel
sudo journalctl -u vm_manager.service -f

# Logs des dernières 24h
sudo journalctl -u vm_manager.service --since "24 hours ago"
```

### Mise à Jour du Code
```bash
cd ~/Vm_Manager
git pull origin main
sudo systemctl restart vm_manager.service
```

### Gestion des VMs
```bash
# Lister toutes les VMs
sudo virsh list --all

# Voir les ports VNC
sudo virsh vncdisplay <vm_name>

# Supprimer une VM bloquée
sudo virsh destroy <vm_name>
sudo virsh undefine <vm_name> --remove-all-storage
```

## 🚨 Troubleshooting

### Problème : Service ne démarre pas
```bash
# Vérifier les logs détaillés
sudo journalctl -u vm_manager.service -n 100 --no-pager

# Vérifier les permissions
ls -la ~/Vm_Manager/.venv/bin/gunicorn
ls -la ~/Vm_Manager/backend/

# Tester manuellement
cd ~/Vm_Manager
source .venv/bin/activate
cd backend
gunicorn --bind 127.0.0.1:5000 main:app
```

### Problème : VM ne se crée pas
```bash
# Vérifier libvirt
sudo systemctl status libvirtd
sudo virsh net-list --all

# Vérifier Vagrant
vagrant version
vagrant plugin list

# Nettoyer les locks Vagrant
rm -rf ~/Vm_Manager/student_vms/*/.vagrant/
```

### Problème : noVNC ne fonctionne pas
```bash
# Vérifier noVNC
ls -la /usr/share/novnc/

# Vérifier websockify
which websockify
pip list | grep websockify

# Tester manuellement
websockify 6080 localhost:5900
```

## 📊 Monitoring

### Logs en Temps Réel
```bash
# Backend
sudo journalctl -u vm_manager.service -f

# Libvirt
sudo journalctl -u libvirtd -f

# Traefik (si systemd)
sudo journalctl -u traefik -f
```

### Métriques Système
```bash
# CPU/RAM
htop

# Espace disque
df -h /var/lib/libvirt/images/

# VMs actives
sudo virsh list
```
