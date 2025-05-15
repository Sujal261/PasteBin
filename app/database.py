import sqlite3
import shortuuid
from datetime import datetime, timedelta
from passlib.context import CryptContext
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Resolve DB path from environment (absolute from root)
ROOT_DIR = Path(__file__).resolve().parent.parent  # Go 1 level up from this file
DB_NAME = os.getenv("DB_NAME")
DB_PATH = ROOT_DIR / DB_NAME  # This is now absolute

def get_db_connection():
    """Get a new database connection"""
    return sqlite3.connect(DB_PATH)

def initialize_db():
    """Initialize the database and create tables if they don't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pastes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        user_id TEXT NOT NULL,
        url_id TEXT UNIQUE NOT NULL,
        password_hash TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP,
        is_private BOOLEAN DEFAULT FALSE
    )
    ''')
    
    conn.commit()
    conn.close()

def generate_url_id():
    """Generate a short unique URL identifier"""
    return shortuuid.uuid()[:8]

def get_password_hash(password):
    """Hash a password for storage"""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_paste(content: str, user_id: str, password: str = None, expires_after: int = None):
    """Create a new paste in the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    url_id = generate_url_id()
    expires_at = None
    password_hash = None
    
    if expires_after:
        expires_at = (datetime.now() + timedelta(minutes=expires_after)).strftime('%Y-%m-%d %H:%M:%S')
    
    if password:
        password_hash = get_password_hash(password)
    
    cursor.execute('''
    INSERT INTO pastes (content, user_id, url_id, password_hash, expires_at)
    VALUES (?, ?, ?, ?, ?)
    ''', (content, user_id, url_id, password_hash, expires_at))
    
    conn.commit()
    conn.close()
    return url_id

def get_paste(url_id: str, password: str = None):
    """Retrieve a paste from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT content, user_id, password_hash, expires_at 
    FROM pastes 
    WHERE url_id = ?
    ''', (url_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return None
    
    content, user_id, password_hash, expires_at = result
    
    # Check if expired
    if expires_at and datetime.strptime(expires_at, '%Y-%m-%d %H:%M:%S') < datetime.now():
        return {'error': 'This paste has expired'}
    
    # Check password if protected
    if password_hash:
        if not password or not verify_password(password, password_hash):
            return {'error': 'Password required or incorrect'}
    
    return {'content': content, 'user_id': user_id}

def get_paste_info(url_id: str):
    """Get paste metadata without content"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT user_id, created_at, expires_at 
    FROM pastes 
    WHERE url_id = ?
    ''', (url_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return None
    
    user_id, created_at, expires_at = result
    return {
        'user_id': user_id,
        'created_at': created_at,
        'expires_at': expires_at,
        'is_expired': expires_at and datetime.strptime(expires_at, '%Y-%m-%d %H:%M:%S') < datetime.now() or False
    }
    
#main