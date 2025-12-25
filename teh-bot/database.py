import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id TEXT UNIQUE,
                role TEXT CHECK(role IN ('student', 'teacher'))
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS homeworks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                deadline TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS lectures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                date TEXT
            )
        ''')
        self.conn.commit()

    def add_homework(self, title, description, deadline):
        self.cursor.execute('INSERT INTO homeworks(title, description, deadline) VALUES(?, ?, ?)', (title, description, deadline))
        self.conn.commit()

    def get_homeworks(self):
        return self.cursor.execute('SELECT * FROM homeworks').fetchall()

    def delete_homework(self, hw_id):
        self.cursor.execute('DELETE FROM homeworks WHERE id=?', (hw_id,))
        self.conn.commit()

    def update_homework(self, hw_id, title=None, description=None, deadline=None):
        updates = {k:v for k,v in {'title': title, 'description': description, 'deadline': deadline}.items() if v}
        set_clause = ', '.join([f'{col}=?' for col in updates.keys()])
        values = list(updates.values()) + [hw_id]
        self.cursor.execute(f'UPDATE homeworks SET {set_clause} WHERE id=?', tuple(values))
        self.conn.commit()

    def add_lecture(self, title, content, date):
        self.cursor.execute('INSERT INTO lectures(title, content, date) VALUES(?, ?, ?)', (title, content, date))
        self.conn.commit()

    def get_lectures(self):
        return self.cursor.execute('SELECT * FROM lectures').fetchall()

    def delete_lecture(self, lecture_id):
        self.cursor.execute('DELETE FROM lectures WHERE id=?', (lecture_id,))
        self.conn.commit()

    def register_user(self, telegram_id, role):
        self.cursor.execute('INSERT OR IGNORE INTO users(telegram_id, role) VALUES(?, ?)', (telegram_id, role))
        self.conn.commit()

db = Database('university_bot.db')