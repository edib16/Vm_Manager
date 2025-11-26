# Résumé des corrections Windows - 10 novembre 2025

## 3 problèmes corrigés ✅

### 1. Clavier QWERTY → AZERTY ✅

**Problème** : La box Windows par défaut est en anglais/QWERTY

**Solution implémentée** :
- Configuration système complète en français (`Set-WinSystemLocale fr-FR`)
- Configuration clavier AZERTY pour tous les utilisateurs (`Set-WinUserLanguageList fr-FR`)
- Configuration registre pour l'écran de connexion (HKU)
- Configuration registre machine pour tous les nouveaux utilisateurs
- Fuseau horaire Europe/Paris

**Résultat** : Après le redémarrage automatique, le clavier est **AZERTY français** partout (écran de connexion, session utilisateur, etc.)

---

### 2. Utilisateur vagrant non renommé ✅

**Problème** : L'utilisateur `vagrant` restait visible au lieu d'être renommé

**Pourquoi ça échouait** : On ne peut pas renommer un utilisateur pendant qu'il est connecté (et Vagrant utilise vagrant pour se connecter et faire le provisioning !)

**Solution implémentée** :
- **Création d'un NOUVEAU compte** avec ton nom d'utilisateur + ton mot de passe
- **Conservation de vagrant** avec le même mot de passe (pour compatibilité Vagrant)
- Les deux comptes ont les droits administrateur

**Résultat** : 
- 3 comptes disponibles : `Administrator`, `[ton_user]`, `vagrant`
- Tous avec les mots de passe que tu as configurés
- Utilise **ton nom d'utilisateur** en priorité

---

### 3. Bouton "Arrêter" ne fonctionne pas sur Windows ✅

**Problème** : Windows Server résiste à l'arrêt gracieux (`vagrant halt` timeout)

**Solution implémentée** :
- Tentative d'arrêt propre d'abord (`vagrant halt`, timeout 30s)
- Si échec ou timeout : **arrêt forcé** avec `virsh destroy` (équivalent à débrancher)
- Message clair à l'utilisateur : "arrêté (forcé)" si nécessaire

**Résultat** : Le bouton "Arrêter" fonctionne **toujours**, même si Windows résiste. L'arrêt est forcé après 30 secondes.

---

## Commandes de test

### Supprimer l'ancienne VM
```bash
cd /home/edib/Vm_Manager/student_vms/alice/edib
vagrant destroy -f
cd ..
rm -rf edib
```

### Créer une nouvelle VM Windows
Via WebUI avec :
- Username : `monnom`
- Password : `Azerty123` (8+ chars, Maj, min, chiffre)
- Root password : `Admin2024`

### Vérifier après provisioning (10 min)
1. Clavier AZERTY ✅
2. Comptes disponibles :
   - `Administrator` / `Admin2024` ✅
   - `monnom` / `Azerty123` ✅
   - `vagrant` / `Azerty123` ✅
3. Bouton arrêter fonctionne ✅

---

## Logs à surveiller

### Terminal Flask
```
✅ Langue/Clavier: Français (AZERTY)
✅ Comptes configurés:
   - Administrator / ***
   - monnom / ***
   - vagrant / *** (même mdp, pour compatibilité)
```

### WebUI
```
✅ VM Windows créée ! Comptes configurés :
   • Administrator / ***
   • monnom / ***
   • vagrant / *** (même mdp)
⌨️ Clavier: AZERTY (français) après redémarrage
```

---

## Fichiers modifiés

1. `backend/main.py`
   - Script PowerShell complètement réécrit
   - Configuration AZERTY complète
   - Création de compte séparé (pas de renommage)
   - Fonction `halt_vm()` avec arrêt forcé

2. `frontend/static/app.js`
   - Messages clarifiés (3 comptes disponibles)
   - Info clavier AZERTY

3. `frontend/index.html`
   - Version JS mise à jour (v13)

4. `WINDOWS_VMS.md`
   - Documentation mise à jour (3 comptes, AZERTY)

---

## À retenir

✅ **Clavier** : AZERTY après le 1er redémarrage automatique  
✅ **Comptes** : Utiliser ton nom d'utilisateur, pas vagrant  
✅ **Arrêt** : Forcé automatiquement si Windows résiste  
✅ **Provisioning** : 5-10 minutes, patience !
