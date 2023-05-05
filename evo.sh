#!/usr/bin/env bash

set -e
set -x

# Set default values for DATADIR and NCORES
DEFAULT_DATADIR="/JawTitan/EvalPlus/humaneval"
DEFAULT_NCORES=$(nproc)
DEFAULT_JUST_RUN=0

# Check if the user has provided a custom value for DATADIR and NCORES
while getopts ":d:n:" opt; do
  case ${opt} in
    d )
      DATADIR=$OPTARG
      ;;
    n )
      NCORES=$OPTARG
      ;;
    j )
      JUST_RUN=1
      ;;
    \? )
      echo "Invalid option: -$OPTARG. Example: bash evo.sh -d /path/to/humaneval -n 32" 1>&2
      exit 1
      ;;
    : )
      echo "Option -$OPTARG requires an argument. Example: bash evo.sh -d /path/to/humaneval -n 32" 1>&2
      exit 1
      ;;
  esac
done

# Set DATADIR and NCORES to default values if they are not provided by the user
DATADIR=${DATADIR:-$DEFAULT_DATADIR}
NCORES=${NCORES:-$DEFAULT_NCORES}
JUST_RUN=${JUST_RUN:-$DEFAULT_JUST_RUN}

export PYTHONPATH=$(pwd)

models=("codegen-2b" "codegen-6b" "codegen-16b" "vicuna-7b" "vicuna-13b" "stablelm-7b" "incoder-1b" "incoder-6b" "polycoder" "chatgpt" "santacoder" "gptneo-2b" "gpt-4")
temps=("0.0" "0.2" "0.4" "0.6" "0.8")

if [ $JUST_RUN -eq 0 ]; then
  echo "Experiements won't run from scratch since JUST_RUN is set to 0. To run and override all experiements, add -j flag."
else
  echo "Experiements will run from scratch since JUST_RUN is set to 1. To run without overriding all experiements, remove -j flag."
fi

for model in "${models[@]}"; do
  for temp in "${temps[@]}"; do
    folder="${DATADIR}/${model}_temp_${temp}"
    if [ -d "$folder" ]; then
      if [ $JUST_RUN -eq 1 ]; then
        yes | python3 evalplus/evaluate.py --dataset humaneval --samples "$folder" --parallel ${NCORES} --i-just-wanna-run --full
      else
        python3 evalplus/evaluate.py --dataset humaneval --samples "$folder" --parallel ${NCORES} --full
      fi
    else
      echo "Folder does not exist: $folder"
    fi
  done
done
