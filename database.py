import sqlite3
import logging
from datetime import datetime, date, time
from typing import List, Optional, Dict, Any
import json

logger = logging.getLogger(__name__)

class EventDatabase:
    def __init__(self, db_path: str = "eventecho.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the database with events table only"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Single events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_username TEXT NOT NULL,
                    event TEXT NOT NULL,
                    date DATE NOT NULL,
                    time TIME
                )
            ''')
            
            # Index for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_username_date ON events(telegram_username, date)')
            
            conn.commit()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
        finally:
            conn.close()

    def add_event(self, username: str, event: str, date: str, time: str = None) -> int:
        """Add a new event and return the event ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO events (telegram_username, event, date, time)
                VALUES (?, ?, ?, ?)
            ''', (username, event, date, time))
            
            event_id = cursor.lastrowid
            conn.commit()
            
            logger.info(f"Added event {event_id} for user {username}: {event}")
            return event_id
            
        except Exception as e:
            logger.error(f"Error adding event: {e}")
            raise
        finally:
            conn.close()


    def get_upcoming_events(self, username: str) -> List[Dict[str, Any]]:
        """Get all upcoming events for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, event, date, time
                FROM events
                WHERE telegram_username = ? AND date >= date('now')
                ORDER BY date, time
            ''', (username,))
            
            events = []
            for row in cursor.fetchall():
                events.append({
                    'id': row[0],
                    'event': row[1],
                    'date': row[2],
                    'time': row[3]
                })
            
            return events
            
        except Exception as e:
            logger.error(f"Error getting upcoming events: {e}")
            return []
        finally:
            conn.close()

    def clear_all_events(self, username: str) -> bool:
        """Delete all events for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM events
                WHERE telegram_username = ?
            ''', (username,))
            
            deleted_count = cursor.rowcount
            conn.commit()
            
            logger.info(f"Cleared {deleted_count} events for user {username}")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing events: {e}")
            return False
        finally:
            conn.close()


db = EventDatabase()