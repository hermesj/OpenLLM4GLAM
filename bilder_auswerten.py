#!/usr/bin/env python3
"""
Schickt alle Bilder aus dem Ordner »bilder« an ein lokales Vision-Modell in Ollama
und schreibt Kategorie und Schlagwörter in eine CSV-Datei.

Voraussetzung: Die Ollama-App läuft, das Modell ist geladen (ollama pull qwen2.5vl:7b).
Nur Python-Standardbibliothek, keine Installation nötig.
"""
import base64, csv, json, os, re, sys, time, urllib.error, urllib.request
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------- Einstellungen
MODELL = "auto"    # größtes installierte qwen2.5vl; sonst genauer Name, z. B. "qwen2.5vl:3b"
DURCHLAEUFE = 1            # 2 oder 3 für den Stabilitätstest
MIT_DEFINITIONEN = False   # True = Kategorien mit Definitionen (Prompt C3)
TEMPERATUR = None          # None = Standard (bei qwen2.5vl praktisch immer gleiche Antworten); 0.8 = mehr Variation
KONTEXT = 16384            # Kontextlänge, unabhängig von der Einstellung in der App
MAX_SEKUNDEN = 180         # danach wird ein Bild übersprungen
MIT_METADATEN = False      # True = Titel, Urheber und Datierung aus bildnachweise.csv in den Prompt

KATEGORIEN = ["Porträt", "Gruppenbild", "Architektur", "Landschaft", "Objekt", "Dokument", "Sonstiges"]

DEFINITIONEN = """- Porträt: eine einzelne Person ist das Hauptmotiv.
- Gruppenbild: mehrere Personen sind das Hauptmotiv.
- Architektur: Gebäude, Gebäudeteile oder Innenräume sind das Hauptmotiv.
- Landschaft: Natur oder Außenraum ist das Hauptmotiv, Personen sind Nebensache.
- Objekt: ein einzelner Gegenstand steht im Mittelpunkt.
- Dokument: Schrift oder Text ist wesentlicher Inhalt.
- Sonstiges: nichts davon trifft zu."""

PROMPT_KATEGORIE = ("Ordne das Bild genau einer dieser Kategorien zu: " + ", ".join(KATEGORIEN) +
                    ". Antworte nur mit dem Namen der Kategorie.")
PROMPT_KATEGORIE_DEF = ("Ordne das Bild genau einer dieser Kategorien zu. "
                        "Antworte nur mit dem Namen der Kategorie.\n" + DEFINITIONEN)
PROMPT_SCHLAGWOERTER = ("Du verschlagwortest Bilder für die Suche in der Online-Sammlung eines Museums. "
                        "Nenne genau 10 Schlagwörter auf Deutsch, durch Kommas getrennt. "
                        "Nur Dinge, die im Bild zu sehen sind. Keine Wertungen, keine Vermutungen über "
                        "Künstler, Datierung oder Bedeutung. Gib nur die Schlagwörter aus.")
# ------------------------------------------------------------------------------

OLLAMA = os.environ.get("OLLAMA_URL", "http://localhost:11434")
ALIAS = {"qwen2.5vl:7b": "qwen2.5vl:latest", "qwen2.5vl:latest": "qwen2.5vl:7b"}
ORDNER = Path(__file__).resolve().parent


def frage(prompt, bild, max_tokens):
    """Eine Anfrage = ein frischer Chat. Frühere Bilder beeinflussen nichts.
    max_tokens begrenzt die Antwortlänge – kleine Modelle geraten sonst manchmal
    in Endlosschleifen und wiederholen sich immer weiter."""
    optionen = {"num_ctx": KONTEXT, "num_predict": max_tokens}
    if TEMPERATUR is not None:
        optionen["temperature"] = TEMPERATUR
    daten = json.dumps({
        "model": MODELL, "stream": False, "options": optionen,
        "messages": [{"role": "user", "content": prompt,
                      "images": [base64.b64encode(bild.read_bytes()).decode()]}],
    }).encode()
    def senden(nutzlast):
        req = urllib.request.Request(OLLAMA + "/api/chat", data=json.dumps(nutzlast).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=MAX_SEKUNDEN) as r:
            return json.loads(r.read())["message"]
    nutzlast = json.loads(daten)
    # Manche Modelle (z. B. qwen3-vl) "denken" vor der Antwort und verbrauchen dabei die
    # erlaubte Antwortlänge. Deshalb das Nachdenken abschalten. Modelle, die das nicht
    # kennen, lehnen die Option ggf. ab – dann ohne sie fragen.
    nutzlast["think"] = False
    try:
        antwort = senden(nutzlast)
    except urllib.error.HTTPError:
        del nutzlast["think"]
        antwort = senden(nutzlast)
    return antwort.get("content", "").strip()


def katalogangaben():
    """Titel, Urheber/Herkunft und Datierung je Bilddatei aus bildnachweise.csv."""
    angaben = {}
    datei = ORDNER / "bildnachweise.csv"
    if not datei.exists():
        sys.exit("MIT_METADATEN ist eingeschaltet, aber bildnachweise.csv fehlt.")
    with open(datei, encoding="utf-8-sig") as f:
        for z in csv.DictReader(f, delimiter=";"):
            angaben[z["Datei"].strip()] = (f"Katalogangaben zu diesem Bild – Titel: {z['Titel']}; "
                                           f"Urheber/Herkunft: {z['Urheber / Herkunft']}; "
                                           f"Datierung: {z['Datierung']}.\n")
    return angaben


def kategorie_aus(antwort):
    """Erste genannte Kategorie aus der Antwort ziehen – Modelle antworten nicht immer mit genau einem Wort."""
    treffer = [(m.start(), k) for k in KATEGORIEN
               for m in [re.search(k, antwort, re.IGNORECASE)] if m]
    return min(treffer)[1] if treffer else "?"


def einzeilig(text):
    return " ".join(text.split())


def main():
    global MODELL
    if len(sys.argv) > 1:             # z. B.  python3 bilder_auswerten.py qwen2.5vl:3b
        MODELL = sys.argv[1]
    # Dateien wie »._bild_01.jpg« entstehen, wenn ein Mac auf USB-Sticks schreibt – ignorieren
    bilder = sorted(b for b in (ORDNER / "bilder").glob("*.jpg") if not b.name.startswith("."))
    if not bilder:
        sys.exit("Keine Bilder im Ordner »bilder« gefunden.")
    try:
        with urllib.request.urlopen(OLLAMA + "/api/tags", timeout=5) as r:
            installiert = [m["name"] for m in json.loads(r.read()).get("models", [])]
    except Exception:
        sys.exit("Ollama ist nicht erreichbar. Läuft die Ollama-App?")
    # Groß-/Kleinschreibung ignorieren (»qwen2.5vl:3B« und »qwen2.5vl:3b« sind dasselbe)
    klein = {m.lower(): m for m in installiert}
    if MODELL.lower() in klein:
        MODELL = klein[MODELL.lower()]
    if MODELL == "auto":              # größtes installierte Qwen2.5-VL nehmen
        wahl = [klein[m] for m in ("qwen2.5vl:7b", "qwen2.5vl:latest", "qwen2.5vl:3b") if m in klein]
        if not wahl:
            sys.exit("Kein qwen2.5vl-Modell installiert.")
        MODELL = wahl[0]
    elif MODELL not in installiert:
        if ALIAS.get(MODELL.lower()) in klein:   # »latest« und »7b« sind dasselbe Modell
            MODELL = klein[ALIAS[MODELL.lower()]]
        else:
            sys.exit(f"Modell {MODELL} ist nicht installiert – erst im Terminal: ollama pull {MODELL}\n"
                     f"Installiert sind: {', '.join(installiert) or 'keine'}")

    prompt_kat = PROMPT_KATEGORIE_DEF if MIT_DEFINITIONEN else PROMPT_KATEGORIE
    variante = "mit Definitionen (C3)" if MIT_DEFINITIONEN else "ohne Definitionen (C1)"
    meta = katalogangaben() if MIT_METADATEN else {}
    if MIT_METADATEN:
        variante += " + Katalogangaben"
    modell_kurz = re.sub(r"[^A-Za-z0-9.-]+", "-", MODELL)          # qwen2.5vl:3B -> qwen2.5vl-3B
    ziel = ORDNER / f"ergebnisse_{datetime.now():%Y-%m-%d_%H%M}_{modell_kurz}.csv"
    print(f"Modell: {MODELL} · Kategorien {variante} · {DURCHLAEUFE} Durchlauf/Durchläufe")
    print(f"{len(bilder)} Bilder, das dauert je nach Rechner einige Minuten …\n")

    with open(ziel, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Bild", "Durchlauf", "Kategorie (Modell)", "Kategorie (Mensch)",
                    "Schlagwörter", "Kategorie-Antwort roh", "Modell", "Variante", "Sekunden"])
        f.flush()
        leer = 0
        for lauf in range(1, DURCHLAEUFE + 1):
            for bild in bilder:
                start = time.time()
                try:
                    vorspann = meta.get(bild.name, "")
                    roh = frage(vorspann + prompt_kat, bild, 30)
                    kat = kategorie_aus(roh)
                    tags = frage(vorspann + PROMPT_SCHLAGWOERTER, bild, 200)
                except TimeoutError:
                    roh, kat, tags = f"ABGEBROCHEN nach {MAX_SEKUNDEN} s", "?", ""
                except Exception as e:
                    if "timed out" in str(e):
                        roh, kat, tags = f"ABGEBROCHEN nach {MAX_SEKUNDEN} s", "?", ""
                    else:
                        roh, kat, tags = f"FEHLER: {e}", "?", ""
                dauer = round(time.time() - start)
                if not roh and not tags:
                    leer += 1
                w.writerow([bild.name, lauf, kat, "", einzeilig(tags), einzeilig(roh),
                            MODELL, variante, dauer])
                f.flush()
                print(f"[{lauf}] {bild.name:26} {kat:12} {einzeilig(tags)[:60]}")

    print(f"\nFertig. Ergebnisse: {ziel.name}")
    if leer == len(bilder) * DURCHLAEUFE:
        print("\nAchtung: Das Modell hat keine einzige Antwort geliefert. Vermutlich ein Modell, das vor\n"
              "der Antwort »nachdenkt« und sich nicht abschalten lässt (z. B. qwen3-vl:8b).\n"
              "Dann die Variante ohne Nachdenken nehmen, z. B.:  ollama pull qwen3-vl:8b-instruct")


if __name__ == "__main__":
    main()
