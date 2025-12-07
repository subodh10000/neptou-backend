from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    preferences = Column(JSON)  # Stores interests/style

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    itinerary_data = Column(JSON)  # Stores the full JSON itinerary from Claude

# Create tables
Base.metadata.create_all(bind=engine)