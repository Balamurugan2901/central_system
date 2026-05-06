import sqlite3
import os

dbs = ['intrusion.db', 'app/database/db.sqlite3']
for db_path in dbs:
    if os.path.exists(db_path):
        print(f'=== DB: {db_path} ===')
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cur.fetchall()]
        print('Tables:', tables)
        for t in tables:
            cur.execute(f'SELECT COUNT(*) FROM {t}')
            count = cur.fetchone()[0]
            print(f'  {t}: {count} rows')
            if t == 'users':
                cur.execute('SELECT id, email, role, is_blocked FROM users')
                rows = cur.fetchall()
                print('  Users:', rows)
            if t == 'intrusions':
                cur.execute('SELECT id, src_ip, attack_type, risk_score, risk_level, action FROM intrusions LIMIT 5')
                rows = cur.fetchall()
                print('  Sample intrusions:', rows)
            if t == 'blocked_ips':
                cur.execute('SELECT * FROM blocked_ips LIMIT 5')
                rows = cur.fetchall()
                print('  Blocked IPs:', rows)
            if t == 'clients':
                cur.execute('SELECT * FROM clients LIMIT 5')
                rows = cur.fetchall()
                print('  Clients:', rows)
        conn.close()
    else:
        print(f'DB not found: {db_path}')
