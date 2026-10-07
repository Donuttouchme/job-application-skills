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

1. **Why** — the user's reason, from `motivation.md`, in a sentence or two. Use
   a company fact only when it genuinely *is* the reason; never recite the
   posting or the company's news back to them. Never open by announcing that you
   are applying; the subject line already did that.
2. **One story** — the *lead argument* from `fit.md`, told as what it was like:
   the situation, what the user did, what they took from it, with the number
   where the profile has one. Skip what the CV says.
3. **The gap** — only if `fit.md` has an *acknowledge and defuse* row: one
   sentence, then move on. Often this paragraph does not exist.
4. **Close** — availability, salary if asked, an invitation to talk.

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
