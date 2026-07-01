import sqlite3
from datetime import datetime


class TicketDatabase:
    def __init__(self, db_name="tickets.db"):
        self.db_name = db_name
        self.create_table()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            issue TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            created_at TEXT
        )
        """)

        conn.commit()
        conn.close()

    def add_ticket(self, name, email, issue, priority):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO tickets
        (name, email, issue, priority, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            email,
            issue,
            priority,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

    def get_all_tickets(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM tickets
        ORDER BY id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        tickets = []

        for row in rows:
            tickets.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "issue": row[3],
                "priority": row[4],
                "status": row[5],
                "created_at": row[6]
            })

        return tickets

    def get_ticket(self, ticket_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM tickets WHERE id=?",
            (ticket_id,)
        )

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "issue": row[3],
                "priority": row[4],
                "status": row[5],
                "created_at": row[6]
            }

        return None

    def update_status(self, ticket_id, status):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE tickets
        SET status=?
        WHERE id=?
        """, (status, ticket_id))

        conn.commit()
        conn.close()

    def delete_ticket(self, ticket_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM tickets
        WHERE id=?
        """, (ticket_id,))

        conn.commit()
        conn.close()

    def search_tickets(self, keyword):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM tickets
        WHERE name LIKE ?
        OR email LIKE ?
        OR issue LIKE ?
        """, (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        ))

        rows = cursor.fetchall()
        conn.close()

        results = []

        for row in rows:
            results.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "issue": row[3],
                "priority": row[4],
                "status": row[5],
                "created_at": row[6]
            })

        return results
