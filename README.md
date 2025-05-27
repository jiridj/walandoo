# Walandoo

Walandoo is a demo single-page e-commerce application featuring a **React.js + TailwindCSS** frontend and a **Django REST Framework + PostgreSQL** backend.

---

## Project Structure

```
walandoo/
├── backend/   # Django REST API backend
├── frontend/  # React.js + TailwindCSS frontend
└── README.md
```

---

## Backend

- **Framework:** Django, Django REST Framework
- **Database:** PostgreSQL

### Setup

1. Create and activate a virtual environment:
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure your PostgreSQL credentials in `backend/walandoo/settings.py`.

4. Run migrations:
    ```bash
    python manage.py migrate
    ```

5. Start the development server:
    ```bash
    python manage.py runserver
    ```

---

## Frontend

- **Framework:** React.js
- **Styling:** TailwindCSS

### Setup

1. Install dependencies:
    ```bash
    cd frontend
    npm install
    ```

2. Start the development server:
    ```bash
    npm start
    ```

---

## Development Notes

- The frontend communicates with the backend via RESTful API endpoints.
- Update CORS settings in Django if accessing the API from a different domain during development.
- Environment variables and secrets should be stored in `.env` files (excluded from version control).

---

## License

This project is for demonstration and educational purposes.