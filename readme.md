# This is the DreamCanvas user login/register page Intructions
This guide will help you set up and run the DreamCanvas Authentication Microservice locally.

## Step 1: Clone the Repo
```bash
git clone https://github.com/Lianyic/DreamCanvas-Auth-service.git
cd DreamCanvas-Auth-service
```

## Step 2: Create an .env file:
```bash
DATABASE_URL=mysql+pymysql://adminuser:LeilaLily?!@dreamcanvas-user-db.mysql.database.azure.com/dream_user_db
```

## Step 3: Create & Activate a Virtual Environment
```bash
python -m venv dreamvenv
dreamvenv\Scripts\activate
```

## Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 5: Apply Database Migrations
### Before running the app, ensure the database is up to date:
```bash
flask db upgrade
```

## Step 6: Run the app
```bash 
python app.py 
or 
flask run
```

# Optional:
## Build the docker image
```
docker build -t dreamcanvas-auth-service .
```

## Tag the image
```
docker tag dreamcanvas-auth-service ghcr.io/lianyic/dreamcanvas-auth-service:latest
```
## Push to GHCR
```
docker push ghcr.io/lianyic/dreamcanvas-auth-service:latest
```
## Deploy to Azure
Hope deployment successfull finger crossed (๑•̀ㅂ•́)و✧

## ACI web access URL
http://auth-services.bshtc3h3fqgkgcct.ukwest.azurecontainer.io:5000
