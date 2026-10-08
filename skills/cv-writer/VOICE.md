# Voice

Shared by `cv-writer` and `motivational-letter`: one source for how anything
going out under the user's name should sound.

Text reads as machine-written when every line is the widest-fit choice: the
verb any CV could use, the adjective any candidate could claim, the sentence
shape any letter could hold. A human document is made of **specific** choices:
this system, this tool, this number, this reader. Every rule below is a way of
making the specific choice.

Before writing, read `profile.md` → *Voice profile*, including its hand-written
samples and *How this translates…* guidance. Those are the primary voice
reference and override every generic default below. A document that sounds like
the user is the target; one that sounds like a recruiter template is the defect.

## Every sentence

- **Concrete subjects and objects.** Name the thing worked on: the payment API,
  the nightly build, the C# tool, the Jira defect queue. Name the people using
  it or waiting for it, and the time, quality or operational pressure, when the
  Profile records them. A sentence made only of abstractions (*innovation,
  excellence, efficiency, solutions*) has no fact in it.
- **Plain verbs, chosen for accuracy.** *wrote, fixed, tested, analysed, built,
  ran, maintained, migrated.* Pick the verb that describes what the hands did,
  even when it repeats. Repetition of a true verb reads human; a different
  thesaurus verb every time reads generated.
- **A number only where the profile records one.** One real number beats three
  rounded ones. Where there is no number, the concrete object carries the
  weight.
- **Cause and consequence.** Connect sentences through *because, so, which
  meant, while,* or an equally plain relationship that is true. Explain the
  stakes in ordinary words: who depended on the work and what a delay, defect
  or wrong decision would affect. Never invent a causal link or consequence.
- **Connected paragraphs.** Each sentence develops something in the one before
  it: the reason, the work, the people, the pressure or the result. A transition
  earns its place by expressing that relationship, not by decorating two
  unrelated facts.
- **Varied rhythm.** Mix a short sentence with a longer explanatory one where
  the user's Voice profile supports it. A tricolon is fine when all three items
  belong together and are sourced; repeated tricolons or a row of clipped
  statements turns prose into a report.
- **No buzzwords, adjective stacks or generic self-praise.** The facts make the
  case; *results-driven, passionate, detail-oriented, motivated* make none. An
  evaluative self-description is allowed only when the Profile records it in
  the user's own words; keep its meaning and do not intensify it.
- **No invention.** Every fact, stake, person, pressure, relationship and
  outcome must be supported by the source allowed for that document.

## CV bullets

- **Uneven shape.** Some bullets are a fact and a number; some are a fact alone;
  a few carry context. Bullets that all follow *Verb + task + resulting in X%*
  are a template showing through.
- **Useful consequence.** A bullet may carry a short clause explaining why the
  work mattered when the Profile records that consequence. Keep it concrete;
  never manufacture impact to complete a pattern.

## CV profile paragraph / Kurzprofil

The highest-risk CV section: it must introduce a person, not compress the CV
into a situation report.

- Write **three to five connected first-person sentences**: `I` in English,
  `ich` in German.
- Open with a personal hook drawn from a self-description in the Profile. Then
  connect what the user built or changed to why it mattered, show how they
  worked with people, and finish with where they are heading.
- Make that direction fit the lane and acknowledge a genuine experience gap
  plainly, without apology or an unsupported title claim.
- Trace every fact and self-description to `profile.md`. The hook changes the
  voice rule, not the evidence rule.

## Letters and covering emails

A letter is where the facts become a connected account of why this move makes
sense. It should sound like the user explaining that account to one interested
person.

- **Open on the real point.** Start with the job-relevant story or the user's
  own hook, then let each sentence explain what the previous one means for this
  role. Avoid ceremonial run-ups (*"Was mich an dieser Stelle besonders reizt
  …"*, *"Your role combines exactly the two sides …"*) and *not X but Y*
  contrasts.
- **The reason is the user's own.** It comes from what they said
  (`motivation.md`), in close to their words. An invented reason (*"Your
  mission resonates with me"*) is the most recognisable AI tell of all.
- **Tell the reader nothing they wrote.** Paraphrasing the posting or the
  company's own news back to them is research theatre, not a reason.
- **Each paragraph adds what the CV cannot.** The reader has the CV. A
  paragraph earns its place with the why: why this move, what one piece of work
  was like, what the user took from it. Restating CV bullets in prose is filler.
- **Carry the thread forward.** Use cause, consequence, contrast or time to
  connect the story, contribution and reason for the search. A short sentence
  can land a point; it must not leave the next sentence to start from zero.
- **Name a gap once.** One sentence, plainly, then the next point. No apology
  and no defence.
- **Vary the sentence openings.** A German letter in which every sentence
  starts with *Ich* reads like a list. Put the object or the time first where
  German allows it: *"Drei Jahre lang habe ich …"*, *"Seit zwei Jahren
  arbeite ich …"*.
- **Uneven paragraphs.** A two-sentence paragraph next to a five-sentence one
  reads written; four equal blocks read generated.
- **Close on the practical and the personal.** Give availability and salary if
  asked, then invite a conversation in words specific to the role or story. A
  friendly final line is welcome; a stock line that fits every application is
  not.

## Punctuation and formatting

- Full stops and commas. A dash or semicolon only where the sentence genuinely
  needs it, at most a couple per document.
- Bold only where the template already bolds (positions, headings, a letter's
  subject line).

## Word list

The single shared literal banned-phrase list, including the CV additions, is
[`../motivational-letter/scripts/banned-phrases.txt`](../motivational-letter/scripts/banned-phrases.txt).
English and German entries apply to CVs and letters alike. Run it through
`python ../motivational-letter/scripts/check.py phrases <document.txt> --document-type cv --language en`
(use `de-ch` for Swiss German). The list is found beside the script, independent
of the working directory. Structural tells remain prose rules in the style
files and above; nominal chains still need a verb rather than a string of nouns.

## The read-aloud test

Read each line as if the user said it to the hiring manager across the table,
or on the phone. If they would not say it that way, rewrite it the way they
would, keeping the fact.
