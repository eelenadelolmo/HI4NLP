#! /usr/bin/env python

import os
import pyconll as pc
import sys
import getopt


def txt_transformer(file_conllu, file_txt):

    conll = pc.load_from_file(file_conllu)
    nf = open(file_txt, "w")

    for sentence in conll:
        sentence_txt = ""

        for word in sentence[:-1]:
            sentence_txt = sentence_txt + " " + word.form

        sentence_txt = sentence_txt + ".\n"

        nf.write(sentence_txt)


def main(argv):

    inputdir = 'conllu/'
    outputdir = 'txt/'

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["idir=", "odir="])

    except getopt.GetoptError:
        print('transformer_forms_conllu.py -i <inputDirectory> -o <outputDirectory>')
        sys.exit(2)

    for opt, arg in opts:

        if opt == '-h':
            print('transformer_forms_conllu.py -i <inputDirectory> -o <outputDirectory>')
            sys.exit()

        elif opt in ("-i", "--idir"):
            inputdir = arg

        elif opt in ("-o", "--odir"):
            outputdir = arg

    print('The input directory is', inputdir)
    print('The output directory is', outputdir)

    directory = os.listdir(inputdir)

    for f in directory:
        if f.endswith(".conllu"):

            f_noExt = f[:-7]

            # Transforms the input documents from inputdir (CoNLL-U format expected) into a txt file of sentences with the forms of each sentence ended with a full stop.
            # Puts its output (.txt) in the outputdir folder
            txt_transformer(inputdir + f, outputdir + f_noExt + "_forms.txt")


if __name__ == "__main__":
    main(sys.argv[1:])


