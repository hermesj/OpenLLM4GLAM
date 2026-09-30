# Prompts

Die Prompts bauen aufeinander auf: erst naiv, dann mit Zweck, dann mit kontrolliertem Vokabular. Probiere sie in dieser Reihenfolge aus – am besten mit demselben Bild – und vergleiche, was sich ändert.

**Tipps**

- Für jedes Bild einen **neuen Chat** beginnen, sonst beeinflussen frühere Bilder die Antwort.
- Antwortet das Modell auf Englisch: „Antworte auf Deutsch." ans Ende setzen.

## Stufe 1 – Ausgangspunkt

> Beschreibe das Bild.

> Beschreibe das Bild in 10 Stichwörtern.

*Zum Nachdenken:* Wofür könnte man diese Antworten verwenden? Woran würdest du erkennen, ob sie gut sind?

## Stufe 2 – Schlagwörter mit Zweck

> Du verschlagwortest Bilder für die Suche in der Online-Sammlung eines Museums. Nenne genau 10 Schlagwörter auf Deutsch, durch Kommas getrennt. Nur Dinge, die im Bild zu sehen sind. Keine Wertungen, keine Vermutungen über Künstler, Datierung oder Bedeutung. Gib nur die Schlagwörter aus.

*Auswerten:* Jedes Schlagwort mit ✓ (passt), ~ (vage) oder ✗ (nicht im Bild) markieren. Hält sich das Modell an die Vorgaben?

## Stufe 3 – Kategorisierung mit kontrolliertem Vokabular

Kategorien: **Porträt · Gruppenbild · Architektur · Landschaft · Objekt · Dokument · Sonstiges**

Ordne die Bilder zuerst selbst zu – dann das Modell:

> Ordne das Bild genau einer dieser Kategorien zu: Porträt, Gruppenbild, Architektur, Landschaft, Objekt, Dokument, Sonstiges. Antworte nur mit dem Namen der Kategorie.

Mit Begründung:

> Ordne das Bild genau einer dieser Kategorien zu: Porträt, Gruppenbild, Architektur, Landschaft, Objekt, Dokument, Sonstiges. Antworte in der Form: *Kategorie: … – Begründung: …* (ein Satz).

Mit Definitionen – also mit einer kleinen Erschließungsrichtlinie:

> Ordne das Bild genau einer dieser Kategorien zu. Antworte nur mit dem Namen der Kategorie.
> - Porträt: eine einzelne Person ist das Hauptmotiv.
> - Gruppenbild: mehrere Personen sind das Hauptmotiv.
> - Architektur: Gebäude, Gebäudeteile oder Innenräume sind das Hauptmotiv.
> - Landschaft: Natur oder Außenraum ist das Hauptmotiv, Personen sind Nebensache.
> - Objekt: ein einzelner Gegenstand steht im Mittelpunkt.
> - Dokument: Schrift oder Text ist wesentlicher Inhalt.
> - Sonstiges: nichts davon trifft zu.

*Zum Nachdenken:* Wo sind sich Mensch und Modell einig, wo nicht? Bei welchen Bildern wart ihr euch untereinander uneinig? Was ändern die Definitionen?

## Variante – mit Katalogangaben

Titel, Urheber und Datierung stehen in [`bildnachweise.csv`](bildnachweise.csv). Stelle sie einem der Prompts oben voran, zum Beispiel:

> Katalogangaben zu diesem Bild – Titel: …; Urheber/Herkunft: …; Datierung: … .
> *(danach der Prompt aus Stufe 2 oder 3)*

*Zum Nachdenken:* Werden die Ergebnisse besser – oder übernimmt das Modell nur, was im Titel steht?

## Stufe 4 – Alternativtext

> Schreibe einen Alternativtext für dieses Bild in der Online-Sammlung eines Museums. Deutsch, höchstens zwei Sätze. Beschreibe nur, was sichtbar ist. Keine Wertungen, keine Deutung. Beginne nicht mit „Das Bild zeigt".

## Ausblick – ein kleiner Katalogdatensatz

> Erstelle für dieses Bild einen kurzen Katalogdatensatz mit genau diesen Feldern: Kategorie (eine aus: Porträt, Gruppenbild, Architektur, Landschaft, Objekt, Dokument, Sonstiges), Schlagwörter (5, durch Kommas getrennt), Alternativtext (ein Satz). Deutsch. Keine weiteren Angaben.

*Zum Nachdenken:* Welches dieser Felder würdest du ungeprüft übernehmen, welches nur als Vorschlag für eine menschliche Durchsicht?
