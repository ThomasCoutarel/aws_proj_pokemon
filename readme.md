### **1. Source des données**

* **Site choisi :** [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number)

* **Raisons du choix :**

    * Base complète des Pokémon par génération (I → IX)
    * Chaque génération est clairement séparée par un titre HTML (`span id="Generation_I"`)
    * Chaque Pokémon possède une image miniature directement accessible


### **2. Langage et librairies**

* **Python 3 :**

    * Langage que je maitrise pour le scraping, et compatible avec d'autre libraie qu'on va utilisé ensuite    * Large écosystème de librairies pour le web et le cloud

* **Librairies utilisées :**

    1. **`requests`** : pour télécharger les pages HTML et les images depuis Bulbapedia
    2. **`BeautifulSoup4` (bs4)** : pour parser le HTML et extraire les informations et images de manière fiable
    3. **`urllib.parse.urljoin`** : pour construire correctement les URLs des images
    4. **`boto3`** : SDK officiel AWS pour Python, utilisé pour uploader les images vers S3
    5. **`os` et `pathlib`** : pour gérer les chemins locaux de manière sécurisée

* **Raisons du choix :**

    * Simplicité et robustesse des librairies
    * Boto3 permet de gérer facilement les permissions, la création de dossiers dans S3, et la gestion des erreurs d’upload
    * `requests` + `BeautifulSoup` est un standard pour le scraping web léger

---

### **3. Gestion des erreurs**

* **Téléchargement des images :**

    * Vérification du **status code** HTTP pour détecter les erreurs 404 ou 500
    * Gestion des exceptions réseau (`try/except`) pour éviter que le script plante sur une image introuvable
    * Affichage des messages `[OK]` ou `[ERREUR]` pour chaque image

* **Scraping HTML :**

    * Vérification de l’existence des sections (`span id="Generation_X"`) et des tables Pokémon
    * Limitation à 10 Pokémon par génération pour éviter de surcharger le site ou le script

* **Upload S3 :**

    * Gestion des erreurs de permissions (`Unable to locate credentials`) via configuration AWS CLI ou IAM Role
    * Validation que le bucket existe et que le chemin de destination est correct

* **Logs clairs dans le terminal** : permet de savoir exactement quelles images ont été téléchargées et quelles erreurs sont survenues.

### **4. Infrastructure AWS**

* **Connexion à l’EC2 :**

    * Nous nous sommes connectés via SSH depuis le terminal Windows :

      ```
      ssh -i "C:\Users\couta\Downloads\ssh_rsa_pokemon.pem" ubuntu@ec2-13-60-95-64.eu-north-1.compute.amazonaws.com
      ```
    * Toutes les actions (installation des dépendances, configuration AWS CLI, lancement du script) se sont faites directement **dans ce terminal sur l’instance EC2**.

* **Instance EC2 Ubuntu :**

    * Exécute le script Python pour scraper et uploader
    * Dépendances Python installées sur la machine (`requests`, `bs4`, `boto3`)
    * AWS CLI installé et configuré avec les credentials ou un IAM Role

* **Bucket S3 public :**

    * Stockage centralisé, durable et accessible publiquement
    * Organisation en dossiers par génération (`Generation_I/`, `Generation_II/`, …)
    * Policy de bucket : lecture publique (`s3:GetObject`) pour chaque objet

---

### **5. Script Python : script\_pokemon\_s3.py**

* **Fonctions principales :**

    1. Récupérer la page Bulbapedia des Pokémon par génération
    2. Scraper les 10 premiers Pokémon de chaque génération (pas besoin de tout)
  3Uploader directement vers S3 dans le répertoire correspondant

* **Avantages :** automatisation complète, compatible EC2 + S3, limitation configurable des Pokémon.

---

### **6. Flux de données**

1. SSH vers l’EC2 et lancement du script
2. Scraping des pages web Bulbapedia
3. Téléchargement des images et upload vers S3
4. Bucket S3 accessible publiquement pour chaque image

---

### **7. Sécurité et permissions**

* IAM Role attaché à l’EC2 ou credentials AWS CLI pour uploader vers S3
* Bucket public limité à la lecture (`s3:GetObject`)
* Pas de stockage de clés dans le script si IAM Role utilisé