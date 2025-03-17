## Pyshare

## Project Overview
This project is a file-sharing server written in Python, designed for efficient and reliable file transfer. It provides a minimal web interface, file upload, download and users manegement

## Features
- **File Upload & Download:** Secure and efficient file transfers.
- **Minimal Web Interface:** Simple UI for managing file uploads and downloads.

## Future Enhancements
- **Docker & Kubernetes Support:** Containerized deployment for scalability.
- **User Authentication & Access Control:** Role-based access management.
- **Database Integration:** PostgreSQL for file metadata storage.

## Getting Started

To run this project locally:

1. **clone repo:**

```bash
git clone https://github.com/l3ox64/pyshare
```

2. **create and activate VE:**

```bash
python3 -m venv pyshare
```

3. **activate VE:**
```bash
cd pyshare
source bin/activate
```

4. **install dependencies:**

```bash
pip install -r requirements.txt
cd src
```

5. **create env file**
To configure the app, create a `.env` file in src folder:

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
flask db init
flask db migrate
flask db upgrade
```

5. **run the application:**

```bash
flask run
```

Your web app will be available at `http://127.0.0.1:5000`.
