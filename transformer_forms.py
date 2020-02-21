#! /usr/bin/env python

import os
import re
import fileinput
import pyconll as pc
from conllu import parse
import sys
import getopt



def conllu_transformer(file_conll, file_conllu):

    # greedy quantifier to match every commented line as $1
    regex_commented = r"(^#.+)"

    # greedy quantifier to match every line as $1
    regex_total = r"(^.+)"

    tmp_file_name = file_conllu[:-6] + "_tmp" + ".conllu"

    tmp_nf = open(tmp_file_name, "w")

    with fileinput.input(files=(file_conll), openhook=fileinput.hook_encoded("utf-8")) as x:

        for line in x:

            # Correcting tabs
            line = re.sub(" +", "\t", line)

            # Deleting commented lines
            line = re.sub(regex_commented, r"", line)

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

    inputdir = 'in/'
    outputdir = 'conllu/'

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["idir=", "odir="])

    except getopt.GetoptError:
        print('transformer_conllu.py -i <inputDirectory> -o <outputDirectory>')
        sys.exit(2)

    for opt, arg in opts:

        if opt == '-h':
            print('transformer_conllu.py -i <inputdir> -o <outputdir>')
            sys.exit()

        elif opt in ("-i", "--idir"):
            inputdir = arg

        elif opt in ("-o", "--odir"):
            outputdir = arg

    print('The input directory is', inputdir)
    print('The output directory is', outputdir)

    directory = os.listdir(inputdir)

    for f in directory:
        if f.endswith(".conll"):

            f_noExt = f[:-6]

            # Transforms the input documents from inputdir into the CoNLL-U format
            # Puts its output (.conllu) in the outputdir folder
            conllu_transformer(inputdir + f, outputdir + f_noExt + ".conllu")

    # conllu_transformer(inputdir + "2_19991102_ssd.conll", outputdir + f_noExt + ".conllu")



if __name__ == "__main__":
    main(sys.argv[1:])


