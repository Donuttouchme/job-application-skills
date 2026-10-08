# Motivationsschreiben — German, for the Swiss market

**Standard High German wording with Swiss orthography.** Written German in
Switzerland *is* Hochdeutsch; what differs is the spelling and the letter
layout, not the vocabulary. Layout follows **SN 010130**, not DIN 5008.

## Word budget: ~300

Hard ceiling. The sender and recipient blocks eat more of the page than an
English letter's header, so the body has less room. Over budget is 🔴.

## Swiss orthography — non-negotiable

- **No `ß`, ever.** `Grüsse`, `Strasse`, `gemäss`, `Masse`, `Fussball`. A single
  `ß` says the letter came from a German template.
- Close with **`Freundliche Grüsse`** — not `Mit freundlichen Grüßen`.
- Salary in **CHF**, annual, apostrophe as thousands separator: `CHF 95'000`.
- Phone in international form: `+41 79 123 45 67`.
- Date: `Ort, T. Monat JJJJ` with the month spelled out — never `02.09.2026`.

## Vocabulary — Hochdeutsch, not Helvetisms

The spelling is Swiss; the words are standard German. Helvetisms in a written
application read as either affected or careless.

| Do not write | Write |
|---|---|
| Salär | Gehalt |
| allfällig | eventuell, etwaig |
| Unterbruch | Unterbrechung |
| Pendenzen | offene Punkte |
| Traktanden | Tagesordnung |
| parkieren | parken |
| Natel | Mobiltelefon |
| Kader | Führungskräfte |

**One exception: mirror the posting.** If the advertisement itself asks for the
`Lohnvorstellung`, answer using *their* word. That is quoting the employer, not
choosing a regionalism, and it reads well. Default to Hochdeutsch everywhere the
posting has not set a term.

## Structure

```
Absender          name, street, PLZ Ort, phone, email
Empfänger         company (legal name from the Impressum)
                  z. H. <contact person>
                  street, PLZ Ort
Ort, Datum        right-aligned
Betreff           bold — "Bewerbung als <Rolle>" + reference number if any
Anrede
Body              3–4 paragraphs
Freundliche Grüsse
<signature>
<typed name>
```

**No `Beilagen:` line** by default. It is conventional on this market, but the
attachments are listed in the covering email anyway. If the user wants it, add
it; otherwise do not reintroduce it. A Swiss application is still a dossier: what is attached goes in
the covering email and in the dossier checklist.

## Salutation

`Sehr geehrte Frau Meier` / `Sehr geehrter Herr Meier` when a name exists — look
in the posting and the Impressum before giving up. `Sehr geehrte Damen und
Herren` only when there is genuinely no name. Never `du`.

## The paragraphs

Three or four, uneven in length. Aim for **180–250 words**; 300 is the ceiling,
not the target.

1. **Berufsrelevante Geschichte zuerst** — mit dem *lead argument* aus
   `fit.md` beginnen und erzählen, wie die Situation war: die Menschen oder
   der Druck, was der Nutzer tat und warum es wichtig war. Eine Zahl nur
   verwenden, wenn sie im Profil steht. Den Einstieg nur dann mit dem Grund des
   Nutzers verbinden, wenn `motivation.md` diesen Grund festhält. Nicht den Akt
   der Bewerbung beschreiben; dafür steht der Betreff.
2. **Was der Nutzer einbringt** — die Evidenz aus der Geschichte mit der Arbeit
   in dieser Rolle verbinden, ohne Lebenslaufpunkte nachzuerzählen. Wenn
   `fit.md` eine Zeile *acknowledge and defuse* enthält, die Lücke hier einmal
   ohne Entschuldigung nennen und dann weitergehen. Oft braucht es keinen Satz
   zur Lücke.
3. **Grund für die Suche** — erfassten persönlichen Kontext wie einen Umzug,
   das Sprachenlernen oder einen Berufswechsel hier einordnen, nicht am Anfang.
   Fakten stammen nur aus den erlaubten Quellen; als Grund für die Suche gelten
   sie nur, wenn `motivation.md` diese Verbindung festhält. Eine Unternehmens-
   tatsache nur verwenden, wenn sie wirklich Teil dieses erfassten Grundes ist;
   Stellenanzeige und Unternehmensnachrichten nicht ihren Verfassern
   nacherzählen.
4. **Praktisches und konkreter Abschluss** — Verfügbarkeit
   (`frühestmöglicher Eintrittstermin`), Gehalt falls verlangt und danach eine
   freundliche Einladung, über die Rolle, die Geschichte oder das gemeinsame
   Problem zu sprechen. Keine Schlusszeile verwenden, die zu jeder Bewerbung
   passen würde.

Jeder Satz entwickelt einen Grund, ein Detail oder eine Folge aus dem Satz
davor. Schlichte kausale, gegensätzliche oder zeitliche Verbindungen verwenden,
wenn sie stimmen; unverbundene Fakten nicht mit einem Übergangswort verkleben.

Umstände eines Austritts, Erklärungen für unfertige Arbeit und ähnliche Details
gehören ins Gespräch. Das Schreiben zeigt die relevante Arbeit und Richtung,
nicht den Ablauf am Ende einer früheren Stelle.

## Register

Polite and personal: a well-written email to someone you respect, not an
official letter to an authority. Varied sentence rhythm, active voice, `ich`
where the user did something. Swiss readers dislike American-style self-promotion and
equally dislike *Amtsdeutsch*: `bezüglich`, `diesbezüglich`, `im Rahmen von`,
`hinsichtlich`, chains of nouns. Hedging (`Ich denke, dass ich eventuell…`) is
the third failure. State what happened, say why it matters to the user, and
let it stand.

Cap sentence complexity at the CEFR level in `profile.md`. Below C1, say so
plainly in the letter (`Deutsch: B2, aktuell im Ausbau`). Recruiters here prefer
knowing to discovering it at interview.

## Banned

Literal banned phrases for both languages, CVs and letters live in
[`scripts/banned-phrases.txt`](scripts/banned-phrases.txt), one UTF-8 phrase per
line. Run the shared check:

```sh
python scripts/check.py phrases <document.txt> --document-type letter --language de-ch
```

The script checks literal phrases case-insensitively and blocks any `ß` in a
de-ch document. It does not judge sentence shape or repetition. These structural
AI tells still need a prose review:
- `nicht nur … sondern auch`
- `Darüber hinaus` opening three paragraphs in a row
- nominal style and chains of nouns where a verb would do
