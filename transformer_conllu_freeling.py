#! /usr/bin/env python

import os
import re
import fileinput
import pyconll as pc
import sys
import getopt


def conllu_freeling_transformer(file_conll, file_conllu):

    # non-greedy quantifier to match only the first six columns after tabulation
    regex_6 = r"^(.+?\t.+?\t.+?\t.+?\t.+?\t.+?\t)"

    # matching the -4:-2 columns after tabulation
    regex_deps = r"(\d+?\t.+?)\t-\t-$"

    # greedy quantifier to match every line as $1
    regex_total = r"(^.+)"

    tmp_file_name = file_conllu[:-6] + "_tmp" + ".conllu"

    tmp_nf = open(tmp_file_name, "w")

    with fileinput.input(files=(file_conll), openhook=fileinput.hook_encoded("utf-8")) as x:

        for line in x:

            # Correcting tabs
            line = re.sub(" +", "\t", line)

            # Keeping conllu fields (1-6 and 10-11)
            # line = re.sub(regex_6 + r".+", r"\1", line)
            # line = re.sub(r".+" + regex_deps, r"\1", line)
            line = re.sub(regex_6 + r"-\t-\t.+?\t" + regex_deps, r"\1\2", line)

            # Tabs required in order not to math word forms line "pre-venta"
            # line = re.sub("\t-\t", "\t_\t", line)

            # Adding empty fields at the end
            line = re.sub(regex_total, r"\1\t_\t_", line)

            tmp_nf.write(line)

        tmp_nf.close()

    conll = pc.load_from_file(tmp_file_name)
    os.remove(tmp_file_name)

    for sentence in conll:
        for word in sentence:
            word.feats['matched'] = set()
            word.feats['matched'].add("no")

    nf = open(file_conllu, "w")
    nf.write(conll.conll())


def main(argv):

    inputdir = 'CEDEL2/conll_CEDEL2/CEDEL2_Q1/'
    outputdir = 'CEDEL2/conllu/CEDEL2_Q1/'

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["idir=", "odir="])

    except getopt.GetoptError:
        print('transformer_conllu_freeling.py -i <inputDirectory> -o <outputDirectory>')
        sys.exit(2)

    for opt, arg in opts:

        if opt == '-h':
            print('transformer_conllu.py -i <inputdir> -o <outputdir>')
            sys.exit()

        elif opt in ("-i", "--idir"):
            inputdir = arg + "/"

        elif opt in ("-o", "--odir"):
            outputdir = arg + "/"

    print('The input directory is', inputdir)
    print('The output directory is', outputdir)

    directory = os.listdir(inputdir)

    for f in directory:
        if f.endswith(".conll"):

            f_noExt = f[:-6]

            # Transforms the input documents from inputdir into the CoNLL-U format
            # Puts its output (.conllu) in the outputdir folder
            conllu_freeling_transformer(inputdir + f, outputdir + f_noExt + ".conllu")


if __name__ == "__main__":
    main(sys.argv[1:])


