#! /usr/bin/env python

import os
import re
from conllu import parse
import sys
import getopt


def conllu_annotator_scope(file_conllu_annotated, rules_file, file_conllu_annotated_rules, order):

    nf = open(file_conllu_annotated_rules, "w")
    input = open(file_conllu_annotated, "r", encoding="utf-8")

    rules_text = open(rules_file, "r")
    rules = []

    # Matching rules of child dependency from a selected parent token, consisting of:
    # - A deprel as the name of a relation/2 with:
    # - A first argument as the key and the value expected for the selected parent
    # - A second argument with the options for matching, being
    #   ALL if all children nodes from the head of a scope should be annotated
    #   ONE if only the immediate child should be annotated
    pattern_child_rules = re.compile(r".+?\(.+?, ?(ALL)|(ONE)\)")
    child_rules = []

    # Matching rules of parent dependency from a selected child token, consisting of:
    # - A deprel as the name of a relation/2 with:
    # - A first argument with the options for matching, being
    #   ALL if all children nodes from the head of a scope should be annotated
    #   ONE if only the immediate child should be annotated
    # - A second argument as the key and the value expected for the selected child
    pattern_parent_rules = re.compile(r".+?\(((ALL)|(ONE)), ?.+?\)")
    parent_rules = []

    for line in rules_text:
        if not line.startswith("#"):
            rules.append(line)

    for rule in rules:

        if pattern_child_rules.match(rule) is not None:

            select = re.match(".+?\((.+?), ?(ALL)|(ONE)\)", rule).group(1)
            select_key = select[:select.find(':')]
            select_value = select[select.find(':')+1:]
            deprel = re.match("(.+?)\(", rule).group(1)
            type = re.match(".+?\(.+?, ?((ALL)|(ONE))\)", rule).group(1)

            new_rule = {}
            new_rule['select_key'] = select_key
            new_rule['select_value'] = select_value
            new_rule['deprel'] = deprel
            new_rule['type'] = type

            child_rules.append(new_rule)

        if pattern_parent_rules.match(rule) is not None:

            select = re.match(".+?\(.+?, ?(.+?)\)", rule).group(1)
            select_key = select[:select.find(':')]
            select_value = select[select.find(':')+1:]
            deprel = re.match("(.+?)\(", rule).group(1)
            type = re.match(".+?\(((ALL)|(ONE)), ?.+?\)", rule).group(1)

            new_rule = {}
            new_rule['select_key'] = select_key
            new_rule['select_value'] = select_value
            new_rule['deprel'] = deprel
            new_rule['type'] = type

            parent_rules.append(new_rule)

    sentences = parse(input.read())

    for sentence in sentences:

        for rule in child_rules:

            # Due to resources consumption only
            # if sentence.filter(feats__negkey="yes"):

            for token in sentence:

                if token[rule['select_key']] == rule['select_value']:
                    parent_id = token['id']

                    for token_2 in sentence:

                        # Token matching the requirement of the deprel type and the excepted head
                        if token_2['deprel'] == rule['deprel'] and token_2['head'] == parent_id:

                            child_id = token_2['id']

                            if order == 'ALL' or (order == 'PRECEDING' and parent_id > child_id) or (order == 'FOLLOWING' and parent_id < child_id):
                                token_2['feats']['matched'] = 'yes: ' + rule['deprel'] + ' child of ' + rule['select_value'] + " " + rule['select_key']


                                # If the child must be annotated recursively
                                if rule['type'] == "ALL":

                                    hijos = sentence.to_tree().children
                                    padre = None

                                    # Getting the head of the scope as a subtree
                                    while len(hijos) > 0 and padre is None:

                                        for hijo in hijos:

                                            if hijo.token['id'] == child_id:
                                                padre = hijo
                                                break

                                        nietos = []

                                        for hijo in hijos:
                                            nietos.extend(hijo.children)

                                        hijos = nietos

                                    if padre is not None:
                                        hijos = padre.children

                                    # Annotating all children
                                    while len(hijos) > 0:

                                        for hijo in hijos:

                                            hijo.token['feats']['matched'] = 'yes: ' + rule['deprel'] + ' child of ' + rule['select_value'] + " " + rule['select_key']

                                        nietos = []

                                        for hijo in hijos:
                                            nietos.extend(hijo.children)

                                        hijos = nietos

        n_anotados_parent_rules = 0

        for rule in parent_rules:

            # Due to resources consumption only
            # if sentence.filter(feats__negkey="yes"):

            for token in sentence:

                if token[rule['select_key']] == rule['select_value'] and token['deprel'] == rule['deprel']:
                    child_head = token['head']
                    child_id = token['id']

                    for token_2 in sentence:

                        # Token matching the requirement of the deprel type and the excepted head
                        if token_2['id'] == child_head:

                            parent_id = token_2['id']

                            if order == '' or (order == 'PRECEDING' and parent_id < child_id) or (order == 'FOLLOWING' and parent_id > child_id):

                                token_2['feats']['matched'] = 'yes: ' + rule['deprel'] + ' parent of ' + rule['select_value'] + " " + rule['select_key']
                                n_anotados_parent_rules += 1

                                # If the parent must be annotated recursively
                                if rule['type'] == "ALL":

                                    hijos = sentence.to_tree().children
                                    padre = None

                                    # Getting the head of the scope as a subtree
                                    while len(hijos) > 0 and padre is None:

                                        for hijo in hijos:

                                            if hijo.token['id'] == parent_id:
                                                padre = hijo
                                                break

                                        nietos = []

                                        for hijo in hijos:
                                            nietos.extend(hijo.children)

                                        hijos = nietos

                                    if padre is not None:
                                        hijos = padre.children

                                    # Annotating all children
                                    while len(hijos) > 0:

                                        for hijo in hijos:

                                            # In order to avoid annotating the selected child token as part of the children of its parent when the rule is recursive
                                            if hijo.token['id'] != child_id:
                                                hijo.token['feats']['matched'] = 'yes: ' + rule['deprel'] + ' child of ' + rule['select_value'] + " " + rule['select_key']

                                        nietos = []

                                        for hijo in hijos:
                                            nietos.extend(hijo.children)

                                        hijos = nietos

        nf.write(sentence.serialize())


def main(argv):

    inputdir = 'conllu_freeling' + '/'
    outputdir = 'annotated_freeling' + '/'
    rulesfile = 'syntax_rules/' + 'rules_nsubj.txt'
    order_option = 'ALL'

    try:
        opts, args = getopt.getopt(argv, "hirp:o:", ["idir=", "odir=", "rfile=", "pos="])

    except getopt.GetoptError:
        print('transformer_conllu.py -i <inputfile> -o <outputfile> -r <rulesfile> -c <orderOption>')
        sys.exit(2)

    for opt, arg in opts:

        if opt == '-h':
            print('transformer_conllu.py -i <inputfile> -o <outputfile> -r <rulesfile> -c <orderOption>')
            sys.exit()

        elif opt in ("-i", "--idir"):
            inputdir = arg + '/'

        elif opt in ("-o", "--odir"):
            outputdir = arg + '/'

        elif opt in ("-r", "--rfile"):
            rulesfile = 'syntax_rules/' + arg

        elif opt in ("-p", "--pos"):
            order_option = arg

    print('The input directory is', inputdir)
    print('The output directory is', outputdir)
    print('The rules file is', rulesfile)
    print('The order option is', order_option)

    directory = os.listdir(inputdir)

    for f in directory:
        if f.endswith(".conllu"):
            f_noExt = f[:-7]

            # Exploits a conllu file in order to add new fields depending on rules
            conllu_annotator_scope(inputdir + f_noExt + ".conllu", rulesfile, outputdir + f_noExt + "_annotated" + ".conllu", order_option)


if __name__ == "__main__":
    main(sys.argv[1:])

