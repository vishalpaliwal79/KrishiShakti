"""
KrishiShakti — SQLite Database Layer
Replaces Google Sheets. Fully offline, zero external dependencies.
"""
import sqlite3
import os
import json
from datetime import datetime, timedelta
from contextlib import contextmanager

DB_PATH = os.path.join('data', 'krishishakti.db')

# ── Connection helper ─────────────────────────────────────────────────────────
@contextmanager
def _conn():
    os.makedirs('data', exist_ok=True)
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")   # safe for concurrent reads
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

# ── Schema init ───────────────────────────────────────────────────────────────
def init_db():
    """Create all tables if they don't exist. Safe to call on every startup."""
    with _conn() as con:
        con.executescript("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp     TEXT    NOT NULL,
                soil_moisture REAL    DEFAULT 0,
                temperature   REAL    DEFAULT 0,
                humidity      REAL    DEFAULT 0,
                air_quality   REAL    DEFAULT 0,
                pm25          REAL    DEFAULT 0,
                pm10          REAL    DEFAULT 0,
                water_level   REAL    DEFAULT 0,
                tds           REAL    DEFAULT 0,
                is_valid      INTEGER DEFAULT 1
            );

            -- Migration: Mark all previous data as invalid (0) to ignore "bad" data
            UPDATE sensor_data SET is_valid = 0 WHERE is_valid = 1;

            CREATE TABLE IF NOT EXISTS device_logs (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT    NOT NULL,
                device    TEXT    NOT NULL,
                action    TEXT    NOT NULL,
                mode      TEXT    DEFAULT 'manual'
            );

            CREATE TABLE IF NOT EXISTS ai_logs (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp        TEXT    NOT NULL,
                decision_summary TEXT,
                confidence       REAL    DEFAULT 0,
                env_state        TEXT,
                raw_inputs       TEXT
            );

            CREATE TABLE IF NOT EXISTS irrigation_logs (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp    TEXT    NOT NULL,
                moisture     REAL    DEFAULT 0,
                duration_min REAL    DEFAULT 0,
                mode         TEXT    DEFAULT 'auto',
                action       TEXT    DEFAULT 'start'
            );

            CREATE TABLE IF NOT EXISTS alerts (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT    NOT NULL,
                type      TEXT    NOT NULL,
                severity  TEXT    DEFAULT 'info',
                title     TEXT    NOT NULL,
                message   TEXT,
                resolved  INTEGER DEFAULT 0
            );

            CREATE INDEX IF NOT EXISTS idx_sensor_ts    ON sensor_data(timestamp);
            CREATE INDEX IF NOT EXISTS idx_device_ts    ON device_logs(timestamp);
            CREATE INDEX IF NOT EXISTS idx_ai_ts        ON ai_logs(timestamp);
            CREATE INDEX IF NOT EXISTS idx_irrigation_ts ON irrigation_logs(timestamp);
            CREATE INDEX IF NOT EXISTS idx_alert_resolved ON alerts(resolved);
        """)
    print("✅ SQLite database ready:", DB_PATH)

# ── Sensor data ───────────────────────────────────────────────────────────────
def insert_sensor(data: dict):
    """Save one sensor reading. data is the nested sensor_data dict from app.py."""
    try:
        with _conn() as con:
            con.execute("""
                INSERT INTO sensor_data
                    (timestamp, soil_moisture, temperature, humidity,
                     air_quality, pm25, pm10, water_level, tds, is_valid)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (
                data.get('timestamp', datetime.now().isoformat()),
                data.get('fc28',   {}).get('value'),
                data.get('dht22',  {}).get('temperature'),
                data.get('dht22',  {}).get('humidity'),
                data.get('mq135',  {}).get('value'),
                data.get('pms5003',{}).get('pm25'),
                data.get('pms5003',{}).get('pm10'),
                data.get('fc28',   {}).get('value'),
                data.get('tds',    {}).get('value'),
                data.get('is_valid', 0)
            ))
    except Exception as e:
        print(f'[DB] insert_sensor error: {e}')

def get_sensor_history(limit: int = 100, hours: int = 24) -> list:
    """Return last N sensor readings within the last X hours."""
    try:
        threshold = (datetime.now() - timedelta(hours=hours)).isoformat()
        with _conn() as con:
            # Note: We fetch latest records first (DESC) then reverse to preserve UI order
            # Strict Filter: Only use data from last 24 hours AND marked as valid (is_valid=1)
            rows = con.execute("""
                SELECT * FROM sensor_data
                WHERE timestamp >= ? AND is_valid = 1
                ORDER BY id DESC LIMIT ?
            """, (threshold, limit)).fetchall()
        return [_sensor_row_to_dict(r) for r in reversed(rows)]
    except Exception as e:
        print(f'[DB] get_sensor_history error: {e}')
        return []

def _sensor_row_to_dict(row) -> dict:
    return {
        'timestamp':   row['timestamp'],
        'mq135':       row['air_quality'],
        'soil_moisture': row['soil_moisture'],
        'temperature': row['temperature'],
        'humidity':    row['humidity'],
        'pm25':        row['pm25'],
        'pm10':        row['pm10'],
        'fc28':        row['water_level'],
        'tds':         row['tds'],
    }

# ── Device logs ───────────────────────────────────────────────────────────────
def insert_device_log(device: str, action: str, mode: str = 'manual'):
    try:
        with _conn() as con:
            con.execute("""
                INSERT INTO device_logs (timestamp, device, action, mode)
                VALUES (?,?,?,?)
            """, (datetime.now().isoformat(), device, action, mode))
    except Exception as e:
        print(f'[DB] insert_device_log error: {e}')

def get_device_logs(limit: int = 50) -> list:
    try:
        with _conn() as con:
            rows = con.execute("""
                SELECT * FROM device_logs
                ORDER BY id DESC LIMIT ?
            """, (limit,)).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f'[DB] get_device_logs error: {e}')
        return []

# ── AI logs ───────────────────────────────────────────────────────────────────
def insert_ai_log(result: dict):
    try:
        explanations = result.get('explanation', [])
        summary = ' | '.join(explanations[:3]) if explanations else 'No decision'
        with _conn() as con:
            con.execute("""
                INSERT INTO ai_logs
                    (timestamp, decision_summary, confidence, env_state, raw_inputs)
                VALUES (?,?,?,?,?)
            """, (
                result.get('timestamp', datetime.now().isoformat()),
                summary,
                result.get('confidence', 0),
                result.get('env_state', ''),
                json.dumps(result.get('inputs', {})),
            ))
    except Exception as e:
        print(f'[DB] insert_ai_log error: {e}')

def get_ai_logs(limit: int = 20) -> list:
    try:
        with _conn() as con:
            rows = con.execute("""
                SELECT * FROM ai_logs
                ORDER BY id DESC LIMIT ?
            """, (limit,)).fetchall()
        result = []
        for r in rows:
            d = dict(r)
            try:
                d['raw_inputs'] = json.loads(d['raw_inputs'] or '{}')
            except Exception:
                d['raw_inputs'] = {}
            result.append(d)
        return result
    except Exception as e:
        print(f'[DB] get_ai_logs error: {e}')
        return []

# ── Irrigation logs ───────────────────────────────────────────────────────────
def insert_irrigation_log(event: dict):
    try:
        with _conn() as con:
            con.execute("""
                INSERT INTO irrigation_logs
                    (timestamp, moisture, duration_min, mode, action)
                VALUES (?,?,?,?,?)
            """, (
                event.get('timestamp', datetime.now().isoformat()),
                event.get('moisture', 0),
                event.get('duration_min', 0),
                event.get('mode', 'auto'),
                event.get('action', 'start'),
            ))
    except Exception as e:
        print(f'[DB] insert_irrigation_log error: {e}')

def get_irrigation_logs(limit: int = 50) -> list:
    try:
        with _conn() as con:
            rows = con.execute("""
                SELECT * FROM irrigation_logs
                ORDER BY id DESC LIMIT ?
            """, (limit,)).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f'[DB] get_irrigation_logs error: {e}')
        return []
# ── Alerts ────────────────────────────────────────────────────────────────────
def insert_alert(type: str, severity: str, title: str, message: str):
    """Save a new alert to the database."""
    try:
        with _conn() as con:
            con.execute("""
                INSERT INTO alerts (timestamp, type, severity, title, message, resolved)
                VALUES (?,?,?,?,?,0)
            """, (datetime.now().isoformat(), type, severity, title, message))
    except Exception as e:
        print(f'[DB] insert_alert error: {e}')

def get_active_alerts() -> list:
    """Return all unresolved alerts."""
    try:
        with _conn() as con:
            rows = con.execute("""
                SELECT * FROM alerts
                WHERE resolved = 0
                ORDER BY id DESC
            """).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f'[DB] get_active_alerts error: {e}')
        return []

def resolve_alert(alert_id: int):
    """Mark a specific alert as resolved."""
    try:
        with _conn() as con:
            con.execute("UPDATE alerts SET resolved = 1 WHERE id = ?", (alert_id,))
    except Exception as e:
        print(f'[DB] resolve_alert error: {e}')

def resolve_alerts_by_type(type: str):
    """Mark all active alerts of a certain type as resolved (Auto-Clear)."""
    try:
        with _conn() as con:
            con.execute("UPDATE alerts SET resolved = 1 WHERE type = ? AND resolved = 0", (type,))
    except Exception as e:
        print(f'[DB] resolve_alerts_by_type error: {e}')

def get_alert_summary() -> dict:
    """Return counts of different alert severities."""
    try:
        with _conn() as con:
            total = con.execute("SELECT COUNT(*) FROM alerts WHERE resolved = 0").fetchone()[0]
            critical = con.execute("SELECT COUNT(*) FROM alerts WHERE resolved = 0 AND severity = 'critical'").fetchone()[0]
            warning = con.execute("SELECT COUNT(*) FROM alerts WHERE resolved = 0 AND severity = 'warning'").fetchone()[0]
            info = con.execute("SELECT COUNT(*) FROM alerts WHERE resolved = 0 AND severity = 'info'").fetchone()[0]
            resolved_today = con.execute("SELECT COUNT(*) FROM alerts WHERE resolved = 1 AND timestamp >= ?", (datetime.now().strftime('%Y-%m-%d'),)).fetchone()[0]
        return {
            'total': total,
            'critical': critical,
            'warning': warning,
            'info': info,
            'resolved_today': resolved_today
        }
    except Exception as e:
        print(f'[DB] get_alert_summary error: {e}')
        return {'total': 0, 'critical': 0, 'warning': 0, 'info': 0, 'resolved_today': 0}
