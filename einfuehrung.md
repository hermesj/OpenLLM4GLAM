# Offene Sprachmodelle – eine kurze Einführung

*Zum Mitlesen während der Einführung im Workshop. Nach dem Vortrag „OpenLLMs in der Praxis" (Jürgen Hermes, 2025), aktualisiert für 2026.*

## Warum überhaupt offene Modelle?

Wer ein Sprachmodell über eine Online-Schnittstelle nutzt, gibt die Kontrolle ab:

- **über den Prozess:** Das Modell kann sich jederzeit ändern oder ganz verschwinden.
- **über den Output:** Ergebnisse sind später womöglich nicht mehr nachvollziehbar oder reproduzierbar.
- **über die Daten:** Alles, was ich hochlade – auch Digitalisate aus dem eigenen Bestand –, kann zum Trainingsmaterial werden.

Dazu kommen Abhängigkeiten von wenigen Anbietern. Offene Modelle holen einen Teil dieser Kontrolle zurück.

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
| **Beispiele** | GPT, Claude, Gemini | Qwen, Llama, Gemma, Mistral | OLMo (Ai2), Apertus (ETH/EPFL), Molmo 2-O (Ai2) |

- **Open Weights:** Die Modelldatei liegt bei mir, ich kann sie lokal betreiben und archivieren. Womit sie trainiert wurde, weiß ich nicht.
- **Truly Open:** Zusätzlich sind Trainingsdaten, Code und Dokumentation offen – das Modell lässt sich nachvollziehen und im Prinzip nachbauen.
- **Interpretierbarkeit:** Auch ein vollständig offenes Modell erklärt seine Entscheidungen nicht. Offenheit ermöglicht Forschung dazu, macht die Modelle aber nicht von sich aus durchschaubar.

Initiativen für wirklich offene Modelle: [OLMo / ATOM Project](https://atomproject.ai) (USA), [Apertus](https://www.apertus-ai.org/) (Schweiz), EuroLLM (EU-Konsortium).

## Welche Rechner für welche Modelle?

Faustregel: Bei üblicher Kompression (4-Bit-Quantisierung) braucht ein Modell grob **0,6 GB Arbeitsspeicher pro Milliarde Parameter**, plus Puffer für Bilder und Kontext. Die Anwendung ist dabei viel genügsamer als das Nachtrainieren (Finetuning).

| Ausstattung | Modellgröße | Beispiele mit Bildverarbeitung (Ollama, Download-Größe) |
|---|---|---|
| **Arbeitsplatz-PC / MacBook** (8–16 GB) | bis ca. 8B | `qwen2.5vl:3b` (3 GB) · `qwen2.5vl:7b` (6 GB) · `qwen3-vl:8b` (6 GB) · `gemma4:e4b` |
| **High-End-Arbeitsplatz** (z. B. Grafikkarte mit 16–24 GB, 64 GB RAM, oder Mac mit 64 GB) | ca. 12–32B | `gemma4:12b` (8 GB) · `gemma4:26b` (MoE, 16–19 GB) · `qwen3-vl:30b` (MoE, 20 GB) · `qwen2.5vl:32b` (21 GB) |
| **Server** (z. B. Grafikkarten mit 48–80 GB) | 70B und mehr | `qwen2.5vl:72b` (49 GB) · InternVL3-78B · `qwen3-vl:235b` (MoE, 143 GB, mehrere GPUs) · Llama 4 Maverick (MoE) |

*MoE* (Mixture of Experts) heißt: Das Modell ist groß, rechnet aber pro Schritt nur mit einem Teil davon – es braucht viel Speicher, läuft aber schneller als ein gleich großes „dichtes" Modell.

**Truly Open mit Bildverarbeitung:** die Molmo-Familie von Ai2 mit offenen Bild-Trainingsdaten. Vollständig offen bis zum Sprachmodell darunter ist **Molmo 2-O (7B)** auf OLMo-Basis; nutzbar über Hugging Face. Laut Projektseite verarbeitet auch **Apertus** ab Version 1.5 Bilder.

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
