# Installation:
pip install -r requiremets.txt

# Corpus processed:

AnCora Surface Syntax Dependencies
published in 2014
at UPF (GLiCom)
by Benjamin Kolz, Toni Badia and Roser Saurí

Syntax information, which is crucial in many NLP tools, can be represented by means of constituent structures or dependency relations. 
While each of these formalisms has its advantages and disadvantages and there is an ongoing debate on preferred uses of them, it is worth noting that dependency-based 
representations can also vary depending on the linguistic criteria they are based upon: from purely syntactically oriented to semantically motivated. 
Most current approaches to dependency functions within NLP embrace an (at least partial) semantic orientation, 
e.g., most notably, the Stanford parser and, in the case of Spanish, the AnCora corpus and any parser trained on that. 
By contrast, the current resource presents a corpus of dependency relations for Spanish based on purely syntactic criteria.
Therefore we decided to name this corpus 'AnCora Surface Syntax Dependencies'.

For further information see:
"From constituents to syntax-oriented dependencies"
published in SEPLN, march 2014
ISSN 1135-5948
© 2014 Sociedad Española para el Procesamiento del Lenguaje Natural



# Execute transformer_conllu.py:

Options:

-i The directory where the input files are.
-o The directory where the conllu files will be saved.
  
# Execute annotator.py:

# Execute classifier.py:

# Execute metrics.py:

# Execute transformer_txt.py:
