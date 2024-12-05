#!/bin/bash
nit=15   # how often should this script be run
nrun=14  # counts iterations of this script
ntex=500  # number of textures per iteration

module load anaconda3/
conda activate data_generation

while [ $nrun -lt $nit ]
do
  njobs=1 # counts slurm jobs running  
  idx_start=$(($nrun*$ntex))
  while [ $njobs -gt 0 ]
  do
    njobs=$(squeue -u jschmidt87 -h -t pending,running -r | wc -l)
    echo "$njobs"
    sleep 30
  done
  python create_dataset_remote.py -name KDEApproach5deg -nt $ntex \
  -ids $idx_start  \
  -dbp /storage/home/hcoda1/7/jschmidt87/scratch/KDEApproach5deg \
  -sp /storage/home/hcoda1/7/jschmidt87/scratch/KDEApproach5deg \
  -n_gpd 11 -n_epg 1 -t_to 300
  echo "I initiated $ntex jobs starting from $idx_start"
  #echo "index start is $idx_start" 
  nrun=$((nrun+1))
done
