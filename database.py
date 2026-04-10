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
                  analysis_output TEXT,
                  timestamp DATETIME DEFAULT (datetime('now', '+8 hours')))''')
    conn.commit()
    conn.close()

def log_scan(sender, message, risk, analysis=None):
    conn = sqlite3.connect('scams.db')
    c = conn.cursor()
    c.execute("INSERT INTO scan_history (sender_id, message_content, risk_level, analysis_output, timestamp) VALUES (?, ?, ?, ?, datetime('now', '+8 hours'))",
              (sender, message, risk, analysis))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('scams.db')
    c = conn.cursor()
    c.execute("SELECT sender_id, risk_level, timestamp, message_content, analysis_output FROM scan_history ORDER BY timestamp DESC LIMIT 5")
    data = c.fetchall()
    conn.close()
    return data