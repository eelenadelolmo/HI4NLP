#! /usr/bin/env python

import os
from conllu import parse
import sys
import getopt
import pandas as pd
from tabulate import tabulate


def main(argv):

    unmatcheddir = 'CEDEL2/annotated/CEDEL2_Q1/_unmatched/'
    matcheddir = 'CEDEL2/annotated/CEDEL2_Q1/_matched/'

    try:
        opts, args = getopt.getopt(argv, "hi:au:", ["udir=", "mdir="])

    except getopt.GetoptError:
        print('transformer_conllu.py -u <UnmatchedOutputDirectory> -m <MatchedOutputDirectory>')
        sys.exit(2)

    for opt, arg in opts:

        if opt == '-h':
            print('matrics.py -u <UnmatchedOutputDirectory> -m <MatchedOutputDirectory>')
            sys.exit()

        elif opt in ("-u", "--udir"):
            unmatcheddir = arg+ "/"

        elif opt in ("-a", "--adir"):
            matcheddir = arg+ "/"

    print('The unmatched directory is', unmatcheddir)
    print('The matched directory is', matcheddir)

    n_matched = 0
    n_unmatched = 0

    docs_ratio_matched = dict()

    directory = os.listdir(unmatcheddir)
    for f in directory:
        docs_ratio_matched[f] = [0, 0]

    directory = os.listdir(matcheddir)
    for f in directory:
        docs_ratio_matched[f] = [0, 0]


    directory = os.listdir(unmatcheddir)
    for f in directory:
        if f.endswith(".conllu"):
            input = open(unmatcheddir + f, "r", encoding="utf-8")
            sentences = parse(input.read())
            n_unmatched += len(sentences)

            docs_ratio_matched[f][0] += len(sentences)

    directory = os.listdir(matcheddir)
    for f in directory:
        if f.endswith(".conllu"):
            input = open(matcheddir + f, "r", encoding="utf-8")
            sentences = parse(input.read())
            n_matched += len(sentences)

            docs_ratio_matched[f][1] += len(sentences)

    for file in docs_ratio_matched:

        # Preventing errors due to empty docs
        if docs_ratio_matched[file][0] + docs_ratio_matched[file][1] != 0:
            docs_ratio_matched[file].append(round((docs_ratio_matched[file][1]/(docs_ratio_matched[file][0] + docs_ratio_matched[file][1]))*100, 2))

    nf = open("metrics_CEDEL2_Q1.txt", "w")

    nf.write("Número de oraciones principales con sujeto antepuesto: " + str(n_matched))
    nf.write("\n")

    nf.write("Número de oraciones principales sin sujeto antepuesto: " + str(n_unmatched))
    nf.write("\n")
    nf.write("\n")

    nf.write("Porcentaje de oraciones con sujeto antepuesto: " + str(round((n_matched/(n_unmatched + n_matched))*100, 2)) + " %")
    nf.write("\n")
    nf.write("\n")

    nf.write("Porcentaje de oraciones con sujeto antepuesto por documento:")
    nf.write("\n")
    nf.write("\n")

    df = pd.DataFrame.from_dict(docs_ratio_matched, orient='index')
    df = df.rename(columns={0: 'No preceding nsubj', 1:'Preceding nsubj', 2:"% of preceding nsubjs"})
    df_desc = df.rename(columns={0: 'No preceding nsubj', 1:'Preceding nsubj', 2:"% of preceding nsubjs"}).describe()

    nf.write(tabulate(df_desc, headers='keys', tablefmt='psql'))
    nf.write("\n")
    nf.write("\n")

    nf.write(tabulate(df, headers='keys', tablefmt='psql'))


if __name__ == "__main__":
    main(sys.argv[1:])
