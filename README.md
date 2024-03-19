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

# Documentation d'installation Docker pour une application Flask avec PowerShell et VMware PowerCLI

Cette documentation guide à travers les étapes d'installation et de déploiement d'une application Flask qui utilise PowerShell et VMware PowerCLI sur une machine locale à l'aide de Docker.


## 1. Création du Dockerfile

Le `Dockerfile` suivant construit une image contenant PowerShell, VMware PowerCLI, Python, et Flask. Commencez par créer un fichier nommé `Dockerfile` sans extension dans le répertoire de votre projet et y insérer le contenu suivant :

```Dockerfile
# Utiliser une image de base avec PowerShell
FROM mcr.microsoft.com/powershell:latest

# Installer Python et pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Installer VMware PowerCLI
RUN pwsh -Command "Set-PSRepository -Name PSGallery -InstallationPolicy Trusted; Install-Module -Name VMware.PowerCLI -Scope AllUsers -Confirm:$false"

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier l'application Flask dans le conteneur
COPY . /app

# Installer les dépendances Python
RUN pip3 install Flask

# Exposer le port sur lequel l'application fonctionne
EXPOSE 5000

# Commande pour exécuter l'application
CMD [ "python3", "app.py" ]
```

## 2. Application Flask

Assurez-vous que votre application Flask (`app.py`) et toutes ses dépendances (par exemple, les templates HTML et les scripts PowerShell qu'elle appelle) se trouvent dans le même répertoire que votre `Dockerfile`. Cette structure de répertoire garantit que tout est copié dans l'image Docker.

## 3. Construction et Exécution du Conteneur Docker

Après avoir créé votre `Dockerfile`, construisez l'image Docker en exécutant la commande suivante dans le même répertoire que votre `Dockerfile` :

```bash
docker build -t flask-powercli-app .
```

Une fois l'image construite, vous pouvez exécuter un conteneur à partir de cette image avec :

```bash
docker run -p 5000:5000 flask-powercli-app
```

Cette commande mappe le port 5000 du conteneur sur le port 5000 de votre hôte, vous permettant d'accéder à l'application Flask en naviguant vers `http://localhost:5000` dans un navigateur web.