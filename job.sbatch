#!/bin/sh
#
#SBATCH --job-name="research_project"
#SBATCH --time=05:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem-per-cpu=4G
#SBATCH --output=out/%j_research_project.out
#SBATCH --error=out/%j_research_project.err

module load 2022r1
module load compute
module load miniconda3/4.10.3-eyq4jvx

#if conda_env does not exist create it
if [ ! -d "/scratch/${USER}/conda_env" ]
then
    echo "slurm: creating env"
    conda env create --prefix=/scratch/${USER}/conda_env -f $HOME/conda_env.yml
else
    echo "slurm: env already created"
fi

# Activate your environment
source activate /scratch/${USER}/conda_env

export PYTHONPATH=$HOME/

# Run your code
srun python -u $HOME/main.py