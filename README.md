# OLX Market Monitor 🏠🏎️ 💰

**Śledź ceny na OLX w czasie — nieruchomości, samochody, alerty, trendy.**

> "Kupuj tanio, sprzedawaj drogo — ale najpierw wiedz, co jest drogie."

Snapshotuje oferty z OLX co 6h i daje Ci obraz rynku zamiast zgadywania.

---

## Szybki start

```bash
# Zbierz dane
python3 collect.py

# Raport rynkowy
python3 report.py summary

# Szukaj konkretnego modelu
python3 report.py search 'bmw'
python3 report.py search 'mieszkanie 2 pokoje'

# Trend z ostatnich 30 dni
python3 report.py trend samochody_osobowe 30
```

**Wymagania:** Python 3, curl (standardowo na każdym VPS/Linux)

---

## Jak działa

```
collect.py ──→ SQLite (snapshoty cen) ──→ report.py
                                              │
                                    ┌─────────┼─────────┐
                                    │         │         │
                                 summary   trend     search
```

- `collect.py` — pobiera oferty z publicznego API OLX (bez auth)
- SQLite — zapisuje snapshot z timestampem
- `report.py` — 3 tryby raportowania

---

## Komendy

### `collect.py` — zbieranie danych

```bash
# Pełny sync
python3 collect.py

# Output:
#   mieszkania_sprzedaz... 12/16 saved
#   domy_sprzedaz...       38/42 saved
#   samochody_osobowe...  600/749 saved
```

### `report.py` — raporty

```bash
# Podsumowanie rynku
python3 report.py summary

# Trend cen (domyślnie 90 dni)
python3 report.py trend domy_sprzedaz 30

# Szukaj w ofertach
python3 report.py search 'volkswagen'
python3 report.py search '3 pokoje' mieszkania_sprzedaz
```

**Przykład search:**

```
Wyniki dla 'bmw':
    4900 zl | BMW 320d E46 2004r. Diesla super stan
    ...
   12900 zl | BMW X5 3.0d 2008r.

  Srednia: 7890 zl
  Mediana: 7200 zl
  Zakres: 4900 - 12900 zl
```

---

## Automatyczne snapshoty (cron)

```bash
# Co 6h
0 */6 * * * cd /opt/data/home/olx-monitor && python3 collect.py >> collect.log 2>&1
```

Po tygodniu masz ~28 snapshotów na kategorię — dane do analizy trendów.

---

## Zbierane kategorie

| Kategoria | ID OLX | Zakres cen |
|-----------|--------|------------|
| Mieszkania sprzedaż | 124 | 23k - 5.3M zł |
| Domy sprzedaż | 125, 126 | 23k - 5.3M zł |
| Samochody osobowe | 84 + brand IDs (181-194) | 1.5k - 429k zł |

**Brand IDs:** Alfa(181), Audi(182), BMW(183), Citroen(184), Fiat(185), Ford(186), Honda(187), Hyundai(188), Kia(189), Mazda(190), Mercedes(191), Mitsubishi(192), Nissan(193), Opel(194)

---

## Roadmap

- [ ] Naprawa Otodom (otodom-pp-cli sync)
- [ ] Lepsze kategorie OLX (mieszkania mają za dużo szumu)
- [ ] Alerty — "cena spadła o X%"
- [ ] Dashboard web z wykresami
- [ ] Model biznesowy: Free / Pro (29 zł) / Dealer (99 zł)
- [ ] Otodom + Gratka + OtoMoto

---

*Część ekosystemu [BeautyAI](https://beautyai.pl) | Dawid Skwira*
