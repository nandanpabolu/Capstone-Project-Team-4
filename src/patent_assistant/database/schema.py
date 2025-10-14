"""
Database schema and initialization for Patent Partners Assistant.

Defines SQLite tables and provides database setup functionality.
"""

import sqlite3
from pathlib import Path
from typing import Optional

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from config.settings import settings


def create_database_schema(db_path: Optional[str] = None) -> None:
    """
    Create the database schema for the patent assistant.
    
    Args:
        db_path: Optional path to database file. Uses settings default if None.
    """
    if db_path is None:
        db_path = settings.db_path
    
    # Ensure directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Create patents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patent_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                abstract TEXT,
                publication_date DATE,
                cpc_class TEXT,
                inventor TEXT,
                assignee TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create doc_text table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doc_text (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patent_id TEXT NOT NULL,
                section TEXT NOT NULL,
                content TEXT NOT NULL,
                char_start INTEGER NOT NULL,
                char_end INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patent_id) REFERENCES patents(patent_id)
            )
        """)
        
        # Create chunks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patent_id TEXT NOT NULL,
                section TEXT NOT NULL,
                chunk_text TEXT NOT NULL,
                char_start INTEGER NOT NULL,
                char_end INTEGER NOT NULL,
                token_count INTEGER NOT NULL,
                embedding_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patent_id) REFERENCES patents(patent_id)
            )
        """)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_patents_patent_id ON patents(patent_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_doc_text_patent_id ON doc_text(patent_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_doc_text_section ON doc_text(section)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_patent_id ON chunks(patent_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_section ON chunks(section)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_embedding_id ON chunks(embedding_id)")
        
        conn.commit()
        print(f"✅ Database schema created at {db_path}")


def get_database_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Get a database connection.
    
    Args:
        db_path: Optional path to database file. Uses settings default if None.
        
    Returns:
        SQLite database connection
    """
    if db_path is None:
        db_path = settings.db_path
    
    # Ensure database exists
    create_database_schema(db_path)
    
    return sqlite3.connect(db_path)


if __name__ == "__main__":
    # Create database schema when run directly
    create_database_schema()
