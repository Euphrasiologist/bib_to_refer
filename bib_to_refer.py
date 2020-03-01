#!/usr/bin/python3

import bibtexparser
import argparse
import re

# sort out the arguments
parser = argparse.ArgumentParser(description="Process an input BibTeX file into a refer database.", 
                                 epilog="Type `man 1 refer` on linux like machines to view the refer manual page.")
parser.add_argument('filename', help="Input .bib file path.")
parser.add_argument('--number', type=int, nargs=1, help="Minimum number of records in a refer entry, default 0", default=0)
args = parser.parse_args()


    ######################################
#                 Dictionary                #
    ######################################

# more can be added here, if necessary. I think these are the 
# only ones that are actually processed by refer.
bib_to_refer = {"author":"%A",
                "title":"%T",
                "journal":"%J",
                "volume":"%V",
                "number":"%N",
                "pages":"%P",
                "year":"%D"}
# parse the --number flag here
minimum = args.number

    ######################################
#                 Load database             #
    ######################################

# load the bib database
with open(args.filename) as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

    ######################################
#                 Begin loop                #
    ######################################

# loop through each bib entry
for bib in bib_database.entries:
    # shows which keys are in both bib and bib_to_refer
    common_keys = [key for key, value in bib.items() if key in bib_to_refer]
    
    # create dictionary of key and value from key in large dictionary if key is present in common keys.
    subset_dict = dict((key, bib[key]) for key in common_keys if key in bib)

    # a keyerror throws if bib_to_refer is not trimmed to match
    subset_bib_to_refer = dict((key, bib_to_refer[key]) for key in common_keys if key in bib_to_refer)

    # now to replace the keys in subset_dict with keys from bib_to_refer
    subset_dict_refer = dict((value,subset_dict[key]) for (key, value) in subset_bib_to_refer.items())

    # lastly split %A records with multiple authors. 
    # first turn subset_dict_refer into a list
    subset_dict_refer_ls = []
    for key, value in subset_dict_refer.items():
        subset_dict_refer_ls.append(key + " " + value)
    
    # second, match and extract %A
    regex1 = re.compile("%A")
    sort_authors = list(filter(regex1.match, subset_dict_refer_ls))

    # split sort_authors on " and " and add %A to start
    for authors in sort_authors:
        sort_authors_2 = ["%A " + s for s in authors.split(" and ")]

    # match and extract %A %A. This is surely stupid and inefficient but I am a novice.
    sort_authors_3 = []
    for el in sort_authors_2:
        l = el.replace("%A %A", "%A")
        sort_authors_3.append(l)

    # append initial list to sort_authors_3
    # remove the entry in the list that contains %A
    regex2 = re.compile("^%A")
    filtered = [i for i in subset_dict_refer_ls if not regex2.match(i)]

    # lowercase those letters not at the beginning of a word
    refer_entries = sort_authors_3 + filtered
    refer_entries = [i.title() for i in refer_entries]

    # append the 'keyword' entry to the end of each list, which I am saying is the first word of the title..?
    # get the title
    regex3 = re.compile("^%T")

    # extract as string
    # if title exists in refer entries, regex to extract keyword
    if any(regex3.match(entry) for entry in refer_entries):
        title = list(filter(regex3.match, refer_entries))[0]

        # extract first word, which may or may not be informative...
        # TODO add custom keyword option (perhaps another regex on the title.)
        regex4 = re.compile("^%T ([A-Z][a-z]*)")
        keyword = ['%K ' + regex4.findall(title)[0]]
        refer_entries = refer_entries + keyword

        if len(refer_entries) > minimum[0]:
            for entry in refer_entries:
                print(entry)
            print("\n")
    # else no title, no keyword.
    else:
        if len(refer_entries) > minimum[0]:
            for entry in refer_entries:
                print(entry)
            print("\n")