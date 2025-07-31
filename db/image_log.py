import sqlite3

class DBManager:
    def __init__(self, db_path="players.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                team TEXT,
                number INTEGER
            )
        ''')
        self.conn.commit()

    def insert_player(self, name, team, number):
        self.cursor.execute(
            'INSERT INTO players (name, team, number) VALUES (?, ?, ?)',
            (name, team, number)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()
