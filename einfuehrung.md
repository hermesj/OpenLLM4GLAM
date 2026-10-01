# Offene Sprachmodelle – eine kurze Einführung

*Zum Mitlesen während der Einführung im Workshop. Nach dem Vortrag „OpenLLMs in der Praxis" (Jürgen Hermes, 2025), aktualisiert für 2026.*

## Warum überhaupt offene Modelle?

Wer ein Sprachmodell über eine Online-Schnittstelle nutzt, gibt die Kontrolle ab:

- **über den Prozess:** Das Modell kann sich jederzeit ändern oder ganz verschwinden.
- **über den Output:** Ergebnisse sind später womöglich nicht mehr nachvollziehbar oder reproduzierbar.
- **über die Daten:** Alles, was ich hochlade – auch Digitalisate aus dem eigenen Bestand –, kann zum Trainingsmaterial werden.

Dazu kommen Abhängigkeiten von wenigen Anbietern. Offene Modelle holen einen Teil dieser Kontrolle zurück.

Für Gedächtnisinstitutionen wiegt das besonders schwer:

- **Rechte:** Viele Bestände sind urheberrechtlich geschützt oder nur unter Auflagen nutzbar – sie dürfen nicht einfach an einen Online-Dienst gehen.
- **Personendaten:** Archivgut, Fotos und Korrespondenz enthalten oft personenbezogene Daten, für die Schutzfristen und Datenschutz gelten.
- **Langfristigkeit:** Archive, Bibliotheken und Museen planen in Jahrzehnten. Ein Arbeitsablauf, der an einem Dienst hängt, der morgen anders funktioniert oder eingestellt wird, passt dazu schlecht. Eine Modelldatei lässt sich dagegen archivieren wie andere digitale Objekte auch.

## Was heißt „offen"?

„Open" ist kein Ja/Nein, sondern ein Spektrum. Liesenfeld & Dingemanse (2024) unterscheiden drei Dimensionen:

| Dimension | Was offen sein kann |
|---|---|
| **Verfügbarkeit** | Code · Trainingsdaten · Gewichte · Daten und Gewichte des Feintunings (RLHF) · Lizenz |
| **Dokumentation** | Code · Architektur · Preprint · Paper · Datenblatt |
| **Zugriff** | Webservice · Paket zum Herunterladen · API |

**Beispiel Lizenz – zum Selbstprüfen:** Die beiden Modelle, die wir heute nutzen, stammen aus derselben Familie, haben aber verschiedene Lizenzen. `qwen2.5vl:7b` steht unter Apache 2.0, `qwen2.5vl:3b` unter der *Qwen Research License* – nur für nicht-kommerzielle Zwecke. Nachlesen im Terminal:

```
ollama show qwen2.5vl:3b --license
```

## Proprietär – Open Weights – Truly Open

| | Proprietär (Online-Frontier) | Open Weights | Truly Open |
|---|:---:|:---:|:---:|
| Wissenschaftliche Kontrolle, reproduzierbarer Prozess | ❌ | ✓ | ✓ |
| Methodische Transparenz (Trainingsdaten, Architektur) | ❌ | ❌ | ✓ |
| Datenschutz, keine externe Governance | ❌ | ✓ | ✓ |
| Interpretierbarkeit | ❌ | ❓ | ❓ |
| **Beispiele** | GPT, Claude, Gemini | Qwen, Llama, Gemma, Mistral | Olmo 3 (Ai2), Apertus (ETH/EPFL/CSCS), Molmo 2-O (Ai2) |

- **Open Weights:** Die Modelldatei liegt bei mir, ich kann sie lokal betreiben und archivieren. Womit sie trainiert wurde, weiß ich nicht.
- **Truly Open:** Zusätzlich sind Trainingsdaten, Code und Dokumentation offen – das Modell lässt sich nachvollziehen und im Prinzip nachbauen.
- **Interpretierbarkeit:** Auch ein vollständig offenes Modell erklärt seine Entscheidungen nicht. Offenheit ermöglicht Forschung dazu, macht die Modelle aber nicht von sich aus durchschaubar.

Initiativen für wirklich offene Modelle: [OLMo / ATOM Project](https://atomproject.ai) (USA), [Apertus](https://www.apertus-ai.org/) (Schweiz), EuroLLM (EU-Konsortium).

## Welche Rechner für welche Modelle?

Faustregel: Bei üblicher Kompression (4-Bit-Quantisierung) braucht ein Modell grob **0,6 GB Arbeitsspeicher pro Milliarde Parameter**, plus Puffer für Bilder und Kontext. Die Anwendung ist dabei viel genügsamer als das Nachtrainieren (Finetuning).

| Ausstattung | Modellgröße | Beispiele mit Bildverarbeitung |
|---|---|---|
| **Arbeitsplatz-PC / MacBook** (8–16 GB) | bis ca. 8B | `qwen2.5vl:3b` / `qwen2.5vl:7b` (3 / 6 GB, heute im Einsatz) · `gemma4:e4b` · **voll offen:** Molmo 2-O 7B (Ai2, auf Olmo 3) · Apertus 1.5 8B (Swiss AI) |
| **High-End-Arbeitsplatz** (z. B. Grafikkarte mit 16–24 GB, 64 GB RAM, oder Mac mit 64 GB) | ca. 12–32B | `gemma4:12b` (8 GB) · `mistral-small3.2:24b` (15 GB) · `gemma4:26b` (MoE, 16–19 GB) · `qwen3-vl:30b` (MoE, 20 GB) · *voll offen: in dieser Größe derzeit kein Bildmodell bekannt* |
| **Server** (z. B. Grafikkarten mit 48–80 GB) | 70B und mehr | **voll offen:** Apertus 1.5 70B · `qwen2.5vl:72b` (49 GB) · `llama4:scout` (MoE, 67 GB) · `llama4:maverick` (MoE, 245 GB, mehrere GPUs) |

Angaben in `code` sind direkt in Ollama verfügbar (mit Download-Größe), die voll offenen Modelle bisher nur über Hugging Face.

*MoE* (Mixture of Experts) heißt: Das Modell ist groß, rechnet aber pro Schritt nur mit einem Teil davon – es braucht viel Speicher, läuft aber schneller als ein gleich großes „dichtes" Modell.

**Truly Open mit Bildverarbeitung** gibt es bisher nur wenig: **Molmo 2-O 7B** von Ai2 baut auf dem vollständig offenen Olmo 3 auf (Bild-Trainingsdaten offen, Trainingscode angekündigt), **Apertus 1.5** (Juli 2026, 8B und 70B) verarbeitet seit dieser Version auch Bilder. Die übrigen Molmo-Modelle beruhen auf Qwen – offen sind dort nur die Bilddaten. Olmo 3 selbst (`olmo-3:7b`, `olmo-3:32b`) gibt es in Ollama, allerdings nur für Text.

**Ohne eigene Hardware:** wissenschaftliche Rechenzentren und Dienste (z. B. GWDG/KISSKI, KI:connect an Hochschulen), Hugging Face Inference Endpoints. Dann gilt aber wieder: Die Daten verlassen das Haus.

## Werkzeuge für den eigenen Rechner

| | [Ollama](https://ollama.com) | [LM Studio](https://lmstudio.ai) | [Hugging Face Transformers](https://github.com/huggingface/transformers) |
|---|---|---|---|
| Modelle | kuratierte Liste (erweiterbar) | Auswahl aus Hugging Face | Zugriff auf Tausende Modelle |
| Bedienung | App und Kommandozeile | grafische Oberfläche | Python-Programmierung |
| Einstellungen | größtenteils automatisch | per Oberfläche | durchgehend konfigurierbar |
| Schnittstelle | API | API | Bibliothek und API |
| Selbst quelloffen? | ja | App nein, kostenlos nutzbar | ja |
| Geeignet für | Einstieg, Workshops | Einstieg ohne Kommandozeile | Forschung, Entwicklung |

Heute nutzen wir **Ollama** – einfach zu installieren, quelloffen und mit einer API, über die auch unser Auswertungsskript läuft.

## Zum Weiterlesen

- Liesenfeld, A. & Dingemanse, M. (2024): Rethinking open source generative AI: Open-washing and the EU AI Act. *FAccT '24*, 1774–1787. <https://doi.org/10.1145/3630106.3659005>
- Gibney, E. (2024): Not all ‚open source' AI models are actually open: Here's a ranking. *Nature*. <https://doi.org/10.1038/d41586-024-02012-5>
- Open Source Initiative: The Open Source AI Definition. <https://opensource.org/ai>
- Balloccu, S. et al. (2024): Leak, Cheat, Repeat: Data Contamination and Evaluation Malpractices in Closed-Source LLMs. *EACL 2024*. <https://aclanthology.org/2024.eacl-long.5>
