salloc --gres=gpu:2 --cpus-per-task=4 --mem=150G --time=24:00:00
salloc --gres=gpu:1 --cpus-per-task=4 --mem=50G --time=12:00:00
srun --pty --overlap --jobid YOUR-JOBID bash
