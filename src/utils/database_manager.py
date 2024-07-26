import sqlite3
from src.models.lead import Lead

class DatabaseManager:
    def __init__(self, db_name="leads.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS leads (
            id TEXT PRIMARY KEY,
            name TEXT,
            contact_info TEXT,
            source TEXT,
            status TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_or_update_lead(self, lead: Lead):
        query = """
        INSERT INTO leads (id, name, contact_info, source, status)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name=excluded.name,
            contact_info=excluded.contact_info,
            source=excluded.source,
            status=excluded.status
        """
        self.conn.execute(query, (lead.id, lead.name, lead.contact_info, lead.source, lead.status))
        self.conn.commit()

    def get_lead_by_contact_info(self, contact_info):
        query = "SELECT * FROM leads WHERE contact_info = ?"
        cursor = self.conn.execute(query, (contact_info,))
        row = cursor.fetchone()
        if row:
            return Lead(id=row[0], name=row[1], contact_info=row[2], source=row[3], status=row[4])
        return None
