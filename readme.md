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
dreamvenv\Scripts\activate  # Windows
source dreamvenv/bin/activate  # macOS/Linux
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
## Step 7: Push changes to github(auto deployment to ACI)
```bash 
git add .
git commit -m "Your commit message"
git push origin master
```

# Auto Deployed to Github once pushed, available at URL:
## ACI web access URL
http://dreamcanvas-auth.ukwest.azurecontainer.io:5000/

## Check database
```
mysql -h dreamcanvas-user-db.mysql.database.azure.com -u adminuser -p --ssl-mode=REQUIRED
```

## Local Docker Run Step

## Build the docker image
```
docker build -t dreamcanvas-auth-service .
```

## Run the container locally
```
docker run -p 5000:5000 --env-file .env dreamcanvas-auth-service
```
