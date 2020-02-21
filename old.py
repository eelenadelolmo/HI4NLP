import os
import re
import fileinput
import pyconll as pc
from conllu import parse

# Pending: Iterators could be implemented to reduce resources consumption
from conllu import parse_tree



docsdir = 'conll/'
keyspath = 'rules_keys/negation_keys_UNED.txt'              # Keys list for the domain
keyspath_out = 'rules_keys/negation_keys_out.txt'           # Keys list to erase depending on context for the domain
rulepath = 'rules_scope/rules_scope_v1.txt'                 # Rules list to match focus



def conllu_transformer(file_conll, file_conllu):

    # non-greedy quantifier to match only the first six columns after tabulation
    regex_6 = r"^(.+?\t.+?\t.+?\t.+?\t.+?\t.+?\t)"

    # matching the -4:-2 columns after tabulation
    regex_deps = r"(\d+?\t.+?)\t-\t-$"

    # greedy quantifier to match every line as $1
    regex_total = r"(^.+)"

    nf = open(file_conllu, "w")

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

            nf.write(line)



def conllu_annotator_keys(file_conllu, keysfile, keys_file_out, file_conllu_annotated):

    conll = pc.load_from_file(file_conllu)
    nf = open(file_conllu_annotated, "w")

    keys = open(keysfile, "r")
    unitokens = []
    multitokens = []
    multitokens_out = []



    for line in keys:

        keytokens = line.split()

        if len(keytokens) == 1:
            unitokens.append(keytokens[0])

        if len(keytokens) > 1:
            multitokens.append(keytokens[0:len(keytokens)])



    for line in keys_file_out:
        keytokens_out = line.split()
        multitokens_out.append(keytokens_out[0:len(keytokens_out)])



    for sentence in conll:
        for word in sentence:
            word.feats['negkey'] = set()
            word.feats['negkey'].add("no")



    # Each multitoken negation key checked once per sentence
    for multitoken in multitokens:

        #if ("[" not in multitoken[-1]):

        # Adding multitoken negation keys
        for sentence in conll:

            count_word_n = 0

            checking = False        # Controls whether a negation multikey is being checked

            for word in sentence:

                # No multitoken being checked yet
                if not(checking):

                    # Matches first token of a multiword negation key which has not been matched as part of one before
                    # Upper-case negation keys allowed only in the very first word of a sentence (in order to avoid matching negation keys inside questions)
                    if (count_word_n == 0 and word.form.lower() == multitoken[0] and "yes" not in word.feats['negkey']) or (word.form == multitoken[0] and "yes" not in word.feats['negkey']):

                        checking = True
                        multitoken_checking = multitoken
                        n = len(multitoken_checking) - 1                # Index updated to the -second token in the tokens list

                        word.feats['negkey'] = set()
                        word.feats['negkey'].add("CHECKING")       # Pending feature created

                # Multitoken being checked
                else:

                    # Successfully matched and not matched as part of one before
                    if word.form == multitoken_checking[-n] and "yes" not in word.feats['negkey']:

                        word.feats['negkey'] = set()
                        word.feats['negkey'].add("CHECKING")

                        n -= 1

                        # Multitoken fully matched
                        if (n == 0):

                            for word in sentence:
                                if 'CHECKING' in word.feats['negkey']:
                                    word.feats['negkey'] = set()
                                    word.feats['negkey'].add("yes")
                                    # word.feats['negkey'].add("mete_multi")

                                if 'UNANNOTATED_tmp' in word.feats['negkey']:
                                    word.feats['negkey'] = set()
                                    word.feats['negkey'].add("UNANNOTATED")
                                    # word.feats['negkey'].add("mete_multi")

                            checking = False


                    # Matched as part of a negation key but unannotated
                    # Punctuation words delimitate the scope
                    elif multitoken_checking[-n] == "?" and "yes" not in word.feats['negkey'] and word.form != "," and word.form != "." and word.form != "(" and word.form != ")" and word.form != ":":

                        word.feats['negkey'] = set()
                        word.feats['negkey'].add("UNANNOTATED_tmp")

                        n -= 1

                    # Unuccessfully matched
                    else:
                        for word in sentence:
                            if 'CHECKING' in word.feats['negkey'] or "UNANNOTATED_tmp" in word.feats['negkey']:
                                word.feats['negkey'] = set()
                                word.feats['negkey'].add("no")
                                # word.feats['negkey'].add("borra_multi")
                        checking = False

                count_word_n += 1



            # A multiword negation key being checked at the end of a sentence
            if (checking):
                for word in sentence:
                    if 'CHECKING' in word.feats['negkey'] or "UNANNOTATED_tmp" in word.feats['negkey']:
                        word.feats['negkey'] = set()
                        word.feats['negkey'].add("no")
                        # word.feats['negkey'].add("borra_multi")



    # Adding unitoken negation keys
    for sentence in conll:

        # Each unitoken negation key checked once per sentence
        for unitoken in unitokens:

            count_word_n = 0

            for word in sentence:

                if (count_word_n == 0 and word.form.lower() == unitoken) or (word.form == unitoken):

                    # Token not matched as a multitoken negation key
                    if "yes" not in word.feats['negkey']:
                        word.feats['negkey'] = set()
                        word.feats['negkey'].add("yes")
                        # word.feats['negkey'].add("mete_uni")

                count_word_n += 1



    # Mutitoken negation keys with a not-matching requirement (i. e. the last token first character is "[")
    for multitoken_out in multitokens_out:

        # Adding multitoken negation keys
        for sentence in conll:

            count_word_n = 0
            containing = True       # Controls whether a token is excepted to be present (True) or absent (False)
            checking = False        # Controls whether a negation multikey is being checked

            for word in sentence:

                # No multitoken being checked yet
                if not(checking):

                    # Matches first token of a multiword negation key that may be erased and was matched before
                    if word.form.lower() == multitoken_out[0] and "yes" in word.feats['negkey']:

                        checking = True
                        multitoken_checking = multitoken_out

                        n = len(multitoken_checking) - 1                    # Index updated to the -second token in the tokens list
                        containing = "[" not in multitoken_checking[-n]

                        word.feats['negkey'] = set()
                        word.feats['negkey'].add("CHECKING_out")            # Pending feature created

                        count_word_n += 1
                        continue                                            # Next word in order to avoid the checking conditional to be true for the same token (avoiding else due to complex conditional anidation)

                # Multitoken being checked
                if checking:

                    # Token not delimited by a non-matching token(s)
                    if containing:

                        # Token between matching and not-matching not matched before as a key in order not to loose the annotation for a _tmp
                        if multitoken_checking[-n] == "?" and "yes" not in word.feats['negkey']:

                            # word.feats['negkey'] = set()
                            # word.feats['negkey'].add("UNANNOTATED_tmp")

                            n -= 1
                            count_word_n += 1
                            containing = "[" not in multitoken_checking[-n]
                            continue

                        # Already matched as key OR
                        # Already matched as discontinuous key OR
                        # Unsuccessfully matched
                        if ("yes" in word.feats['negkey']) or ("UNANNOTATED" in word.feats['negkey']) or (word.form != multitoken_checking[-n] and "yes" not in word.feats['negkey']):

                            # Revert the original annotation for the tokens matched (with a CHECKING_out feature)
                            for word in sentence:
                                if 'CHECKING_out' in word.feats['negkey']:
                                    word.feats['negkey'] = set()
                                    word.feats['negkey'].add("yes")

                                # if "UNANNOTATED" in word.feats['negkey']:
                                #     pass

                            checking = False
                            continue

                        # Successfully matched
                        if word.form == multitoken_checking[-n]:

                            word.feats['negkey'] = set()
                            word.feats['negkey'].add("CHECKING_out")

                            n -= 1
                            count_word_n += 1
                            containing = "[" not in multitoken_checking[-n]

                            continue                                            # Next word in order to avoid the containing conditional to be true for the same token (avoiding else due to complex conditional anidation)


                    # Checking if a negation key must keep annotated or not
                    if not(containing):

                        # Matched with the stopping word --> Delete tmp annotations
                        if word.form == multitoken_checking[-n][1:]:

                            for word in sentence:
                                # if 'CHECKING_out' in word.feats['negkey'] or "UNANNOTATED_tmp" in word.feats['negkey']:
                                if 'CHECKING_out' in word.feats['negkey']:
                                    word.feats['negkey'] = set()
                                    word.feats['negkey'].add("no")

                            checking = False
                            containing = True


                        # Successfully not matched with the stopping word --> Confirm tmp annotations
                        if word.form != multitoken_checking[-n][1:]:

                            # Revert the original annotation for the tokens matched (with a CHECKING_out feature)
                            for word in sentence:

                                if 'CHECKING_out' in word.feats['negkey']:
                                    word.feats['negkey'] = set()
                                    word.feats['negkey'].add("yes")

                                # if 'UNANNOTATED_tmp' in word.feats['negkey']:
                                #     word.feats['negkey'] = set()
                                #     word.feats['negkey'].add("no")

                            checking = False
                            containing = True

                count_word_n += 1


            # A multiword negation key being checked at the end of a sentence
            if (checking):

                for word in sentence:

                    if 'CHECKING' in word.feats['negkey'] or "UNANNOTATED_tmp" in word.feats['negkey']:
                        word.feats['negkey'] = set()
                        word.feats['negkey'].add("no")

                    if 'CHECKING_out' in word.feats['negkey'] or "UNANNOTATED_tmp" in word.feats['negkey']:
                        word.feats['negkey'] = set()
                        word.feats['negkey'].add("yes")




    nf.write(conll.conll())





def conllu_annotator_scope(file_conllu_annotated, rules_file, file_conllu_annotated_rules):

    nf = open(file_conllu_annotated_rules, "w")
    input = open(file_conllu_annotated, "r", encoding="utf-8")

    rules_text = open(rules_file, "r")
    rules = []

    # Matching rules of child dependency from the negation key, consisting of:
    # - A deprel as the name of a relation/2 with:
    # - A first argument as the lemma of the expected head
    # - A second argument with the options for matching, being
    #   ALL if all children nodes from the head of a scope should be annotated
    #   ONE if only the immediate child should be annotated
    pattern_child_rules = re.compile(r".+?\(.+?, ?(ALL)|(ONE)\)")
    child_rules = []

    # Matching rules of parent dependency from the negation key, consisting of:
    # - A deprel as the name of a relation/2 with:
    # - A first argument with the options for matching, being
    #     #   ALL if all children nodes from the head of a scope should be annotated
    #     #   ONE if only the immediate child should be annotated
    # - A second argument as the lemma of the expected head
    pattern_parent_rules = re.compile(r".+?\(((ALL)|(ONE)), ?.+?\)")
    parent_rules = []

    for line in rules_text:
        rules.append(line)

    for rule in rules:

        if pattern_child_rules.match(rule) is not None:

            lemma = re.match(".+?\((.+?), ?(ALL)|(ONE)\)", rule).group(1)
            deprel = re.match("(.+?)\(", rule).group(1)
            type = re.match(".+?\(.+?, ?((ALL)|(ONE))\)", rule).group(1)

            new_rule = {}
            new_rule['lemma'] = lemma
            new_rule['deprel'] = deprel
            new_rule['type'] = type

            child_rules.append(new_rule)

        if pattern_parent_rules.match(rule) is not None:

            lemma = re.match(".+?\(.+?, ?(.+?)\)", rule).group(1)
            deprel = re.match("(.+?)\(", rule).group(1)
            type = re.match(".+?\(((ALL)|(ONE)), ?.+?\)", rule).group(1)

            new_rule = {}
            new_rule['lemma'] = lemma
            new_rule['deprel'] = deprel
            new_rule['type'] = type

            parent_rules.append(new_rule)


    sentences = parse(input.read())

    for sentence in sentences:

        for rule in child_rules:

            # Due to resources consumption only
            if sentence.filter(feats__negkey="yes"):

                for token in sentence:

                    # Token matching the requirement for being the head of the scope
                    if token['feats']['negkey'] == "yes" and token['lemma'] == rule['lemma']:
                        negkey_id = token['id']

                        for token_2 in sentence:

                            # Token matching the requirement of the deprel type and the excepted head
                            if token_2['deprel'] == rule['deprel'] and token_2['head'] == negkey_id:
                                token_2['feats']['scope'] = 'yes'
                                scope_id = token_2['id']


                                # If the scope must be annotated recursively
                                if rule['type'] == "ALL":

                                    hijos = sentence.to_tree().children
                                    padre = None

                                    # Getting the head of the scope as a subtree
                                    while len(hijos) > 0 and padre is None:

                                        for hijo in hijos:

                                            if hijo.token['id'] == scope_id:
                                                padre = hijo
                                                break

                                        nietos = []

                                        for hijo in hijos:
                                            nietos.extend(hijo.children)

                                        hijos = nietos



                                    if padre is not None:
                                        hijos = padre.children



                                    # Annotating all children of the head of the scope
                                    while len(hijos) > 0:

                                        for hijo in hijos:

                                            hijo.token['feats']['scope'] = 'yes'

                                        nietos = []

                                        for hijo in hijos:
                                            nietos.extend(hijo.children)

                                        hijos = nietos



        n_anotados_parent_rules = 0

        for rule in parent_rules:

            # Due to resources consumption only
            if sentence.filter(feats__negkey="yes"):

                for token in sentence:

                    # Token matching the requirement for being the head of the scope
                    if token['feats']['negkey'] == "yes" and token['lemma'] == rule['lemma'] and token['deprel'] == rule['deprel']:
                        negkey_head = token['head']
                        negkey_id = token['id']
                        # print(token['lemma'], negkey_head)

                        for token_2 in sentence:

                            # Token matching the requirement of the deprel type and the excepted head
                            if token_2['id'] == negkey_head:
                                # print(token_2['id'])
                                token_2['feats']['scope'] = 'yes'
                                scope_id = token_2['id']
                                n_anotados_parent_rules += 1


                                # If the scope must be annotated recursively
                                if rule['type'] == "ALL":

                                    hijos = sentence.to_tree().children
                                    padre = None

                                    # Getting the head of the scope as a subtree
                                    while len(hijos) > 0 and padre is None:

                                        for hijo in hijos:

                                            if hijo.token['id'] == scope_id:
                                                padre = hijo
                                                break

                                        nietos = []

                                        for hijo in hijos:
                                            nietos.extend(hijo.children)

                                        hijos = nietos



                                    if padre is not None:
                                        hijos = padre.children



                                    # Annotating all children of the head of the scope
                                    while len(hijos) > 0:

                                        for hijo in hijos:

                                            # In order to avoid annotating the parent-scope negation key as its own scope when the scope is described as recursive in the scope rules file
                                            if hijo.token['id'] != negkey_id:
                                                hijo.token['feats']['scope'] = 'yes'

                                        nietos = []

                                        for hijo in hijos:
                                            nietos.extend(hijo.children)

                                        hijos = nietos



        nf.write(sentence.serialize())








directory = os.listdir(docsdir)

for f in directory:

    if f.endswith(".conll"):

        f_noExt = f[:-6]

        # Transforms the input documents from docsdir into the CoNLL-U format
        # Puts its output (.conllu) in the conllu folder
        conllu_transformer(docsdir + f, "conllu/" + f_noExt + ".conllu")

        # Exploits a conllu file in order to add new fields depending on rules based on string continuous and discontinuous (un)matching
        # Puts its output (.conllu) in the conllu_annotated folder
        conllu_annotator_keys("conllu/" + f_noExt + ".conllu", keyspath, keyspath_out, "conllu_keys/" + f_noExt + "_keys" + ".conllu")

        # Exploits a conllu file in order to add new fields depending on rules
        conllu_annotator_scope("conllu_keys/" + f_noExt + "_keys" + ".conllu", rulepath, "conllu_keys_scope/" + f_noExt + "_keys_scope" + ".conllu")


# print("Probando solo con un documento")
# conllu_annotator_scope("conllu_keys/" + "appended_unique_noInitialPunt_keys.conllu", rulepath, "conllu_keys_scope/" + "appended_unique_noInitialPunt_keys_scope.conllu")
