# Documentation d'installation powercli et python pour faire tourner le code sur votre PC


### Étape 1 : Installer VMware PowerCLI

1. **Ouvrez PowerShell en tant qu'administrateur**. Recherchez PowerShell dans le menu de démarrage, cliquez droit dessus, puis choisissez "Exécuter en tant qu'administrateur".

2. **Installez VMware PowerCLI** avec la commande suivante :

   ```powershell
   Install-Module -Name "VMware.PowerCLI" -Scope AllUsers
   ```

3. **Configurez PowerCLI** pour ignorer les avertissements de certificats non valides (utile pour les tests ; à gérer différemment en production) :

   ```powershell
   Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false
   ```

### Étape 2 : Dot Source le Script

**Exécutez le script** avec la commande dot source pour qu'il soit chargé dans votre session PowerShell dans le dossier code:

   ```powershell
   . .\api.ps1
   ```

### Étape 3 : Installer Python et Flask

1. **Téléchargez et installez Python** si ce n'est pas déjà fait. Assurez-vous de cocher l'option "Add Python to PATH" lors de l'installation.

2. **Ouvrez un CMD** et installez Flask avec pip :

   ```bash
   pip install Flask
   ```

### Étape 4 : Exécuter l'Application Flask

1. **Placez votre application Flask** (y compris le fichier `app.py` et d'autres ressources nécessaires) dans un répertoire de votre choix.

2. **Ouvrez une invite de commande** ou PowerShell dans ce répertoire.

3. **Lancez votre application Flask** en exécutant :

   ```bash
   python app.py
   ```

   Assurez-vous que votre script `app.py` configure correctement l'application Flask pour écouter sur le port 5000 (ou tout autre port de votre choix).

### Étape 5 : Accéder à l'Application

1. **Ouvrez un navigateur web** et accédez à :

   ```
   http://localhost:5000/
   ```

   Vous devriez voir l'interface de votre application Flask, prouvant que tout fonctionne comme prévu.

---

# Documentation api.ps1


### Définition des paramètres initiaux

Le script commence par définir trois paramètres :

vcServer : L'adresse du serveur VMware vCenter.
username : Le nom d'utilisateur pour l'authentification avec le serveur vCenter.
password : Le mot de passe pour l'authentification avec le serveur vCenter.
###Vérification des paramètres
Il vérifie si tous les paramètres nécessaires (vcServer, username et password) sont fournis. Si l'un de ces paramètres est manquant, il affiche un message d'erreur et se termine.

### Connexion au vCenter
Utilisant les identifiants fournis, il se connecte au serveur vCenter spécifié avec la commande Connect-VIServer.

### Fonction Get-VMInfo
Cette fonction récupère et affiche des informations sélectionnées sur une VM spécifique. Elle accepte un paramètre vmName, cherche la VM correspondante, et si trouvée, affiche son nom, son adresse IP, son état (allumée ou éteinte), et la date de son dernier backup. Si aucune VM n'est trouvée avec le nom spécifié, un message d'erreur est affiché.

### Fonction Remove-SelectedVM
Cette fonction supprime une VM spécifiée par vmName. Elle vérifie d'abord si la VM est allumée et, dans ce cas, l'éteint de force avant de la supprimer définitivement. Si la VM spécifiée n'est pas trouvée, un message d'erreur est affiché.

### Fonction Restart-SelectedVM
Cette fonction redémarre la VM spécifiée par vmName. Si la VM est trouvée, elle est redémarrée sans confirmation. Si non trouvée, un message d'erreur est affiché.

### Fonction Add-NewVM
Cette fonction ajoute une nouvelle VM basée sur un template spécifié. Elle prend plusieurs paramètres pour définir les caractéristiques de la nouvelle VM, y compris le nom du client (customerName), le nom de la VM (vmName), le template à utiliser, le datastore pour le stockage, et une adresse IP optionnelle. La fonction crée ou trouve un dossier pour le client, sélectionne un hôte VM avec la mémoire la moins utilisée, vérifie l'existence du template et du datastore spécifiés, et configure le réseau de la VM en utilisant un commutateur distribué (vSwitch) spécifique. Si la nouvelle VM est créée avec succès, elle est allumée et un message de confirmation est affiché.

---

# Documentation app.py

Ce script Flask est une interface web pour gérer des machines virtuelles (VMs) dans un environnement VMware via des scripts PowerShell. Il définit plusieurs routes pour afficher des formulaires et exécuter des actions spécifiques sur les VMs, telles que les afficher, les supprimer, les redémarrer et en ajouter de nouvelles. Voici comment chaque partie fonctionne :

### Importations
Le script commence par importer les modules nécessaires, y compris `Flask` pour le framework web et `subprocess` pour exécuter les commandes PowerShell.

### Initialisation de l'application Flask
`app = Flask(__name__)` crée une instance de l'application Flask.

### Routes et Fonctions de Vue
- `@app.route('/')` : La page d'accueil qui affiche des liens vers chaque action possible.
- `@app.route('/display')` : Affiche un formulaire pour obtenir les informations d'une VM.
- `@app.route('/delete')` : Affiche un formulaire pour supprimer une VM.
- `@app.route('/restart')` : Affiche un formulaire pour redémarrer une VM.
- `@app.route('/add')` : Affiche un formulaire pour ajouter une nouvelle VM.

### Exécution des Actions
- `@app.route('/execute', methods=['POST'])` : Cette route gère la logique d'exécution des actions basées sur les données du formulaire soumis. Elle récupère les informations du formulaire, construit la commande PowerShell correspondante à l'action demandée, et exécute cette commande. Les actions possibles incluent l'affichage, la suppression, le redémarrage de VMs, et l'ajout de nouvelles VMs.

### Exécution de la Commande PowerShell
La commande PowerShell est construite en fonction de l'action sélectionnée et des informations fournies via le formulaire. Le script utilise `subprocess.run` pour exécuter la commande dans l'environnement PowerShell, capturer la sortie (stdout ou stderr), et afficher cette sortie sur une page web.

### Démarrage de l'Application
En fin de script, `app.run(debug=True)` démarre l'application Flask en mode débogage, ce qui est utile pendant le développement pour voir les erreurs et les modifications en temps réel.

---

# Documentation index.html


### Structure HTML :
- **DOCTYPE et Langue** : Le document commence par `<!DOCTYPE html>` pour déclarer le type de document HTML5 et utilise `<html lang="en">` pour spécifier l'anglais comme langue principale.
- **Section Head** : Contient des métadonnées incluant la déclaration du jeu de caractères (`<meta charset="UTF-8">`), le titre de la page web (`<title>Interface de Gestion VM</title>`), et les styles CSS internes.
- **Section Body** : Encapsule le contenu du document dans un élément `div` de classe "container" pour centrer et styliser le contenu. À l'intérieur de ce conteneur, il y a :
  - Un `div` avec la classe "logos" affichant les logos de SUPINFO et VMware vSphere 7, indiquant les outils ou organisations associés à l'application web.
  - Un titre `<h1>` avec le titre "Gestion VM" pour la page.
  - Une liste non ordonnée (`<ul>`) contenant des éléments de liste (`<li>`) qui agissent comme des boutons de navigation. Chaque élément de liste enveloppe une ancre (`<a>`) liant à différentes routes de l'application Flask (`/display`, `/delete`, `/restart`, `/add`), correspondant à différentes fonctionnalités comme afficher les infos VM, supprimer une VM, redémarrer une VM et ajouter une nouvelle VM.

### CSS Styling :
- **Styles Globaux** : Le `body` est stylisé avec un fond en dégradé, une couleur de texte blanche pour le contraste, et des propriétés flexbox pour centrer le contenu verticalement et horizontalement.
- **Styles du Conteneur** : La classe `.container` applique un fond blanc semi-transparent, des coins arrondis, une ombre pour la profondeur, et un padding pour l'espacement interne.
- **Styles des Logos** : La classe `.logos` utilise flexbox pour aligner horizontalement les logos, et les images à l'intérieur sont stylisées pour avoir une largeur maximale et une hauteur automatique pour la réactivité.
- **Styles des Titres et Listes** : Le titre `h1` contraste avec le fond plus clair du conteneur. La liste (`ul`) a son style par défaut supprimé, et ses éléments (`li`) sont stylisés comme des boutons bleus avec des effets de survol pour améliorer l'interactivité.
- **Styles des Ancres** : Les ancres à l'intérieur des éléments de liste sont stylisées pour hériter de la couleur du texte et supprimer le soulignement par défaut, rendant toute la zone du bouton cliquable.

---

# Documentation add.html


### Structure et Métadonnées
- **DOCTYPE et Langue** : Le document spécifie le type DOCTYPE pour HTML5 et définit l'anglais comme langue principale.
- **Head** : Contient la métadonnée de l'encodage de caractères UTF-8, le titre de la page, et les styles CSS internes pour styliser la page.

### Styles CSS
- Les styles définissent l'apparence de la page, y compris un arrière-plan en dégradé, une typographie lisible, et un conteneur central pour les éléments de formulaire.
- Les champs de formulaire (`input` et `button`) sont stylisés pour s'adapter au design global, avec des bordures arrondies et des couleurs distinctives pour les boutons, notamment un effet de survol.

### Corps de la Page
- **Conteneur** : Un `div` qui sert de conteneur principal, stylisé pour être visuellement distinct sur l'arrière-plan en dégradé.
- **Logos** : Des images représentant les logos de SUPINFO et VMware vSphere 7, montrant visuellement les outils ou technologies associés.
- **Formulaire** : Un formulaire HTML (`<form>`) qui envoie ses données à l'URL `/execute` via la méthode POST. Le formulaire inclut :
  - Un champ caché pour spécifier l'action (`add`) à exécuter.
  - Des champs de texte pour entrer les détails nécessaires à l'ajout d'une VM, comme le nom de la VM, le template, le datastore, le serveur vCenter, le nom d'utilisateur, le mot de passe, et le nom du client.
  - Un bouton pour soumettre le formulaire et exécuter l'action d'ajout de la VM.

### Bouton de Retour à la Maison
- Un bouton supplémentaire en bas du formulaire offre une option rapide pour revenir à la page d'accueil de l'application web, améliorant ainsi la navigation dans l'interface utilisateur.

---

# Documentation delete.html

### Structure et Métadonnées
- **DOCTYPE et Langue** : Déclare le document comme HTML5 et définit l'anglais comme langue principale.
- **Head** : Inclut la métadonnée pour l'encodage des caractères (UTF-8), le titre de la page, et des styles CSS internes pour le design.

### Styles CSS
- Le CSS définit l'apparence de la page, en utilisant un dégradé comme fond pour le `body`, et stylise le conteneur principal pour bien présenter le formulaire. Les éléments de formulaire tels que les champs de saisie (`input`) et les boutons (`button`) sont conçus pour s'intégrer harmonieusement à l'esthétique générale.

### Corps de la Page
- **Conteneur** : Utilise un `div` comme enveloppe principale pour les éléments de la page, avec des styles appliqués pour la transparence, les ombres, et le rayon de bordure pour une apparence moderne et engageante.
- **Logos** : Affiche les logos de SUPINFO et VMware vSphere 7, établissant visuellement le contexte de l'application et des technologies utilisées.
- **Formulaire de Suppression** : 
  - **Action et Méthode** : Le formulaire est configuré pour envoyer les données à l'URL `/execute` via la méthode POST. 
  - **Champs de Saisie** : Inclut des champs pour saisir l'adresse du serveur vCenter, le nom d'utilisateur, le mot de passe, et le nom de la VM à supprimer. Un champ caché définit l'action à exécuter comme `delete`.
  - **Bouton de Soumission** : Permet à l'utilisateur de soumettre le formulaire pour supprimer la VM spécifiée.

### Bouton de Retour à la Page d'Accueil
- Offre une méthode simple pour revenir à la page principale de l'application, améliorant la navigabilité et l'expérience utilisateur globale.

---

# Documentation display.html

### Structure et Métadonnées
- **DOCTYPE et Langue** : Utilise la déclaration HTML5 et spécifie l'anglais comme langue pour le contenu.
- **Head** : Inclut la métadonnée d'encodage UTF-8, le titre de la page, et des styles CSS internes.

### Styles CSS
- Le design de la page utilise un dégradé de couleurs comme arrière-plan, avec des textes en blanc pour un contraste optimal. Le conteneur principal est mis en évidence avec une couleur de fond semi-transparente, des coins arrondis, et une ombre pour créer de la profondeur.
- Les champs de saisie et les boutons sont conçus pour être cohérents avec l'esthétique générale, offrant une interface utilisateur harmonieuse.

### Corps de la Page
- **Conteneur Principal** : Un `div` qui sert d'enveloppe pour les éléments de la page, centré à l'écran pour faciliter la lecture et l'interaction.
- **Logos** : Inclut les logos de SUPINFO et VMware vSphere 7, établissant le contexte de l'application web et des technologies impliquées.
- **Formulaire d'Affichage des Informations** : 
  - **Action et Méthode** : Configuré pour envoyer les données à `/execute` via la méthode POST.
  - **Champs de Saisie** : Permet à l'utilisateur d'entrer les détails requis pour la connexion au serveur vCenter (serveur, nom d'utilisateur, mot de passe) et le nom de la VM dont les informations doivent être affichées. Un champ caché spécifie l'action comme `display`.
  - **Bouton de Soumission** : Invite l'utilisateur à soumettre le formulaire pour afficher les informations de la VM spécifiée.

### Bouton de Retour à la Page d'Accueil
- Fournit un moyen simple et rapide pour revenir à la page principale de l'application, améliorant l'expérience utilisateur par une navigation intuitive.

---

# Documentation restart.html

### Structure et Métadonnées
- **DOCTYPE et Langue** : Le document suit la spécification HTML5 et est défini pour utiliser l'anglais comme langue principale.
- **Head** : Contient la métadonnée pour l'encodage UTF-8, le titre de la page (`Restart VM`), ainsi que des styles CSS internes définissant l'apparence de la page.

### Styles CSS
- Le CSS établit un design cohérent et attrayant avec un fond en dégradé, des textes en blanc pour un contraste optimal, et un conteneur central pour le formulaire. Le formulaire et ses boutons sont stylisés pour une interaction facile et visuellement agréable.
- Des modifications spécifiques, comme l'espacement supplémentaire au-dessus des boutons et une couleur distincte pour le bouton de retour à la page d'accueil, améliorent l'expérience utilisateur.

### Corps de la Page
- **Conteneur Principal** : Un `div` qui sert de conteneur pour les éléments de la page, centré pour faciliter l'accès et l'interaction.
- **Logos** : Affiche les logos de SUPINFO et VMware vSphere 7, renforçant visuellement le contexte technologique de l'application.
- **Formulaire de Redémarrage** : 
  - **Action et Méthode** : Le formulaire est configuré pour poster les données vers `/execute` en utilisant la méthode POST.
  - **Champs de Saisie** : Des champs pour entrer l'adresse du serveur vCenter, le nom d'utilisateur, le mot de passe, et le nom de la VM à redémarrer. Un champ caché spécifie l'action comme `restart`.
  - **Bouton de Soumission** : Permet à l'utilisateur de soumettre le formulaire pour initier le redémarrage de la VM spécifiée.

### Bouton de Retour à la Page d'Accueil
- Offre une navigation facile pour revenir à la page principale de l'application, améliorant l'utilisabilité et l'expérience utilisateur générale.