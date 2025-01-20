#!/bin/bash
#SBATCH --job-nam=CYL_Array_Test		#  Job name
#SBATCH --account=gts-skalidindi7               # charge account
#SBATCH -N1 --ntasks-per-node=8                 # Number of nodes and cores per node required
#SBATCH --mem-per-cpu=8G                        # Memory per core
#SBATCH -t1:00:00                               # Duration of the job (Ex: 15 mins)
#SBATCH -qembers                                # QOS Name
#SBATCH -oReport-%A_%a.out     			# Combined output and error messages file
#SBATCH --mail-type=FAIL	                # Mail preferences
#SBATCH --mail-user=jschmidt87@gatech.edu       # E-mail address for notifications
cd $SLURM_SUBMIT_DIR                            # Change to working directory

threshold=0
txdone=$(($threshold+$SLURM_ARRAY_TASK_COUNT*$2*$1))
idx_start=$((($SLURM_ARRAY_TASK_ID-1)*$2+$txdone))

echo "Task_ID: $SLURM_ARRAY_TASK_ID"
echo "Iteration: $1"
echo "Tetures to calc: $2"
echo "Textures done: $txdone"
echo "StartIdx $idx_start"
echo "FinalIdx $(($idx_start+$2))"

module load anaconda3
module load matlab/r2023a
conda activate data_generation
export LD_PRELOAD="/usr/local/pace-apps/manual/packages/matlab/r2023a/bin/glnxa64/glibc-2.17_shim.so"
module load fftw
python /storage/home/hcoda1/7/jschmidt87/software/DataBase/src/CYL_remote.py -start $idx_start -n $2 -st /storage/home/hcoda1/7/jschmidt87/scratch/KDEApproach5deg/CYL/textures_success.json -pm /storage/home/hcoda1/7/jschmidt87/software/mtex-5.10.2 -ps /storage/home/hcoda1/7/jschmidt87/scratch/KDEApproach5deg -pt /storage/home/hcoda1/7/jschmidt87/scratch/KDEApproach5deg/TextureFiles -rj /storage/home/hcoda1/7/jschmidt87/scratch/KDEApproach5deg/CYL/recreate_cyl_keys.json

