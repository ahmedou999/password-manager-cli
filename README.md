# password-manager-cli
Un petit gestionnaire de mots de passe en Python, utilisable en ligne de commande, avec :

- Mot de passe maître sécurisé (hachage SHA3-256)
- Chiffrement des mots de passe enregistrés (Fernet)
- Stockage local dans un fichier JSON
- Interface interactive en ligne de commande (ajout, lecture, suppression)

---

## ⚙️ Fonctionnalités

- 🔑 Saisie d’un mot de passe maître au lancement
- ➕ Ajout d’un identifiant + mot de passe chiffré
- 🔍 Affichage des identifiants enregistrés
- 🗑️ Suppression d’un mot de passe
- 🧠 Protection en cas de fichier corrompu
- 🔒 Chiffrement Fernet + Hachage SHA3

---

## 💻 Utilisation

```bash
python gestionnaire.py
