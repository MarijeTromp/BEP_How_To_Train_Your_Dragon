import itertools

# ---------------------------------------------------------------------------------------------------------------
# This script generates SLURM jobs to run Metropolis-Hastings experiments for the DHPC DelftBlue super computer
# ---------------------------------------------------------------------------------------------------------------

# Tips:
# 1. When selecting parameters, pay attention to the mutation name suffix! They indicate locality, i.e. end vs random
# 2. Check which modules are needed/available on DelftBlue, this is bound to change.
#         -> You can use the "module spider ___" to search for a module and its dependencies on DelftBlue


# Select here which values you want to vary
param_values: dict = {
    "type": ['metropolis_hastings'],
    "alpha": [1],
    "add_token_end": [30],
    "remove_token_end": [50],
    "add_loop_end": [10],
    "add_if_statement_end": [10],
    "start_over": [10]
}

# Select here what your default/control variables are
default_params = {
    "alpha": 1,
    "add_token_end": 30,
    "remove_token_end": 30,
    "add_loop_end": 30,
    "add_if_statement_end": 30,
    "start_over": 6
}

# Select whether you want to do a
#   1) grid search or
#   2) want to vary each param individually while keeping the rest the controlled.

# Option 1.
# param_search_space = [str({**default_params, k: v}) for k, vs in param_values.items() for v in vs]

# Option 2.
param_keys, param_values = zip(*param_values.items())
param_search_space = [str(dict(zip(param_keys, v))) for v in itertools.product(*param_values)]

# Select the domains you want to create a job for and how long they should be able to run
domains = ['robot', 'pixel', 'string']
durations = [1, 6, 12]

# Makes a script for each domain and parameter combination
for domain in range(len(domains)):
    for part in range(len(param_search_space)):
        i = domain * len(param_search_space) + part

        # You can do a more detailed config of the slurm job here:
        f = open("job%d.sh" % i, "w", newline='\n')
        f.write("#!/bin/sh\n")
        f.write("#SBATCH --partition=compute\n")
        f.write("#SBATCH --time=%d:00:00\n" % durations[domain])
        f.write("#SBATCH --ntasks=1\n")
        f.write("#SBATCH --cpus-per-task=32\n")
        f.write("#SBATCH --mem-per-cpu=4G\n")
        f.write("#SBATCH --job-name=job%d\n" % i)
        f.write("#SBATCH --output=out/job%dout.txt\n" % i)
        f.write("#SBATCH --error=out/job%derr.txt\n" % i)

        # Make sure to check which modules are currently needed/available
        f.write("module load 2022r1\n")
        f.write("module load compute\n")
        f.write("module load miniconda3/4.10.3-eyq4jvx\n")

        f.write("if [ ! -d \"/scratch/${USER}/conda_env\"]\n")
        f.write("then\n")
        f.write("    echo \"slurm: creating env\"\n")
        f.write("    conda env create --prefix=/scratch/${USER}/conda_env -f $HOME/conda_env.yml\n")
        f.write("else\n")
        f.write("    echo \"slurm: env already created\"\n")
        f.write("fi\n")

        f.write("source activate /scratch/${USER}/conda_env\n")
        f.write("export PYTHONPATH=$HOME\n")

        f.write("srun python -u $HOME/main.py \"" + domains[domain] + "\" \"" + param_search_space[part] + "\"\n")

# After uploading the job scripts, you can copy / paste the following in the terminal to submit all the jobs:
# x = _____ # Fill in how many jobs are created + 1
# for part in range(0,x):
#     print('sbatch job%d.sh' % part)