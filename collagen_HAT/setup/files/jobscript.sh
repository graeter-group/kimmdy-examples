#!/bin/env bash
#SBATCH --job-name=kimmdy_run
#SBATCH --output=kimmdy_%j.o.log
#SBATCH --error=kimmdy_%j.e.log
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --mincpus=40
#SBATCH --exclusive
#SBATCH --cpus-per-task=1
#SBATCH --gpus=2
#SBATCH --partition=cascade.p

current_dir=$(basename "$(pwd)")

# Setup up your environment here
# modules.sh might load lmod modules, set environment variables, etc.
if [ -f ./_modules.sh ]; then
    source ./_modules.sh
fi

CYCLE=24
CYCLE_buffered=$(echo "scale=2; $CYCLE - 0.08" | bc)


START=$(date +"%s")

timeout ${CYCLE_buffered}h kimmdy -i kimmdy.yml --restart 

END=$(date +"%s")

LEN=$((END-START))
HOURS=$((LEN/3600 + 1))

echo "$LEN seconds ran"
echo "$HOURS full hours ran"

if [ $HOURS -lt $CYCLE ]; then
  echo "last cycle was just $HOURS h long, KIMMDY is done."
  exit 3
else
  echo "jobscript resubmitting"
  sbatch -J $current_dir ./jobscript.sh
  exit 2
fi
