TLA+ symbols
============

A list of [TLA+](https://lamport.azurewebsites.net/tla/tla.html) symbols, which
can be rendered as a PDF or used as flashcards.
For each I show its rendered display, its ASCII notation, and its meaning if I
have learned it.

A work in progress.

Get pre-rendered flashcards
---------------------------

Install [Anki Desktop](https://ankiweb.net/). I've [shared the pre-rendered
cards on AnkiWeb](https://ankiweb.net/shared/info/493978002) and I will try to
keep them updated as I extend and correct the source file.  

Generate PDF and flashcards
---------------------------

Requires Python 3.6 or later, and pdflatex. On Mac:

```
brew cask install basictex
```

Run `all-operators.py` to generate a PDF and a CSV file. The latter
is suitable for importing into Anki as flashcards.

To create a set of flashcards from the CSV, install
[Anki Desktop](https://ankiweb.net/). On Mac you need also `basictex` and
`dvipng` to create LaTeX flashcards: 

```
brew cask install basictex
sudo tlmgr update --self; sudo tlmgr install dvipng
```

* In Anki Desktop, "Tools" -> "Manage Note Types", "Add".
* Choose "Add: Basic (and reversed card)".
* Name the new note type "TLA+", click "OK".
* Highlight the new note type and click "Fields...". Add fields "Rendered TLA+", "ASCII", and "Meaning". Click "Close".
* Highlight the new note type and click "Cards...". 
* In the "Front Template" area put:
```
{{Rendered TLA+}}
```
* In the "Back Template" area put:
```
{{Meaning}}

<hr id=answer>

{{ASCII}}
``` 
* Leave the "Styling" area as-is. Click "Close". Close the "Note Types" dialog.
* In the main Anki window, "Import File".
* Choose `all-operators.csv`.
* In the "Import" dialog choose "Type: TLA+". Ensure the "Field mapping" shows the proper order: "Rendered TLA+", "ASCII", "Meaning".
* Click "Import".

FAQ
---

## What about the other lists of TLA+ symbols?

In "Specifying Systems", the table of ASCII representations and the set of
symbols shown in the book's index are differently incomplete, and the same goes
for the symbols in the TLA+ Toolkit's help. In this project I try to include all 
symbols I expect to encounter.
