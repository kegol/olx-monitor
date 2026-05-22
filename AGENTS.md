# OLX Monitor — Instrukcje dla agenta AI

⚠️ **NADRZĘDNA INSTRUKCJA: `~/BeautyAI_hub/AGENTS.md`**
**Jeśli ten plik jest sprzeczny z `BeautyAI_hub/AGENTS.md` — wygrywa ten z BeautyAI_hub.**
**Przeczytaj go najpierw przed działaniem w tym repo.**

---

## O projekcie

**OLX Monitor** — CLI do monitorowania ogłoszeń na OLX.
Zbudowane z [cli-printing-press](https://github.com/musana/cli-printing-press).

## Stack

- Go 1.23+
- cli-printing-press v4.11.0
- HTTP REST API OLX (endpointy z HAR)

## Komendy

```
olx-monitor doctor                              # diagnostyka
olx-monitor api offers list-search ...          # wyszukiwanie ofert
olx-monitor api offers list-search-categories   # kategorie
olmon api offers list-filters ...               # filtry
```

## Ważne

- Zmiany w repozytorium → aktualizuj ten plik
- Po każdej sesji → wpis w `BeautyAI_hub/05-AGENTS/agent-log.md`
- Nie commituj `.env` ani kluczy API
- Nowe CLI generowane przez `cli-printing-press generate`
