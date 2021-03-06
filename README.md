## Parse a BibTeX file into a refer database

### Example

BibTeX files look something like this:

@Article{RN298,\
   author = {Abbott, R. J.},\
   title = {LIFE-HISTORY VARIATION ASSOCIATED WITH THE POLYMORPHISM FOR CAPITULUM TYPE AND OUTCROSSING RATE IN SENECIO-VULGARIS L},\
   journal = {Heredity},\
   volume = {56},\
   pages = {381-391},\
   ISSN = {0018-067X},\
   DOI = {10.1038/hdy.1986.60},\
   url = {<Go to ISI>://WOS:A1986C827000012},\
   year = {1986},\
   type = {Journal Article}\
}
  
The output of the script produces:

%A Abbott, R. J.\
%D 1986\
%P 381-391\
%V 56\
%J Heredity\
%T Life-History Variation Associated With The Polymorphism For Capitulum Type And Outcrossing Rate In Senecio-Vulgaris L\
%K Life

This can then be used in the GNU troff (groff) and refer unix toolkits for making pretty typeset formatted output, which looks a bit like LaTeX, but much faster (and easier..?).

### Usage

There is an implementation in python, and one in JavaScript, so it can be easily manipulated in the browser.

A python script is provided which takes a mandatory argument, specifying a path to a .bib file and an optional argument which filters the final refer record based upon a minimum number of entries. Use `-h` flag for more information.

`python bib_to_refer.py [-h] [--number NUMBER] filename`

By default it prints to the console, so it is best to pass it to a simple text file.

`python bib_to_refer.py /path/to/bib.bib > refer_database.txt`

The JavaScript script is an export of the 'Refer' object. I think it will run like Refer.parse(refer_database_file).

### Dependencies

The script depends on `bibtexparser`, a cool module that allows for parsing of BibTeX files, `argparse` which allows for pretty command line interface and `re` for regular expressions.
