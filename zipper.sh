#!/usr/bin/env bash

set -e
set -x

DEFAULT_DATADIR="/JawTitan/EvalPlus/humaneval"

while getopts ":d:" opt; do
  case ${opt} in
    d )
      DATADIR=$OPTARG
      ;;
    \? )
      echo "Invalid option: -$OPTARG." 1>&2
      exit 1
      ;;
    : )
      echo "Option -$OPTARG requires an argument." 1>&2
      exit 1
      ;;
  esac
done

DATADIR=${DATADIR:-$DEFAULT_DATADIR}

# models=("codegen-2b" "codegen-6b" "codegen-16b" "vicuna-7b" "vicuna-13b" "stablelm-7b" "incoder-1b" "incoder-6b" "polycoder" "chatgpt" "santacoder" "gptneo-2b" "gpt-4")
models=("gpt-j", "starcoder" "codegen2-16b" "codegen2-3b" "codegen2-7b" "codegen2-1b")
temps=("0.0" "0.2" "0.4" "0.6" "0.8")

for model in "${models[@]}"; do
  for temp in "${temps[@]}"; do
    folder="${DATADIR}/${model}_temp_${temp}"
    if [ -d "$folder" ]; then
        # exclude files with ".json" or ".bak" suffixes
        zip -qr "${folder}.zip" "$folder" -x "*.json" "*.bak"
    else
      echo "Folder does not exist: $folder"
    fi
  done
done
