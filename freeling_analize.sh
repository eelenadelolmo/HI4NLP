cd txt && for file in *
do
	analyze -f es.cfg < "${file##*/}" > ../conll_freeling/"${file%.*}".conll --outlv dep --output conll
done


