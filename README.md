# saga

Saga is a document management system for writing.

The goal is to write in Markdown and use saga to generate a variety of document formats adhering to the [Standard Manuscript Format](https://www.shunn.net/format/story.html).


## Formats

The input format is always Markdown. Saga uses _pandoc_ to transform this into **RTF**, which can then be converted to a variety of formats, such as docx, pdf, epub, and html.

## Targets

The `saga` command has a number of targets:
- new [novel, short, script, etc]
- compile [draft, outline, research]
- stats (word count)
- grammar (run some kind of grammar/spellcheck tool?)

### Stats

Word count by Draft, Outline, and Research. Done.

Word frequency

Longest word

Reading time:

    If the average page has 250–300 words, then the word count for a 100-page book totals 25,000–30,000. By reading 300 words per minute, it will take you 83–100 minutes to read this book. -- Dr. Google

We should be able to determine the average reading level of the book. Somehow. That will give us the words per minute. We can then calculate, based on the draft length, the average reading time.


## New Project

```bash
saga new novel foo
cd novels/foo
saga compile draft
```

### Templates

Templates allow the customization of a type of writing, but must follow the same folder structure:
- Draft
- Outline
- Research

The contents of those folders can be customized for the template, though.

Saga will look for these folders when compiling manuscripts.

## Drafts

In the Drafts folder, folders are treated as chapters and individual Markdown as scenes.

This would be formatted as three sequential scenes:

    Drafts/01 - A Foo.md
    Drafts/02 - A Bar.md
    Drafts/03 - A Foo Bar.md

This would be formatted as a single chapter with three scenes:

    Drafts/Chapter 1/01 - A Foo.md
    Drafts/Chapter 1/02 - A Bar.md
    Drafts/Chapter 1/03 - A Foo Bar.md

A scene break will automatically be inserted between scenes.

## Compile

Compile the manuscript(s) into a single document and produce a variety of formats


## TODO
- Make font type and size customizable
- Better formatting of folder names (acts/chapters)
- Configuration: A list of files to ignore during compilation (i.e., 0.md)
