#!/usr/bin/env python3
"""OLX Market Report - prices, trends & insights"""
import sqlite3, os, sys, statistics
from datetime import datetime, timedelta

DB = os.path.expanduser("~/olx-monitor/olx_prices.db")

def trend_report(conn, category, days=90, min_price=1000, max_price_=1e10):
    cutoff = datetime.now() - timedelta(days=days)
    c = conn.cursor()
    c.execute("""
        SELECT DATE(snapshot_time) as day, 
               COUNT(DISTINCT offer_id) as offers,
               ROUND(AVG(price), 0) as avg_price,
               ROUND(MIN(price), 0) as min_p,
               ROUND(MAX(price), 0) as max_p
        FROM snapshots 
        WHERE category=? AND price > ? AND price < ? AND snapshot_time > ?
        GROUP BY day ORDER BY day
    """, (category, min_price, max_price_, cutoff.isoformat()))
    rows = c.fetchall()
    if not rows:
        return "Brak danych"
    lines = [f"\nTrend {category} - ostatnie {days} dni:"]
    for r in rows:
        lines.append(f"  {r[0]}: {int(r[3])}-{int(r[4])} zl, avg={int(r[2])} zl ({r[1]} ofert)")
    return '\n'.join(lines)

def search_results(conn, query, category=None):
    c = conn.cursor()
    sql = "SELECT category, price, substr(title,1,60), url FROM snapshots WHERE title LIKE ?"
    params = [f"%{query}%"]
    if category:
        sql += " AND category=?"
        params.append(category)
    sql += " GROUP BY offer_id ORDER BY price LIMIT 25"
    c.execute(sql, params)
    rows = c.fetchall()
    if not rows:
        return f"Brak wynikow dla '{query}'"
    lines = [f"\nWyniki dla '{query}':"]
    prices = []
    for r in rows:
        lines.append(f"  {str(r[1]).rjust(8)} zl | {r[2][:55]}")
        lines.append(f"           | {r[3]}")
        if r[1]: prices.append(r[1])
    if prices:
        lines.append(f"\n  Srednia: {statistics.mean(prices):.0f} zl")
        lines.append(f"  Mediana: {statistics.median(prices):.0f} zl")
        lines.append(f"  Zakres: {min(prices):.0f} - {max(prices):.0f} zl")
    return '\n'.join(lines)

def market_summary(conn):
    c = conn.cursor()
    lines = ["="*60, "OLX RAPORT RYNKOWY", datetime.now().isoformat()[:19], "="*60]
    c.execute("""SELECT category, COUNT(DISTINCT offer_id), ROUND(AVG(price),0),
                        ROUND(MIN(price),0), ROUND(MAX(price),0)
                 FROM snapshots WHERE price > 1000 AND price < 10000000
                 GROUP BY category ORDER BY category""")
    for r in c.fetchall():
        lines.append(f"\n  {r[0]}")
        lines.append(f"    Ofert: {r[1]}")
        lines.append(f"    Ceny: {r[3]:,.0f} - {r[2]:,.0f} (srednia) - {r[4]:,.0f} zl")
    c.execute("SELECT COUNT(DISTINCT snapshot_time), COUNT(*) FROM snapshots")
    r = c.fetchone()
    lines.append(f"\n  Baza: {r[0]} serii, {r[1]} rekordow")
    return '\n'.join(lines).replace(',', ' ')

def main():
    conn = sqlite3.connect(DB)
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "trend" and len(sys.argv) > 2:
            d = int(sys.argv[3]) if len(sys.argv) > 3 else 90
            print(trend_report(conn, sys.argv[2], d))
        elif cmd == "search" and len(sys.argv) > 2:
            cat = sys.argv[3] if len(sys.argv) > 3 else None
            print(search_results(conn, sys.argv[2], cat))
        elif cmd == "summary":
            print(market_summary(conn))
        else:
            print("Uzycie: python3 report.py summary|trend <cat>|search <query>")
    else:
        print(market_summary(conn))
    conn.close()

if __name__ == "__main__":
    main()
