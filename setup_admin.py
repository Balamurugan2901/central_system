"""
Setup script: Creates admin user (ID=1000) and seeds realistic intrusion data.
Run: .\\venv\\Scripts\\python.exe setup_admin.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sqlite3
from datetime import datetime, timedelta
import random

DB_PATH = "app/database/db.sqlite3"

def make_hash(password):
    try:
        import bcrypt
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed.decode()
    except Exception:
        pass
    try:
        from werkzeug.security import generate_password_hash
        return generate_password_hash(password, method='pbkdf2:sha256')
    except Exception:
        pass
    import hashlib
    return "sha256$" + hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# --- 1. Admin User ---
ADMIN_EMAIL = "admin@shieldx.local"
ADMIN_ID = 1000

cur.execute("SELECT id, email, role FROM users WHERE email=?", (ADMIN_EMAIL,))
existing = cur.fetchone()

if existing:
    print("[!] Admin already exists: {} (id={})".format(existing[1], existing[0]))
else:
    pwd_hash = make_hash("123")
    try:
        cur.execute(
            "INSERT INTO users (id, email, password, role, is_blocked) VALUES (?, ?, ?, ?, ?)",
            (ADMIN_ID, ADMIN_EMAIL, pwd_hash, "admin", 0)
        )
        conn.commit()
        print("[+] Admin created -> id={}, email={}, password=123".format(ADMIN_ID, ADMIN_EMAIL))
    except Exception as e:
        print("[!] Insert failed: {}".format(e))

# --- 2. Check Client ---
cur.execute("SELECT id FROM clients LIMIT 1")
client_row = cur.fetchone()
if not client_row:
    cur.execute("INSERT INTO clients (name, ip_address, created_at) VALUES (?,?,?)",
                ("Lab-PC-01", "192.168.1.100", datetime.utcnow().isoformat()))
    conn.commit()
    cur.execute("SELECT id FROM clients LIMIT 1")
    client_row = cur.fetchone()
    print("[+] Client seeded.")
client_id = client_row[0]

# --- 3. Seed Intrusion Data ---
cur.execute("SELECT COUNT(*) FROM intrusions")
existing_count = cur.fetchone()[0]

if existing_count < 30:
    print("[*] Seeding intrusion data ({} existing)...".format(existing_count))
    attack_types = ["Brute Force", "Port Scan", "DDoS", "SQL Injection",
                    "XSS Attack", "Man-in-the-Middle", "Ransomware", "Phishing"]
    actions_map = {
        "HIGH":   ["BLOCK_IP", "BLOCK_IP", "BLOCK_IP", "ALERT"],
        "MEDIUM": ["RATE_LIMIT", "ALERT", "RATE_LIMIT"],
        "LOW":    ["ALLOW", "ALLOW", "ALERT"],
    }
    src_ips = [
        "192.168.1.150", "10.0.0.45", "172.16.0.22", "45.33.32.156",
        "203.0.113.12", "198.51.100.3", "91.108.4.10", "185.220.101.5",
        "104.21.56.77", "193.32.160.143"
    ]
    now = datetime.utcnow()
    records = []
    for i in range(60):
        risk_level = random.choice(["HIGH", "HIGH", "MEDIUM", "MEDIUM", "LOW"])
        action = random.choice(actions_map[risk_level])
        risk_score = round(random.uniform(
            7.0 if risk_level == "HIGH" else (4.0 if risk_level == "MEDIUM" else 0.5),
            9.9 if risk_level == "HIGH" else (6.9 if risk_level == "MEDIUM" else 3.9)
        ), 2)
        ts = now - timedelta(days=random.randint(0,13), hours=random.randint(0,23), minutes=random.randint(0,59))
        records.append((
            random.choice(src_ips),
            round(random.uniform(100, 5000), 1),
            random.randint(0, 50),
            random.choice(attack_types),
            risk_score,
            risk_level,
            action,
            "ML engine detected {} threat".format(risk_level),
            ts.isoformat(),
            client_id
        ))

    cur.executemany(
        "INSERT INTO intrusions (src_ip, packet_rate, failed_logins, attack_type, risk_score, risk_level, action, details, timestamp, client_id) VALUES (?,?,?,?,?,?,?,?,?,?)",
        records
    )
    conn.commit()
    print("[+] Seeded {} intrusion log entries.".format(len(records)))
else:
    print("[=] Intrusion data sufficient: {} entries.".format(existing_count))

# --- 4. Seed Blocked IPs ---
cur.execute("SELECT COUNT(*) FROM blocked_ips")
blocked_count = cur.fetchone()[0]
if blocked_count == 0:
    blocked_data = [
        ("45.33.32.156", "Repeated brute force attacks", datetime.utcnow().isoformat()),
        ("185.220.101.5", "Known Tor exit node", datetime.utcnow().isoformat()),
        ("91.108.4.10",  "DDoS source IP flagged", datetime.utcnow().isoformat()),
        ("193.32.160.143", "SQL injection attempts", datetime.utcnow().isoformat()),
    ]
    cur.executemany(
        "INSERT INTO blocked_ips (ip_address, reason, created_at) VALUES (?,?,?)",
        blocked_data
    )
    conn.commit()
    print("[+] Seeded {} blocked IPs.".format(len(blocked_data)))
else:
    print("[=] Blocked IPs already exist: {}.".format(blocked_count))

# --- 5. Summary ---
cur.execute("SELECT COUNT(*) FROM intrusions")
total_intrusions = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
total_admins = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM blocked_ips")
total_blocked = cur.fetchone()[0]

print("\n--- DB Summary ---")
print("Users (admin): {}".format(total_admins))
print("Intrusions:    {}".format(total_intrusions))
print("Blocked IPs:   {}".format(total_blocked))

conn.close()

print("\n[OK] Setup complete!")
print("     Admin Login -> email: {}  |  password: 123  |  id: {}".format(ADMIN_EMAIL, ADMIN_ID))
print("     Open: dashboard/login.html in your browser")
