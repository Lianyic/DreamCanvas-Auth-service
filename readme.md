# DreamCanvas Authentication Microservice
This guide provides instructions to set up and run the DreamCanvas Authentication Microservice locally.

## Setup and Run Locally

### Step 1: Clone the Repo
```bash
git clone https://github.com/Lianyic/DreamCanvas-Auth-service.git
cd DreamCanvas-Auth-service
```

### Step 2: Create an .env file:
```bash
DATABASE_URL=mysql+pymysql://adminuser:LeilaLily?!@dreamcanvas-user-db.mysql.database.azure.com/dream_user_db
```

### Step 3: Create & Activate a Virtual Environment
```bash
python -m venv dreamvenv
dreamvenv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Apply Database Migrations
Before running the app, ensure the database is up to date:
```bash
flask db upgrade
```

### Step 6: Run the App
default running at http://127.0.0.1:5000
```bash 
python app/app.py
```

## Access the Deployed Service
DreamCanvas Authentication Service is automatically deployed via GitHub Actions and is accessible at:  
http://dreamcanvas-auth.ukwest.azurecontainer.io:5000/

### Check Database Connection
```
mysql -h dreamcanvas-user-db.mysql.database.azure.com -u adminuser -p --ssl-mode=REQUIRED
```
