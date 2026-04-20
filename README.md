# Aarohi AI

A Flask-based web application for women's health and wellness. Includes authentication, Gemini-powered chatbot, and placeholders for Period Predictor, Schemes, and Clinics.

## Project Structure

```
/
├── app.py                    # Flask app entry point
├── config.py                 # Config (DB, JWT, Gemini API key)
├── database.py               # MySQL connection (PyMySQL)
├── requirements.txt
├── schema_chat_history.sql   # Run once to create chat_history table
├── auth/
│   ├── middleware.py         # JWT decorator (jwt_required)
│   ├── routes.py             # /api/auth/register, /api/auth/login
│   └── services.py
├── chatbot/
│   ├── routes.py             # POST /api/chatbot/chat (JWT protected)
│   └── services.py           # Gemini, language detection, chat history
├── period_predictor/         # JWT protected (placeholder)
├── schemes/                  # JWT protected (placeholder)
├── clinics/                  # JWT protected (placeholder)
├── static/
│   ├── css/theme.css, auth.css, chatbot.css
│   └── js/auth.js, chatbot.js
└── templates/
    ├── base.html
    ├── login.html, register.html
    ├── dashboard.html
    └── chatbot.html
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database

Edit `config.py` and update the database credentials:

```python
DB_HOST = 'localhost'
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_NAME = 'aarohi_ai'
```

Or set them as environment variables:

```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=aarohi_ai
export SECRET_KEY=your-secret-key
```

### 3. Create MySQL Database

```sql
CREATE DATABASE aarohi_ai;
```

### 4. Create chat_history table (for chatbot)

```bash
mysql -u root -p aarohi_ai < schema_chat_history.sql
```

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Pages

- `/login` - Login page
- `/register` - Registration page
- `/dashboard` - Dashboard (requires login)
- `/chatbot` - Chatbot UI (requires login)

## API Endpoints

- `GET /api/health` - Health check endpoint
- `GET /` - API information and available endpoints

## Module Structure

Each module (`auth`, `chatbot`, `period_predictor`, etc.) follows this structure:

- `__init__.py` - Module initialization
- `routes.py` - API endpoints (Flask blueprints)
- `services.py` - Business logic and database operations

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL (cursor-based, no ORM)
- **Authentication**: JWT (to be implemented)
- **Frontend**: HTML + CSS (no React)

## Next Steps

1. Implement database schema and migrations
2. Add JWT authentication in the `auth` module
3. Implement features in each module
4. Create frontend pages extending `base.html`

## Notes

- All database operations use raw SQL queries with dictionary cursors
- The theme uses soft pink and lavender gradients for a women-friendly UI
- All modules are currently placeholders and ready for implementation
