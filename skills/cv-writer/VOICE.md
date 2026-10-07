# Voice

Shared by `cv-writer` and `motivational-letter`: one source for how anything
going out under the user's name should sound.

Text reads as machine-written when every line is the widest-fit choice: the
verb any CV could use, the adjective any candidate could claim, the sentence
shape any letter could hold. A human document is made of **specific** choices:
this system, this tool, this number, this reader. Every rule below is a way of
making the specific choice.

The user's own voice is in `profile.md` → *Voice profile*. Most people's
real voice is plainer and shorter than a template's, with no self-rating. A document that sounds like them is the target; one
that sounds like a recruiter template is the defect.

## Every sentence

- **Concrete object first.** Name the thing worked on: the payment API,
  the nightly build, the C# tool, the Jira defect queue. A sentence whose object
  is an abstraction (*innovation, excellence, efficiency, solutions*) has no
  fact in it.
- **Plain verbs, chosen for accuracy.** *wrote, fixed, tested, analysed, built,
  ran, maintained, migrated.* Pick the verb that describes what the hands did,
  even when it repeats. Repetition of a true verb reads human; a different
  thesaurus verb every time reads generated.
- **A number only where the profile records one.** One real number beats three
  rounded ones. Where there is no number, the concrete object carries the
  weight.
- **One thing at a time.** Three verbs or three outcomes in a row is a
  tricolon; keep the one that matters for this posting.
- **No evaluative adjectives about the user.** The facts make the case;
  *results-driven, passionate, detail-oriented, motivated* make none.

## CV bullets

- **Uneven shape.** Some bullets are a fact and a number; some are a fact alone;
  a few carry context. Bullets that all follow *Verb + task + resulting in X%*
  are a template showing through.

## CV profile paragraph / Kurzprofil

The highest-risk CV section: it is where generators default to an adjective
stack.

- **Open with what the user did, for how long, on what.** *"<n> years of
  <language> on <system> at <employer> …"*, filled from `profile.md`: a fact,
  not a self-description.
- **Say the direction plainly** where the posting is a change of lane: one
  sentence on what they are moving towards and the evidence for it.
- **Three to six short sentences**, not a block.

## Letters and covering emails

A letter is where generators *stage*: they announce a point, frame it, then
make it, and close on a moral. The user states the point and stops.

- **State, don't stage.** No run-up sentence before the fact (*"Was mich an
  dieser Stelle besonders reizt …"*, *"Your role combines exactly the two
  sides …"*), no *not X but Y* contrast, no one-line closer that sums up the
  paragraph. Delete the frame; the fact that follows it is the sentence.
- **The reason is the user's own.** It comes from what they said
  (`motivation.md`), in close to their words. An invented reason (*"Your
  mission resonates with me"*) is the most recognisable AI tell of all.
- **Tell the reader nothing they wrote.** Paraphrasing the posting or the
  company's own news back to them is research theatre, not a reason.
- **Each paragraph adds what the CV cannot.** The reader has the CV. A
  paragraph earns its place with the why: why this move, what one piece of work
  was like, what the user took from it. Restating CV bullets in prose is filler.
- **No setup and punchline.** *"X habe ich gelernt. Y nie. Das will ich
  jetzt."* is a staged contrast with a closer. Say it once, flat: *"Ich will
  Software nicht nur schreiben, sondern auch betreiben."*
- **Name a gap once.** One sentence, plainly, then the next point. No apology
  and no defence.
- **Vary the sentence openings.** A German letter in which every sentence
  starts with *Ich* reads like a list. Put the object or the time first where
  German allows it: *"Drei Jahre lang habe ich …"*, *"Seit zwei Jahren
  arbeite ich …"*.
- **Uneven paragraphs.** A two-sentence paragraph next to a five-sentence one
  reads written; four equal blocks read generated.
- **Close on the practical.** Availability, the salary if asked, and the
  invitation to talk, in plain words. A closing sentence that would fit any
  other letter is cut.

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
