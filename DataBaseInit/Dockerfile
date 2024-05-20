# Utilisez une image de base Python
FROM python:3.11

# Définissez le répertoire de travail
WORKDIR /app

# Copier vos fichiers de projet
COPY . /app

# Installer les dépendances
RUN pip install -r requirements.txt

# Commande pour lancer votre script Python
CMD ["python", "db_config.py"]
