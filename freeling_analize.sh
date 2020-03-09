#!/bin/bash
 
while [ -n "$1" ]; do
 
    case "$1" in

    -i)
        param="$2"
        echo "-i option passed, with value $param"
        cd $param
        shift
        ;;

    -o)
        param="$2"
        echo "-o option passed, with value $param"
        for file in *
            do
                analyze -f es.cfg < "${file##*/}" > $param"${file%.*}".conll --outlv dep --output conll
            done
        shift
        ;;
    --)

        shift # The double dash makes them parameters
 
        break
        ;;
 
    *) echo "Option $1 not recognized" ;;
 
    esac
 
    shift
 
done