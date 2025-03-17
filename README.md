##Pyshare

## Project Overview
This project is a lightweight, secure, and high-performance file-sharing server written in Python, designed for efficient and reliable file transfer. It provides a minimal web interface, file upload, and download functionality, and is optimized for scalability and ease of deployment.

## Features
- **File Upload & Download:** Secure and efficient file transfers.
- **HTTP/REST API Support:** RESTful endpoints for file operations.
- **Minimal Web Interface:** Simple UI for managing file uploads and downloads.

## Future Enhancements
- **Docker & Kubernetes Support:** Containerized deployment for scalability.
- **User Authentication & Access Control:** Role-based access management.
- **Database Integration:** PostgreSQL for file metadata storage.

## Configuration

### Environment Variables
To configure the app, create a `.env` file with the following content:

```
# Configuration Mode => development, testing, staging, or production
CONFIG_MODE = development
SECRET_KEY = 

# POSTGRESQL_DATABASE_URI => 'postgresql+psycopg2://user:password@host:port/database'
DEVELOPMENT_DATABASE_URL = 'postgresql+psycopg2://user:password@host:port/testdb'
TEST_DATABASE_URL        =
STAGING_DATABASE_URL     =
PRODUCTION_DATABASE_URL  =
```

## Getting Started

To run this project locally:

1. **Create a Virtual Environment:**

```bash
python -m venv venv
```

2. **Activate the Virtual Environment:**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

4. **Run the Application:**

```bash
flask run
```

Your web app will be available at `http://127.0.0.1:5000`.

## Project Status
- **Development Phase:** The project is under active development.
- **Objective:** To build a minimal, secure, and efficient file-sharing server with RESTful API support.

