# OpenLLM4GLAM

**Offene Sprachmodelle lokal ausprobieren: Bilder verschlagworten und kategorisieren**

Material für eine Barcamp-Session auf der Tagung [**„Out of Frame – 25 Jahre prometheus zwischen Struktur und Vision"**](https://prometheus-bildarchiv.de/de/tagung2026/index) von prometheus – Das verteilte digitale Bildarchiv für Forschung & Lehre, 30. September bis 2. Oktober 2026 in Köln.

> *English:* Hands-on material for a barcamp session at the prometheus conference *Out of Frame* (Cologne, 30 Sep – 2 Oct 2026), aimed at people from galleries, libraries, archives and museums (GLAM). Participants run an open-weight vision language model (Qwen2.5-VL) locally on their own laptops with [Ollama](https://ollama.com), and use it to tag and classify a small set of public-domain images. The material is in German; the setup steps below work the same in any language.

Dieses Repository enthält alles, was du für die Barcamp-Session brauchst – außer Ollama und dem Modell selbst, die du über die Links und Befehle unten herunterlädst. **Am besten installierst du beides schon vor der Session**, denn das Modell ist 3–7 GB groß. Kurzentschlossene können es aber auch den Anfang der Session nutzen, falls das WLAN einknickt, gibt es vor Ort auch USB-Sticks mit den erforderlichen Dateien.

## Was du brauchst

| | Mindestens | Empfohlen |
|---|---|---|
| Mac | macOS 14 (Sonoma) | Apple-Chip (M1 oder neuer) |
| Windows | Windows 10 (22H2), keine Administratorrechte nötig | Grafikkarte von NVIDIA oder AMD |
| Linux | x86-64, Arbeit im Terminal | |
| Arbeitsspeicher | 8 GB → Modell `qwen2.5vl:3b` | 16 GB → Modell `qwen2.5vl:7b` |
| Speicherplatz | ca. 5 GB | ca. 10 GB |

## 1 · Ollama installieren

- **Mac und Windows:** Installer von <https://ollama.com/download> laden und starten. Auf dem Mac Ollama in den Ordner »Programme« ziehen.
- **Linux:** im Terminal
  ```
  curl -fsSL https://ollama.com/install.sh | sh
  ```

Nach dem Start erscheint das Lama-Symbol in der Menüleiste (Mac) bzw. unten rechts in der Taskleiste (Windows).

## 2 · Modell herunterladen

Entweder über die graphische Benutzeroberfläche die genauen Modellnamen eingeben und eine Konversation starten (erst dann wird das Modell auch geladen) oder –
im Terminal (Mac: Programm »Terminal«, Windows: »Eingabeaufforderung« oder »PowerShell«):

```
ollama pull qwen2.5vl:3b
```

Wer 16 GB Arbeitsspeicher oder mehr hat, kann zusätzlich das größere Modell laden:

```
ollama pull qwen2.5vl:7b
```

Mit `ollama list` siehst du, welche Modelle installiert sind.

## 3 · Kontextlänge einstellen

In der Ollama-App unter **Einstellungen → Context length** mindestens **16k** wählen. Sonst bricht das Gespräch nach dem ersten Bild mit einer Fehlermeldung ab.

Unter Linux (ohne App) Ollama so starten:

```
OLLAMA_CONTEXT_LENGTH=16384 ollama serve
```

## 4 · Material herunterladen

Oben auf dieser Seite **Code → Download ZIP** klicken und das ZIP entpacken. Oder, wer mit Git arbeitet:

```
git clone https://github.com/hermesj/OpenLLM4GLAM.git
```

## 5 · Loslegen

In der Ollama-App das Modell `qwen2.5vl` auswählen, ein Bild aus dem Ordner `bilder/` ins Chatfenster ziehen und eine Frage stellen. **Für jedes Bild einen neuen Chat beginnen.**

Unter Linux wird das Bild direkt im Befehl übergeben:

```
ollama run qwen2.5vl:3b ./bilder/bild_01.jpg Beschreibe das Bild.
```

Die Prompts, mit denen wir im Workshop arbeiten, stehen in [`prompts.md`](prompts.md).

## Automatische Auswertung aller Bilder

Das Skript `bilder_auswerten.py` schickt alle Bilder an das Modell und schreibt Kategorie und Schlagwörter in eine CSV-Datei (`ergebnisse_<Datum>_<Uhrzeit>.csv`). Ollama muss dabei laufen.

- **Mac:** Doppelklick auf `bilder_auswerten.command` (falls macOS blockiert: Rechtsklick → Öffnen)
- **Windows:** Doppelklick auf `bilder_auswerten_windows.bat` – braucht [Python](https://www.python.org/downloads/windows/)
- **Linux / Terminal:** `python3 bilder_auswerten.py`

Einstellungen stehen oben im Skript: Modell (`"auto"` nimmt das größte installierte qwen2.5vl), Kategorien mit Definitionen, Katalogangaben aus `bildnachweise.csv` im Prompt. Ein bestimmtes Modell lässt sich auch beim Aufruf angeben: `python3 bilder_auswerten.py qwen2.5vl:3b`.

## Die Bilder

Zwölf gemeinfreie Bilder aus dem Art Institute of Chicago, der Elbląska Biblioteka Cyfrowa und dem Museum im Schloss Bad Pyrmont – Gemälde, Fotografien, Objekte, ein Plakat, eine Zeitung, eine gestickte Landkarte. Einige sind eindeutig einer Kategorie zuzuordnen, andere bewusst nicht. Titel, Herkunft und Lizenzen stehen in [`bildnachweise.csv`](bildnachweise.csv).

## Wenn etwas hakt

| Problem | Lösung |
|---|---|
| Fehlermeldung *exceeds the available context size* | Kontextlänge auf 16k oder mehr stellen (Schritt 3) |
| Modell taucht nicht in der Auswahl auf | Ollama ganz beenden (Lama-Symbol → Quit) und neu starten |
| Antworten kommen sehr langsam | Kein nutzbarer Grafikchip – auf `qwen2.5vl:3b` wechseln |
| Antwort auf Englisch | „Antworte auf Deutsch." ans Ende des Prompts setzen |
| Das Skript meldet *Modell … ist nicht installiert* | `ollama pull` mit dem angegebenen Namen ausführen |

## Lizenz

Texte CC BY 4.0, Skripte MIT, Bilder gemeinfrei – Details in [`LICENSE.md`](LICENSE.md).

Getestet im September 2026 mit Ollama 0.34 und qwen2.5vl (3b und 7b).
