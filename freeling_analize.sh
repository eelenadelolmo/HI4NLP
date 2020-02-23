cd CEDEL2/txt/CEDEL2_Q2 && for file in *
do
	analyze -f es.cfg < "${file##*/}" > ../../conll_CEDEL2/CEDEL2_Q2/"${file%.*}".conll --outlv dep --output conll
done


