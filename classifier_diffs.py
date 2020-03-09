#! /usr/bin/env python

import os
from conllu import parse
import pyconll as pc
import regex


def classifier_diffs(file_in, file_out, outputfile):

    outputfile_toAppend = open(outputfile, "a")

    conll_in = pc.load_from_file(file_in)
    conll_out = pc.load_from_file(file_out)
    conll_out_str = ""

    for s in conll_out:
        conll_out_str = conll_out_str + " ".join([w.form for w in s]) + "\n"

    for sentence_in in conll_in:

        sentence_in_str = " ".join([w.form for w in sentence_in])
        if len(sentence_in_str) >= 20:
            sentence_in_str = sentence_in_str[:20]

        try:
            if not regex.search('(' + sentence_in_str + '){e<=5}', conll_out_str):

                outputfile_toAppend.write(sentence_in.source + "\n\n")
        except:
            continue

    outputfile_toAppend.close()




unmatched_inputdir = 'AnCora_Surface_Syntax_Dependencies/annotated/_unmatched/'
matched_inputdir = 'AnCora_Surface_Syntax_Dependencies/annotated/_matched/'
unmatched_inputdir_freeling = 'AnCora_Surface_Syntax_Dependencies/annotated_freeling/_unmatched/'
matched_inputdir_freeling = 'AnCora_Surface_Syntax_Dependencies/annotated_freeling/_matched/'

"""

outputdir_overmatched = 'AnCora_Surface_Syntax_Dependencies/overmatched_by_freeling.conllu'
outputdir_undermatched = 'AnCora_Surface_Syntax_Dependencies/undermatched_by_freeling.conllu'

undermatched = open(outputdir_undermatched, "w")
overmatched = open(outputdir_overmatched, "w")

directory_undermatched = os.listdir(unmatched_inputdir)
directory_matched = os.listdir(matched_inputdir)


for f in directory_undermatched:
    if f.endswith(".conllu"):

        f_oldName = f[:-17]

        # Appends to the conllu document of the third argument
        # the sentences in the file of the first argument
        # not contained in the file of the second document
        classifier_diffs(unmatched_inputdir + f, unmatched_inputdir_freeling + f_oldName + "_forms_annotated.conllu", outputdir_overmatched)


for f in directory_matched:
    if f.endswith(".conllu"):

        f_oldName = f[:-17]

        # Appends to a conllu document of the third argument
        # the sentences in the file of the first argument
        # not contained in the file of the second document
        classifier_diffs(matched_inputdir + f, matched_inputdir_freeling + f_oldName + "_forms_annotated.conllu", outputdir_undermatched)


overmatched_final = open(outputdir_overmatched, "r", encoding="utf-8")
overmatched_final_sentences = parse(overmatched_final.read())
print(len(overmatched_final_sentences))

undermatched_final = open(outputdir_undermatched, "r", encoding="utf-8")
undermatched_final_sentences = parse(undermatched_final.read())
print(len(undermatched_final_sentences))

"""

outputdir_overmatched = 'AnCora_Surface_Syntax_Dependencies/overmatched_by_AnCora.conllu'
outputdir_undermatched = 'AnCora_Surface_Syntax_Dependencies/undermatched_by_AnCora.conllu'

overmatched = open(outputdir_overmatched, "w")
undermatched = open(outputdir_undermatched, "w")

directory_unmatched = os.listdir(unmatched_inputdir_freeling)
directory_matched = os.listdir(matched_inputdir_freeling)

for f in directory_unmatched:
    if f.endswith(".conllu"):

        f_oldName = f[:-23]

        # Appends to the conllu document of the third argument
        # the sentences in the file of the first argument
        # not contained in the file of the second document
        classifier_diffs(unmatched_inputdir_freeling + f, unmatched_inputdir + f_oldName + "_annotated.conllu", outputdir_overmatched)


for f in directory_matched:
    if f.endswith(".conllu"):

        f_oldName = f[:-23]

        # Appends to a conllu document of the third argument
        # the sentences in the file of the first argument
        # not contained in the file of the second document
        classifier_diffs(matched_inputdir_freeling + f, matched_inputdir + f_oldName + "_annotated.conllu", outputdir_undermatched)


overmatched_final = open(outputdir_overmatched, "r", encoding="utf-8")
overmatched_final_sentences = parse(overmatched_final.read())
print(len(overmatched_final_sentences))

undermatched_final = open(outputdir_undermatched, "r", encoding="utf-8")
undermatched_final_sentences = parse(undermatched_final.read())
print(len(undermatched_final_sentences))

