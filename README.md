# Casino Machine Tracker

A web application for tracking casino machine maintenance and status. Built with FastAPI backend and React frontend.

## Features

- User authentication
- Track machine status (Down, In Progress, Fixed)
- Add new machines
- Update machine status
- View machine details including vendor and maintenance history

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Python 3.8+

### Frontend
- React
- TypeScript
- Tailwind CSS
- React Query
- Axios

## Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python init_db.py
```

4. Start the backend server:
```bash
uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

## Default Login

- Username: admin
- Password: admin123

## API Documentation

Once the backend is running, visit http://localhost:8001/docs for the interactive API documentation.

## Project Structure

```
.
├── backend/
│   ├── models.py      # Database models
│   ├── schemas.py     # Pydantic schemas
│   ├── main.py        # FastAPI application
│   ├── auth.py        # Authentication logic
│   └── database.py    # Database configuration
└── frontend/
    ├── src/
    │   ├── components/    # React components
    │   ├── api/          # API client
    │   └── types.ts      # TypeScript types
    └── public/
```
