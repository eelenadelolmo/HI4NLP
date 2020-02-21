#! /usr/bin/env python

import os
from conllu import parse
import sys
import getopt



def conllu_classifier(inputfile, unmatchedfile, matchedfile):

    matched_nf = open(matchedfile, "w")
    unmatched_nf = open(unmatchedfile, "w")

    input = open(inputfile, "r", encoding="utf-8")
    sentences = parse(input.read())

    for sentence in sentences:
        matched = False

        for token in sentence:

            if token['feats']['matched'] != "no":
                matched = True

        if matched:
            matched_nf.write(sentence.serialize())
        else:
            unmatched_nf.write(sentence.serialize())



def main(argv):

    inputdir = 'annotated/'
    unmatched_outputdir = 'annotated/_unmatched/'
    matched_outputdir = 'annotated/_matched/'

    try:
        opts, args = getopt.getopt(argv, "hi:au:", ["idir=", "udir=", "mdir="])

    except getopt.GetoptError:
        print('transformer_conllu.py -i <inputDirectoru> -u <UnmatchedOutputDirectory> -m <MatchedOutputDirectory>')
        sys.exit(2)

    for opt, arg in opts:

        if opt == '-h':
            print('classifier.py -i <inputdir> -o <outputdir>')
            sys.exit()

        elif opt in ("-i", "--idir"):
            inputdir = arg+ "/"

        elif opt in ("-u", "--udir"):
            unmatched_outputdir = arg+ "/"

        elif opt in ("-a", "--adir"):
            matched_outputdir = arg+ "/"

    print('The input directory is', inputdir)
    print('The unmatched output directory is', unmatched_outputdir)
    print('The matched output directory is', matched_outputdir)

    directory = os.listdir(inputdir)

    for f in directory:
        if f.endswith(".conllu"):

            f_noExt = f[:-7]

            # Creates two new folders to classify the sentences in a document depending on
            # whether they contains a matched feature annotation or not
            conllu_classifier(inputdir + f, unmatched_outputdir + f_noExt + ".conllu", matched_outputdir + f_noExt + ".conllu")



if __name__ == "__main__":
    main(sys.argv[1:])


