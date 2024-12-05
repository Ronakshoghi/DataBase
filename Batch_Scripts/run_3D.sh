#!/bin/bash
# Bash script to fire new simulations once all 50 have converged

module load anaconda3
conda activate data_generation

for idx_start in {2934..2983..50}
do
  nrun=50
  while [ $nrun -gt 0 ]
  do
    nrun=$(squeue -u jschmidt87 -h -t pending,running -r | wc -l)
    echo "$nrun"
    sleep 30
  done
  python create_dataset_remote_6d.py -name KDEApproach5degRec -nt 50 \
  -ids $idx_start  \
  -dbp /storage/home/hcoda1/7/jschmidt87/scratch/KDEApproach5deg \
  -sp /storage/home/hcoda1/7/jschmidt87/scratch/KDEApproach5deg \
  -n_gpd 11 -n_epg 1 -t_to 300
  echo "I initiated 50 jobs starting from $idx_start"
done
