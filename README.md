# Installation
pip install -r requirements.txt


# Processed corpora

* [Ancora corpus]

_AnCora Surface Syntax Dependencies published in 2014 at UPF (GLiCom) by Benjamin Kolz, Toni Badia and Roser Saurí_

_Syntax information, which is crucial in many NLP tools, can be represented by means of constituent structures or dependency relations. 
While each of these formalisms has its advantages and disadvantages and there is an ongoing debate on preferred uses of them, it is worth noting that dependency-based representations can also vary depending on the linguistic criteria they are based upon: from purely syntactically oriented to semantically motivated. 
Most current approaches to dependency functions within NLP embrace an (at least partial) semantic orientation, e.g., most notably, the Stanford parser and, in the case of Spanish, the AnCora corpus and any parser trained on that. 
By contrast, the current resource presents a corpus of dependency relations for Spanish based on purely syntactic criteria.
Therefore we decided to name this corpus 'AnCora Surface Syntax Dependencies'._

_For further information see: "From constituents to syntax-oriented dependencies" published in SEPLN, march 2014 ISSN 1135-5948 
© 2014 Sociedad Española para el Procesamiento del Lenguaje Natural_

* [CEDEL2 corpus]

_CEDEL2 stands for Corpus Escrito del Español como L2 ‘L2 Spanish Written Corpus’._

_CEDEL2 (version 1.0) is a large database containing the language produced by learners of Spanish as a second/foreign language (L2). This database is called a linguistic ‘corpus’._

_CEDEL2 contains the language produced by English-speaking natives who are learning Spanish. It also contains a subcorpus of Greek-speaking learners of English. For future versions of the corpus, we are also collecting data from Japanese-speaking learners of Spanish._

_CEDEL2 also contains a subcorpus of Spanish native speakers for comparative purposes._


# Scripts

This repository contains the following Bash and Python scripts:

| Script | Description |
| ------ | ------ |
| freeling_analize.sh | Executes the Freeling analyzer for Spanish with the dependency annotation and the output CoNLL option |
| transformer_forms_conllu.py | Transforms the input documents (CoNLL-U format expected) into a txt file of sentences with the forms of each sentence ended with a full stop |
| transformer_conllu.py | Transforms the input documents (CoNLL 2006 format expected) into the CoNLL-U format |
| transformer_conllu_freeling.py | Transforms the input documents (CoNLL Freeling output format expected) into the CoNLL-U format |
| annotator.py | Exploits a CoNLL-U file in order to add new fields depending on rules |
| classifier.py | Creates two new folders to classify the sentences in a document depending on whether they contains a matched feature annotation or not |
| metrics.py | Generates a txt file containing statistical information on the annotations matched |


### Execution options:

* freeling_analize.sh
```sh
$ freeling_analize.sh -i <inputDirectory> -o <outputDirectory>
``` 
* transformer_forms_conllu.py
```sh
$ transformer_forms_conllu.py -i <inputDirectory> -o <outputDirectory>
``` 
* transformer_conllu.py
```sh
$ transformer_conllu.py -i <inputDirectory> -o <outputDirectory>
``` 
* transformer_conllu_freeling.py
```sh
$ transformer_conllu_freeling.py -i <inputDirectory> -o <outputDirectory>
``` 
* annotator.py
```sh
$ annotator.py -i <inputDirectory> -o <outputDirectory> -r <rulesfile> -p <orderOption>
``` 
* classifier.py
```sh
$ classifier.py -i <inputDirectoru> -u <UnmatchedOutputDirectory> -m <MatchedOutputDirectory>
``` 
* metrics.py
```sh
$ metrics.py -u <UnmatchedOutputDirectory> -a <MatchedOutputDirectory> -m <MetricsFile>
``` 


[Ancora corpus]: http://clic.ub.edu/corpus/es/ancora
[CEDEL2 corpus]: http://cedel2.learnercorpora.com/learners-english/
