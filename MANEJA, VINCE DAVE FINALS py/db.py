import sqlite3
import hashlib
from datetime import datetime

DB_FILE = "ocean.db"

def connect():
    return sqlite3.connect(DB_FILE)
# Save as diagnose_db.py in your project folder and run: python diagnose_db.py
import sqlite3, db, os
print("Using DB file:", getattr(db, "DB_FILE", None) or "db.DB_FILE not set")
db_path = os.path.abspath(getattr(db, "DB_FILE", "ocean.db"))
print("DB absolute path:", db_path)
conn = sqlite3.connect(db_path)
cur = conn.cursor()
try:
    cur.execute("PRAGMA table_info(reports)")
    print("reports table columns:", cur.fetchall())
    try:
        cur.execute("SELECT COUNT(*) FROM reports")
        print("reports row count:", cur.fetchone()[0])
    except Exception as e:
        print("COUNT query failed:", e)
    try:
        cur.execute("SELECT id, location, waste_type, description, COALESCE(date_reported, date), user_id FROM reports LIMIT 10")
        rows = cur.fetchall()
        print("sample rows (up to 10):")
        for r in rows:
            print(r)
    except Exception as e:
        print("SELECT sample failed:", e)
except Exception as e:
    print("PRAGMA failed:", e)
finally:
    conn.close()
def initialize():
    """Create tables if missing and run safe migrations for older DBs."""
    conn = connect()
    cur = conn.cursor()

    # Ensure users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # If reports table missing, create with modern schema
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        location TEXT NOT NULL,
        waste_type TEXT NOT NULL,
        description TEXT,
        date_reported TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    conn.commit()

    # Run safe migration to fix legacy schemas (e.g. reports.date NOT NULL)
    _migrate_reports_table(conn)

    conn.commit()
    conn.close()

def _migrate_reports_table(conn):
    """
    Safe migration:
    - If legacy column 'date' exists but 'date_reported' does not, rebuild reports table
      copying date -> date_reported to avoid NOT NULL constraint errors.
    - Add missing nullable columns (user_id, date_reported, created_at) when possible.
    """
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(reports)")
    cols_info = cur.fetchall()
    cols = [c[1] for c in cols_info]

    # If legacy 'date' exists and date_reported missing -> rebuild table to map date -> date_reported
    if "date" in cols and "date_reported" not in cols:
        try:
            # Create new table with desired schema
            cur.execute("""
            CREATE TABLE IF NOT EXISTS reports_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                location TEXT NOT NULL,
                waste_type TEXT NOT NULL,
                description TEXT,
                date_reported TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """)
            # Copy data mapping old 'date' -> 'date_reported'
            # For missing user_id/created_at values we preserve existing columns where possible
            # We select columns that exist in old table; use NULL/defaults for missing ones.
            # Build a SELECT with best-effort column availability
            select_cols = []
            select_cols.append("id")
            select_cols.append("NULL AS user_id") if "user_id" not in cols else select_cols.append("user_id")
            select_cols.append("location") if "location" in cols else select_cols.append("'' AS location")
            select_cols.append("waste_type") if "waste_type" in cols else select_cols.append("'' AS waste_type")
            select_cols.append("description") if "description" in cols else select_cols.append("NULL AS description")
            # map legacy date -> date_reported
            select_cols.append("date AS date_reported")
            select_cols.append("COALESCE(created_at, CURRENT_TIMESTAMP) AS created_at") if "created_at" in cols else select_cols.append("CURRENT_TIMESTAMP AS created_at")

            cur.execute(f"INSERT INTO reports_new (id, user_id, location, waste_type, description, date_reported, created_at) SELECT {', '.join(select_cols)} FROM reports")
            # Drop old table and rename
            cur.execute("DROP TABLE reports")
            cur.execute("ALTER TABLE reports_new RENAME TO reports")
            conn.commit()
        except Exception:
            # If something fails, ignore and allow later code to attempt lighter migrations
            conn.rollback()

        # refresh cols_info after rebuild
        cur.execute("PRAGMA table_info(reports)")
        cols_info = cur.fetchall()
        cols = [c[1] for c in cols_info]

    # If date_reported missing but date not present (rare), try adding column
    if "date_reported" not in cols:
        try:
            cur.execute("ALTER TABLE reports ADD COLUMN date_reported TEXT")
            conn.commit()
        except Exception:
            conn.rollback()

    # Add user_id if missing (nullable)
    if "user_id" not in cols:
        try:
            cur.execute("ALTER TABLE reports ADD COLUMN user_id INTEGER")
            conn.commit()
        except Exception:
            conn.rollback()

    # Add created_at if missing
    if "created_at" not in cols:
        try:
            cur.execute("ALTER TABLE reports ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            conn.commit()
        except Exception:
            conn.rollback()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, hash_password(password)))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def add_report(location, waste_type, description, date_reported, user_id):
    # store None for empty dates
    if not date_reported or str(date_reported).strip() == "":
        date_reported = None
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reports (user_id, location, waste_type, description, date_reported)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, location, waste_type, description, date_reported))
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_id

def get_all_reports():
    """
    Return rows in a shape main.py handles:
    (id, location, waste_type, description, date_reported, username)
    Username may be NULL/None if no user linked.
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.id,
               r.location,
               r.waste_type,
               r.description,
               COALESCE(r.date_reported, r.date) AS date_reported,
               u.username
        FROM reports r
        LEFT JOIN users u ON r.user_id = u.id
        ORDER BY COALESCE(r.created_at, r.id) DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_report(report_id):
    """
    Return a single report in a shape main.py expects:
    (id, location, waste_type, description, date_reported, username?)
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.id,
               r.location,
               r.waste_type,
               r.description,
               COALESCE(r.date_reported, r.date) AS date_reported,
               u.username
        FROM reports r
        LEFT JOIN users u ON r.user_id = u.id
        WHERE r.id = ?
    """, (report_id,))
    row = cur.fetchone()
    conn.close()
    return row

def update_report(report_id, location, waste_type, description, date_reported):
    if not date_reported or str(date_reported).strip() == "":
        date_reported = None
    conn = connect()
    cur = conn.cursor()
    # Update both date_reported and legacy date if exists to keep compatibility
    cur.execute("PRAGMA table_info(reports)")
    colnames = [c[1] for c in cur.fetchall()]
    if "date" in colnames:
        cur.execute("""
            UPDATE reports
            SET location = ?, waste_type = ?, description = ?, date_reported = ?, date = ?
            WHERE id = ?
        """, (location, waste_type, description, date_reported, date_reported, report_id))
    else:
        cur.execute("""
            UPDATE reports
            SET location = ?, waste_type = ?, description = ?, date_reported = ?
            WHERE id = ?
        """, (location, waste_type, description, date_reported, report_id))
    conn.commit()
    conn.close()

def delete_report(report_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM reports WHERE id = ?", (report_id,))
    conn.commit()
    conn.close()