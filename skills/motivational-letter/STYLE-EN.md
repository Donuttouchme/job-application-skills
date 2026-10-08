# Cover letter — English

For English-language postings, including Swiss companies that hire in English.

## Word budget: ~350

Hard ceiling, one page. Over budget is 🔴.

## Structure

```
Sender block      name, street, PLZ Ort, phone, email
Recipient         company, contact person, address    (omit if unknown — current practice)
Date
Subject line      "Application: <Role>" + reference number if any
Salutation
Body              3–4 paragraphs
"Kind regards,"
<signature>
<typed name>
```

**No `Enclosures:` line** by default. What is attached belongs in the
covering email and in the dossier checklist, not at the foot of the letter.

## Salutation

In order of preference: **a named person** → **"Dear Hiring Team"** → never
**"To Whom It May Concern"**. Check the posting and the company site before
settling for the generic form.

## The paragraphs

Three or four, uneven in length. Aim for **200–280 words**; 350 is the ceiling,
not the target.

1. **Job-relevant story first** — lead with the *lead argument* from `fit.md`,
   told as what it was like: the situation, the people or pressure, what the
   user did and why it mattered, with the number where the Profile has one.
   Connect the opening to the user's reason only when `motivation.md` records
   that reason. Never open by announcing an application; the subject line
   already did that.
2. **What the user would bring** — connect the story's evidence to the work in
   this role without repeating CV bullets. If `fit.md` has an *acknowledge and
   defuse* row, name the gap once in this paragraph, without apology, then move
   forward. Often there is no gap sentence.
3. **Reason for the search** — place recorded personal context such as a move,
   language learning or a career change here, not in the opening. State facts
   only from their allowed sources, and present them as a reason for the search
   only when `motivation.md` records that connection. Use a company fact only
   when it genuinely is part of that recorded reason; never recite the posting
   or company news back to its author.
4. **Practicals and a specific close** — availability, salary if asked, then a
   friendly invitation to discuss the role, story or shared problem rather than
   a line that could close any application.

Each sentence must develop a reason, detail or consequence from the sentence
before it. Use plain causal, contrasting or time links where they are true; do
not join unrelated facts with a transition word.

Leave departure circumstances, explanations for unfinished work and similar
details for a conversation. The letter gives the relevant work and direction,
not an account of how a previous role ended.

## Register

Polite and personal: a well-written email to someone you respect. For Swiss
employers hiring in English, keep the restraint of the German market:
superlatives and US-style self-promotion read as noise. State what happened and
why it matters to the user.

Cap sentence complexity at the CEFR level in `profile.md`.

## Banned

Literal banned phrases for both languages, CVs and letters live in
[`scripts/banned-phrases.txt`](scripts/banned-phrases.txt), one UTF-8 phrase per
line. Run the shared check:

```sh
python scripts/check.py phrases <document.txt> --document-type letter --language en
```

The script checks literal phrases case-insensitively; it does not judge sentence
shape or repetition. These structural AI tells still need a prose review:
- tricolons — "designed, built, and shipped" three times in one letter
- "not only … but also"
- "It's not just X — it's Y"
- em-dash pile-ups
- "Furthermore" / "Moreover" opening consecutive paragraphs
- paragraphs of uniform length; real writing is uneven
