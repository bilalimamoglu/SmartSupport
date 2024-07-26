# src/utils/database_manager.py

import sqlite3
import json
import logging
from src.models.lead import Lead

class DatabaseManager:
    def __init__(self, db_name="data/leads.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS leads (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    contact_info TEXT,
                    source TEXT,
                    status TEXT
                )
            """)

    def add_or_update_lead(self, lead: Lead):
        with self.conn:
            self.conn.execute("""
                INSERT INTO leads (id, name, contact_info, source, status) 
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name=excluded.name,
                    contact_info=excluded.contact_info,
                    source=excluded.source,
                    status=excluded.status
            """, (lead.id, lead.name, lead.contact_info, lead.source, lead.status))

    def get_lead_by_contact_info(self, contact_info):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM leads WHERE contact_info = ?", (contact_info,))
            row = cur.fetchone()
            if row:
                return Lead.from_dict({
                    "id": row[0],
                    "name": row[1],
                    "contact_info": row[2],
                    "source": row[3],
                    "status": row[4]
                })
            return None

    def get_all_leads(self):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM leads")
            rows = cur.fetchall()
            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "contact_info": row[2],
                    "source": row[3],
                    "status": row[4]
                } for row in rows
            ]

    def initialize_db_from_file(self, file_path):
        with open(file_path, 'r') as file:
            leads_data = json.load(file)
            for lead_data in leads_data:
                lead = Lead.from_dict(lead_data)
                self.add_or_update_lead(lead)

    def verify_lead_update(self, contact_info):
        return self.get_lead_by_contact_info(contact_info)

    def log_all_leads(self):
        leads = self.get_all_leads()
        logging.info(f"All leads in DB: {leads}")
