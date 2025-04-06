import hashlib, json
from pathlib import Path
from cryptography.fernet import Fernet


def hashMdpMaitre():
    mdp = input("🔑 Créez votre mot de passe maître (ne l'oubliez pas, il est irrécupérable) : ")

    while True:
        mdpConfirm = input("🔄 Confirmez votre mot de passe ou tapez 'return' pour en choisir un autre : ")

        if mdpConfirm.lower().strip() == "return":
            print("↩ Recommençons...")
            return hashMdpMaitre()  # Relance la fonction pour choisir un nouveau mot de passe

        if mdpConfirm == mdp:
            break  # ✅ Si les mots de passe correspondent, on sort de la boucle

        print("❌ Les mots de passe ne correspondent pas. Réessayez.")

    # Hachage du mot de passe
    mdpH = hashlib.sha3_256(mdp.encode()).hexdigest()

    # Sauvegarde dans un fichier JSON
    with open("mot_de_passe.json", "w") as f:
        json.dump({"mot_de_passe_maitre": mdpH}, f)

    print("✅ Mot de passe maître enregistré avec succès !")




def existeMdpMaitre():
    fichier=Path("mot_de_passe.json")

    if not fichier.exists():
        print("❌ Aucun mot de passe maître trouvé. Création en cours...")
        return False
    try:
        with open("mot_de_passe.json") as f:
            data= json.load(f)
    
    except json.JSONDecodeError:
        print("⚠ Erreur : Le fichier JSON est corrompu. Supprimez-le et recréez un mot de passe maître.")
        return False
    
    if "mot_de_passe_maitre" in data:
        print("✅ Mot de passe maître trouvé !")
        return True
    else:
        print("⚠ Aucun mot de passe maître valide dans le fichier.")
        return False




def verifierMdpMaitre():
    
    if not existeMdpMaitre():
        hashMdpMaitre()
        return True
    
    with open("mot_de_passe.json") as f:
        data= json.load(f)
    
    mdpMaitreHash=data["mot_de_passe_maitre"]

    essaie=3
    while essaie > 0:
        
        verifMdp=input(f"veuillez entrez le mot de passe du gestionnaire(il vous reste {essaie} essaie):")
        hashVerifMdp=hashlib.sha3_256(verifMdp.encode()).hexdigest()
        
        if hashVerifMdp == mdpMaitreHash:
            print("✅Mot de Passe correct")
            return True
        essaie -= 1
    
    print("⛔ Trop de tentatives. Accès refusé.")
    return False




def get_or_create_key():
    """ Vérifie si la clé existe, sinon la crée et la sauvegarde """
    fichier_cle = Path("cle_secrete.key")

    if fichier_cle.exists():
        # 🔑 Charger la clé existante
        with open("cle_secrete.key", "rb") as key_file:
            key = key_file.read()
        print("✅ Clé de chiffrement chargée.")
    else:
        # 🔑 Générer une nouvelle clé (première utilisation)
        key = Fernet.generate_key()
        with open("cle_secrete.key", "wb") as key_file:
            key_file.write(key)
        print("🔐 Nouvelle clé de chiffrement générée et sauvegardée.")

    return key



def ajouterMotDePasse():
    serv = input("🔹 Veuillez entrer le nom du service à enregistrer (ex: Twitter) : ").strip().lower()
    id = input("👤 Veuillez entrer votre identifiant (ex: user@gmail.com) : ").strip()
    mdp = input("🔑 Veuillez entrer le mot de passe : ").strip()

    key= get_or_create_key()
    fernet=Fernet(key)
    mdpChiffrer=fernet.encrypt(mdp.encode()).decode()

    fichier=Path("mdp_stockes.json")
    
    if fichier.exists():
        try:
            with open("mdp_stockes.json", "r") as f:
                data = json.load(f)  # Charger le JSON existant
        except json.JSONDecodeError:
            print("⚠ Fichier JSON corrompu. Réinitialisation.")
            data = {}  # Si le fichier est corrompu, repartir de zéro
    else:
        data= {}
    
    if serv not in data:
        data[serv]=[]

    data[serv].append({"identifiant": id, "mot_de_passe": mdpChiffrer})

    with open("mdp_stockes.json","w") as f:
        json.dump(data,f,indent=4)
    
    print(f"✅identifiant et Mot de passe pour {serv} enregistré avec succès !")




def recupererMotDePasse():
    fichier = Path("mdp_stockes.json")
    
    if not fichier.exists():
        print("❌ Aucun mot de passe enregistré.")
        return

    with open("mdp_stockes.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("⚠ Fichier JSON corrompu. Impossible de récupérer les mots de passe.")
            return

    if not data:
        print("❌ Aucun service enregistré.")
        return

    # ✅ Afficher la liste des services disponibles
    print("\n📋 **Services enregistrés** :")
    for service in data.keys():
        print(f"  🔹 {service}")

    # ✅ Demander un service existant
    while True:
        serv = input("\n🔹 Entrez le nom du service à récupérer : ").strip().lower()
        if serv in data:
            break
        print("❌ Ce service n'existe pas. Veuillez choisir parmi la liste affichée.")

    key = get_or_create_key()
    fernet = Fernet(key)

    print(f"\n🔐 Comptes enregistrés pour {serv} :")
    for compte in data[serv]:
        identifiant = compte["identifiant"]
        mdpdecrypt = fernet.decrypt(compte["mot_de_passe"].encode()).decode()
        print(f"👤 Identifiant : {identifiant} | 🔑 Mot de passe : {mdpdecrypt}")

    print("\n✅ Récupération terminée.")



def supprimerMotDePasse():
    serv = input("🔹 Veuillez entrer le nom du service à enregistrer (ex: Twitter) : ").strip().lower()
    id = input("👤 Veuillez entrer l'identidfiant que vous voullez supprimer (ex: user@gmail.com) : ").strip()
    mdp = input("🔑 Veuillez entrer le mot de passe que vous voullez supprimer : ").strip()

    with open("mdp_stockes.json", "r") as f:
        try:
            data=json.load(f)
        except json.JSONDecodeError:
            print("⚠ Fichier JSON corrompu. Impossible de supprimer le mots de passe.")
            return    

    if serv not in data:
        print(f"❌ Aucun mot de passe enregistré pour {serv}.")
        return
    
    key=get_or_create_key()
    fernet=Fernet(key)

    nv_comptes=[]
    for compte in data[serv]:
        identifiant=compte["identifiant"]
        motDePasse=fernet.decrypt(compte["mot_de_passe"].encode()).decode()
        if not(identifiant == id and motDePasse == mdp):
            nv_comptes.append(compte)

    if nv_comptes:
        data[serv] = nv_comptes
    else:
        del data[serv]
        

    with open("mdp_stockes.json","w") as f:
        json.dump(data,f,indent=4)
    
    print(f"✅ Identifiant {id} pour {serv} supprimé avec succès !")




def menu():
    verifierMdpMaitre()  # Vérifier le mot de passe maître au début

    while True:  # ✅ Permet de revenir au menu après chaque action
        print("\n🔹 Que voulez-vous faire ?")
        print("1️⃣ Ajouter un mot de passe")
        print("2️⃣ Récupérer un mot de passe")
        print("3️⃣ Supprimer un mot de passe")
        print("4️⃣ Quitter")

        num = input("👉 Entrez votre choix : ").strip()

        if num == "1":
            ajouterMotDePasse()
        elif num == "2":
            recupererMotDePasse()
        elif num == "3":
            supprimerMotDePasse()
        elif num == "4":
            print("👋 Au revoir !")  # ✅ Message de sortie
            break  # ✅ Quitte proprement la boucle
        else:
            print("❌ Choix invalide. Veuillez entrer un chiffre entre 1 et 4.")

menu()
