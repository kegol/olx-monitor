# OLX Market Monitor — dokumentacja techniczna

## Architektura

### collect.py

Pobiera dane z OLX API v1 (REST, publiczne, bez autoryzacji).

**Mechanizm:**
1. Dla każdej kategorii → GET `https://www.olx.pl/api/v1/offers/`
2. Parsuje JSON (id, title, params.price, created_time)
3. Zapisuje do SQLite z timestampem

**Parametry:**
- `--max-time 10` per request
- User-Agent: standardowy browser
- 3 strony × 40 ofert = ~120/kategorię/cykl

### report.py — 3 tryby

| Tryb | Opis |
|------|------|
| `summary` | Średnie ceny, min/max, liczba ofert na kategorię |
| `trend <cat> [dni]` | Ceny w czasie — dzień po dniu |
| `search <query> [cat]` | Szukaj w tytułach, pokaż średnią/medianę/zakres |

### Baza SQLite

Ścieżka: `olx_prices.db`

```sql
CREATE TABLE snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    offer_id TEXT NOT NULL,
    price REAL,
    title TEXT,
    url TEXT,
    created_time TEXT,
    snapshot_time TEXT NOT NULL
);
-- indeksy
CREATE INDEX idx_snapshots_cat ON snapshots(category, snapshot_time);
CREATE INDEX idx_snapshots_offer ON snapshots(offer_id);
```

**Filtrowanie:** `INSERT OR IGNORE` — duplikaty po offer_id są odrzucane.

---

## Troubleshooting

| Problem | Rozwiązanie |
|---------|-------------|
| "0 saved" | Sprawdź czy OLX API odpowiada: `curl -s https://www.olx.pl/api/v1/offers/ \| head -c 200` |
| Brak danych w trend | Potrzebuje snapshotów z różnych dni — uruchom collect kilka razy |
| Baza rośnie | ~700KB po jednym przebiegu, ~20MB po miesiącu — można archiwizować stare snapshoty |
| Kategoria 124 daje wynajem | OLX nie ma czysto-sprzedażowej kategorii mieszkań — filtruj po cenie >1000 zł |
