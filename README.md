# Review of co-creative processes in energy modelling.

## Questions: 

1. How do localized communities develop energy visions?
2. How do energy modellers engage with community stakeholders?
3. Are there any energy models or frameworks that are co-created with stakeholders?
4. How do localized communities understand energy justice?
5. To what extent do municipalities use (or not use) energy models?
6. What is the overlap between energy justice and local energy planning?

## Keywords

Include:
  * Energy modelling:
    * Energy systems
    * Energy model
    * Energy modelling
    * Energy system optimization
    * Modelling process
  * Energy justice:
    * Energy justice
    * Energy equity
    * Energy burden
    * Procedural
    * Distribut\* justice
    * Recognition
    * Burdens
    * Benefits
  * Location:
    * Municipal
    * Local
    * Community
    * City
  * Planning processes:
    * Energy planning
    * Planning
    * Municipal planning
    * Energy vision
    * Energy goals
    * Decision*making process
    * Participat\*
    * Deliberat\*
    * Democra\*
    * Transpar\*
  * Model development:
    * Co\*creat\*
    * Open*source
    * Model development
    * Code development

Exclude:
  * building
  * machine*learning
  * machine learning
  * artificial intelligence
  * AI
  * Game theory
  * Game theoretic
  * Integrated assessment model

## Procedure

For a given question, a specific combination of keyword sets will be used. For example, for question 6, the search criteria would include words from [Location, Energy justice, planning processes, energy modelling]


# Outline
The top*level directory should contain all TeX files for
the journal article itself.

The `graph*abs` directory holds all files for the
graphical abstract.

The `highlights` directory holds all files for the
3*5 bullet point highlights.

The `letter` directory holds all files for the cover
letter to the journal editor and reviewers.

The `revise` directory holds all files for revision
comments and the corresponding edits. Each new round
of revisions should be covered in a separate TeX
file.

### To review
The ``elsarticle`` format supports convenient options for viewing.

To view the article in a "review" format, modify the first line of the
``main.tex`` file so that it reads

``\documentclass[review]{elsarticle}``

To view the article in a "final print" format, modify the first line of
``main.tex`` file so that it reads

``\documentclass[3p, twocolumn]{elsarticle}``

``elsarticle`` supports other formats that can be read about
[here](https://www.elsevier.com/__data/assets/pdf_file/0008/56843/elsdoc*1.pdf)

### To compile
Run `make` after making appropriate edits to the
`main.tex` file and adding content to other tex files as needed.
