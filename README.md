## Pyshare

## Project Overview
This project is a file-sharing server written in Python, designed for efficient and very simple file transfer. It provides a minimal web interface, file upload, download and users manegement. I'm creating this project as I was not able to find any self-hostable web-app that allowed me to share files easily over the internet.

## Features
- **File Upload & Download:** Secure and easy file transfers even with external user.
- **Minimal Web Interface:** Simple UI for managing file uploads/downloads and user management.
- **Docker & Kubernetes Support:** Containerized deployment for scalability.
- **User Authentication & Access Control:** Role-based access management.
- **Database Integration:** PostgreSQL for file metadata storage.

## Getting Started

To run this project locally:

1. **clone repo:**

```bash
git clone https://github.com/l3ox64/pyshare
cd pyshare
```

2. **create and activate VE:**

```bash
python3 -m venv venv
```

3. **activate VE:**
```bash
source venv/bin/activate
```

4. **install dependencies:**

```bash
pip install -r requirements.txt
```

5. **modify env file**
To configure the app, modify a `.env` to meet your needs:

```
# Configuration Mode => development, testing, staging, or production
CONFIG_MODE = development
SECRET_KEY = 

# POSTGRESQL_DATABASE_URI => 'postgresql+psycopg2://user:password@host:port/database'
DEVELOPMENT_DATABASE_URL = 'postgresql+psycopg2://user:password@localhost:5432/testdb'
TEST_DATABASE_URL        =
STAGING_DATABASE_URL     =
PRODUCTION_DATABASE_URL  =
```

4. **db init**

```bash
cd src
flask db init
flask db migrate
flask db upgrade
```

5. **run the application:**

```bash
flask run
```

Your web app will be available at `http://127.0.0.1:5000`.
