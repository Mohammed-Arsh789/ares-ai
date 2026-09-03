import sqlite3
from datetime import datetime

from core.config import MEMORY_DB


class Memory:

    def __init__(self):
        self.connection = sqlite3.connect(MEMORY_DB)
        self._create_tables()

    def _create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        self.connection.commit()

    def remember(self, category, content):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO memories
            (category, content, created_at)
            VALUES (?, ?, ?)
            """,
            (
                category,
                content,
                datetime.now().isoformat()
            )
        )

        self.connection.commit()

    def search(self, query="", limit=10):

        cursor = self.connection.cursor()

        if query:

            cursor.execute(
                """
                SELECT category, content, created_at
                FROM memories
                WHERE content LIKE ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (f"%{query}%", limit)
            )

        else:

            cursor.execute(
                """
                SELECT category, content, created_at
                FROM memories
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,)
            )

        return cursor.fetchall()

    def close(self):
        self.connection.close()