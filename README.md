# saga

Saga is a document management system for writing.

The goal is to write in Markdown and use saga to generate a variety of document formats adhering to the [Standard Manuscript Format](https://www.shunn.net/format/story.html).


## Formats

The input format is always Markdown. Saga uses _pandoc_ to transform this into **RTF**, which can then be converted to a variety of formats, such as docx, pdf, epub, and html.

## Targets

The `saga` command has a number of targets:
- new [novel, short, script, etc]
- compile [draft, outline, research]
- wc (word count)
- grammar (run some kind of grammar/spellcheck tool?)

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

TBD: Write to `~drafts/<project type>/<short-title>` or `~/<type>/<short-title>/Output?`.

## TODO
- Make font type and size customizable
- 