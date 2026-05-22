#!/usr/bin/env python3
"""OLX Market Monitor — collects price snapshots for real estate and cars."""
import sqlite3, json, subprocess, os, sys
from datetime import datetime

DB_PATH = os.path.expanduser("~/olx-monitor/olx_prices.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            offer_id TEXT NOT NULL,
            price REAL,
            title TEXT,
            url TEXT,
            created_time TEXT,
            snapshot_time TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_snapshots_cat ON snapshots(category, snapshot_time);
        CREATE INDEX IF NOT EXISTS idx_snapshots_offer ON snapshots(offer_id);
    """)
    conn.commit()
    return conn

def fetch_olx(category_name, cat_ids, query="", pages=2):
    results = []
    for cat_id in cat_ids:
        for page in range(1, pages+1):
            url = f"https://www.olx.pl/api/v1/offers/?query={query}&category_id={cat_id}&page={page}&limit=40&sort_by=created_at:desc"
            r = subprocess.run(["curl", "-s", url,
                "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                "-H", "Accept: application/json",
                "--max-time", "10"], capture_output=True, text=True, timeout=15)
            try:
                data = json.loads(r.stdout)
                for item in data.get("data", []):
                    params = {p["key"]: p.get("value",{}).get("label",p.get("value",{}).get("value","")) for p in item.get("params",[])}
                    price = params.get("price","")
                    results.append({
                        "category": category_name,
                        "offer_id": str(item.get("id","")),
                        "price": price,
                        "title": item.get("title",""),
                        "url": f"https://www.olx.pl/d/oferta/{item.get('id','')}.html",
                        "created_time": (item.get("created_time","") or "")[:10]
                    })
            except:
                continue
    return results

def save(conn, offers):
    c = conn.cursor()
    now = datetime.now().isoformat()
    saved = 0
    for o in offers:
        try:
            p = float(str(o["price"]).replace(" ","").replace(",",".").replace("z\u0142","").strip())
        except:
            p = None
        try:
            c.execute("INSERT OR IGNORE INTO snapshots (category, offer_id, price, title, url, created_time, snapshot_time) VALUES (?,?,?,?,?,?,?)",
                      (o["category"], o["offer_id"], p, o["title"][:200], o["url"], o["created_time"], now))
            saved += c.rowcount
        except:
            pass
    conn.commit()
    return saved

def main():
    now = datetime.now()
    print(f"=== OLX Monitor {now.isoformat()[:19]} ===")
    conn = get_db()
    
    configs = [
        ("mieszkania_sprzedaz", [124], "mieszkanie"),
        ("domy_sprzedaz", [125, 126], "dom"),
        ("samochody_osobowe", [84], ""),
        ("samochody_osobowe", list(range(181, 195)), ""),
    ]
    
    for name, cats, q in configs:
        print(f"\n{name}...")
        offers = fetch_olx(name, cats, q, pages=3)
        saved = save(conn, offers)
        print(f"  {saved}/{len(offers)} saved")
    
    c = conn.cursor()
    c.execute("SELECT category, COUNT(DISTINCT offer_id) FROM snapshots GROUP BY category")
    print("\nTotals:")
    for r in c.fetchall():
        print(f"  {r[0]}: {r[1]}")
    conn.close()

if __name__ == "__main__":
    main()

