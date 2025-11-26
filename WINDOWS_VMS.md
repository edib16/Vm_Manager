# Guide VMs Windows

## Création d'une VM Windows

### Exigences de mot de passe

Les VMs Windows ont des **politiques de sécurité strictes**. Les mots de passe doivent respecter :

- **Minimum 8 caractères**
- Au moins **1 lettre majuscule** (A-Z)
- Au moins **1 lettre minuscule** (a-z)
- Au moins **1 chiffre** (0-9)

Exemples valides :
- `Password123`
- `Azerty12`
- `Eleve2024`

❌ Exemples invalides :
- `azerty` (pas de majuscule ni chiffre)
- `AZERTY` (pas de minuscule ni chiffre)
- `Azerty` (pas de chiffre)

### Identifiants créés

Après la création d'une VM Windows, **trois comptes** sont disponibles :

1. **Administrator** / `[mot de passe root saisi]`
   - Compte administrateur principal
   - Accès complet au système

2. **[Nom d'utilisateur saisi]** / `[mot de passe utilisateur saisi]`
   - Compte élève personnalisé
   - Droits administrateur (membre du groupe Administrators)
   - **Nouveau compte créé spécialement**

3. **vagrant** / `[mot de passe utilisateur saisi]`
   - Compte Vagrant par défaut (conservé pour compatibilité)
   - Même mot de passe que votre compte personnalisé
   - Droits administrateur

⚠️ **Utilisez votre nom d'utilisateur personnalisé** (ou `vagrant` si besoin de compatibilité)

### Premier démarrage

⏱️ Le **provisioning Windows prend 5-10 minutes**. Soyez patient !

Le script PowerShell effectue :
1. Configuration langue/clavier français
2. Désactivation temporaire de la complexité des mots de passe
3. Création des comptes utilisateur
4. Activation de RDP
5. **Redémarrage automatique** pour appliquer les changements

### Connexion

1. Cliquez sur **"GUI"** dans la liste des VMs
2. Attendez l'écran de connexion Windows
3. Utilisez l'un des deux comptes créés :
   - **Administrator** avec votre mot de passe root
   - **Votre nom d'utilisateur** avec votre mot de passe utilisateur

### Dépannage

**Si les identifiants ne fonctionnent pas :**

1. Vérifiez que le provisioning est terminé (attendez 10 min après création)
2. Vérifiez les logs dans le terminal Flask
3. Reprovisionnez manuellement :
   ```bash
   cd /home/edib/Vm_Manager/student_vms/<utilisateur>/<vm_name>
   vagrant reload --provision
   ```

**Si vous voyez encore "vagrant" :**
- Le provisioning n'a pas fonctionné
- Vérifiez le fichier `provision.ps1` dans le dossier de la VM
- Tentez un redémarrage : `vagrant reload`

### Configuration système

| Type | RAM | CPU | Stockage | Réseau | Clavier |
|------|-----|-----|----------|--------|---------|
| Windows Server 2022 | 6 GB | 2 vCPU | ~40 GB | DHCP privé | **AZERTY (FR)** |
| Windows 10 Enterprise | 6 GB | 2 vCPU | ~30 GB | DHCP privé | **AZERTY (FR)** |

⌨️ **Le clavier est configuré en AZERTY français** dès le premier redémarrage après provisioning.

### Accès RDP (optionnel)

Si votre réseau le permet, vous pouvez aussi utiliser RDP :
```bash
# Récupérer l'IP de la VM
vagrant ssh -c "ipconfig" 
# ou depuis votre hôte
virsh domifaddr <vm_name>_default

# Connexion RDP
rdesktop <ip_vm>:3389
# ou
xfreerdp /v:<ip_vm> /u:Administrator
```

### Particularités Windows

- ⚠️ Les VMs Windows sont **volumineuses** (10-20 GB par box téléchargée)
- 🐌 Le **premier boot est très lent** (initialisation OOBE, provisioning)
- 🔄 Un **redémarrage automatique** a lieu après le provisioning
- 🇫🇷 Le **clavier FR** est configuré automatiquement
- 🔐 **RDP est activé** par défaut (firewall configuré)

### Boxes utilisées

- **Serveur** : `peru/windows-server-2022-standard-x64-eval`
- **Client** : `peru/windows-10-enterprise-x64-eval`

Ces boxes sont des **versions d'évaluation** (180 jours).
