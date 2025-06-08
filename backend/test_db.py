from database import engine
from sqlalchemy import text

def test_connection():
    try:
        # Try to connect and execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful!")
            return True
    except Exception as e:
        print("Failed to connect to the database.")
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_connection() 