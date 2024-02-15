#!/bin/bash

while read samples; do
    echo "Processing: $samples"
    sanitized_results="$samples-sanitized"
    echo $sanitized_results
    if [ -d $sanitized_results ]; then
	    echo "$sanitized_results exist, skip"
    fi
done
