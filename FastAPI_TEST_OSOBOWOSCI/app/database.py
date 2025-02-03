from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os
load_dotenv()

server = os.getenv("DB_SERVER")
port = os.getenv("DB_PORT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
driver = os.getenv("DB_DRIVER")

# DB_URL = f"mssql+pyodbc://{user}:{password}@{server}:{port}/{database}?driver={driver}&TrustServerCertificate=yes"

# DB_URL  = "postgresql://postgres:postgres@localhost:5432/postgres"
DB_URL = f"mssql+pyodbc://{user}:{password}@{server}:{port}/{database}?driver={driver}&TrustServerCertificate=yes&charset=utf8"


engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)
Base = declarative_base()


#Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()

# Function to test the connection
def test_connection():
    try:
        # Create a new session
        session = SessionLocal()
        
        # Try executing a simple query to check the connection
        result = session.execute(text("SELECT 1"))
        print(result.fetchone())
        
        # If we get here, the connection is working
        print("Connection to the database is successful.")
        
        # Close the session
        session.close()
        
    except Exception as e:
        # Print error message if connection fails
        print(f"Error: {e}")

# Run the test
# test_connection()

