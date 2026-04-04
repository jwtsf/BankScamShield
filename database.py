import sqlite3

def init_db():
    conn = sqlite3.connect('scams.db')
    c = conn.cursor()
    # Create table to store every scan attempt
    c.execute('''CREATE TABLE IF NOT EXISTS scan_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  sender_id TEXT,
                  message_content TEXT,
                  risk_level TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def log_scan(sender, message, risk):
    conn = sqlite3.connect('scams.db')
    c = conn.cursor()
    c.execute("INSERT INTO scan_history (sender_id, message_content, risk_level) VALUES (?, ?, ?)",
              (sender, message, risk))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('scams.db')
    c = conn.cursor()
    c.execute("SELECT sender_id, risk_level, timestamp FROM scan_history ORDER BY timestamp DESC LIMIT 5")
    data = c.fetchall()
    conn.close()
    return data