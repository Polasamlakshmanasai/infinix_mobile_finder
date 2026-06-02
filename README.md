# Infinix API

A simple Flask web application for browsing Infinix mobile phone listings with user authentication and filter-based search.

## Features

- User signup and login with SQLite authentication
- Protected home page for authenticated users
- Search Infinix mobile devices by price range, RAM, and storage
- Mobile data served from a local Python list in `mobiles.py`
- Responsive HTML templates with static CSS and JavaScript

## Project Structure

- `main.py` - Flask application and API routes
- `mobiles.py` - Infinix mobile data list
- `create_db.py` - SQLite database table creation script
- `templates/` - HTML templates for login, signup, and home page
- `static/` - CSS and JavaScript assets

## Requirements

- Python 3.8+
- Flask
- Flask-CORS
- Werkzeug

## Setup

1. Create and activate a Python virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install flask flask-cors werkzeug
```

3. Create the database:

```powershell
python create_db.py
```

## Run the application

```powershell
python main.py
```

Open your browser at `http://127.0.0.1:5000/`.

## Usage

- Navigate to `/signup` to create a new account.
- Login at `/login`.
- Use the search filters on the home page to find Infinix phones by price, RAM, and storage.
- The `/mobiles` endpoint returns JSON results for filtered mobile listings.

## Notes

- Passwords are stored securely using hashed passwords via `werkzeug.security`.
- The app uses a local SQLite database named `auth.db`.
- The current mobile inventory is hard-coded in `mobiles.py`.
