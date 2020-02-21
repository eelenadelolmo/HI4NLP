cd txt && for file in *
do
	analyze -f es.cfg < "${file##*/}" > ../freeling/"${file%.*}".conll --outlv dep --output conll
done


