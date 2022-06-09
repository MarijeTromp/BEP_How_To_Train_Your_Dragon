# import itertools

param_values: dict = {
    "alpha": [1],
    "add_token_end": [10, 20, 30, 40, 50],
    "remove_token_end": [10, 20, 30, 40, 50],
    "add_loop_end": [10, 20, 30, 40, 50],
    "add_if_statement_end": [10, 20, 30, 40, 50],
    "start_over": [2, 4, 6, 8, 10]
}

default_params = {
    "alpha": 1,
    "add_token_end": 30,
    "remove_token_end": 30,
    "add_loop_end": 30,
    "add_if_statement_end": 30,
    "start_over": 6
}

param_search_space = [str({**default_params, k: v}) for k, vs in param_values.items() for v in vs]
# param_keys, param_values = zip(*param_search_space.items())
# param_grid_space = [str(dict(zip(param_keys, v))) for v in itertools.product(*param_values)]


for part in range(len(param_search_space)):
    f = open("job%d.sh" % part, "w", newline='\n')
    f.write("#!/bin/sh\n")
    f.write("#SBATCH --partition=compute\n")
    f.write("#SBATCH --time=1:00:00\n")
    f.write("#SBATCH --ntasks=1\n")
    f.write("#SBATCH --cpus-per-task=32\n")
    f.write("#SBATCH --mem-per-cpu=4G\n")
    f.write("#SBATCH --job-name=job%d\n" % part)
    f.write("#SBATCH --output=out/job%dout.txt\n" % part)
    f.write("#SBATCH --error=out/job%derr.txt\n" % part)

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

    f.write("srun python -u $HOME/main.py \"robot\" \"" + param_search_space[part] + "\"\n")

# after uploading the jobscripts, you can copy / paste the following in the terminal to submit all the jobs:
# for part in range(0,26):
#     print('sbatch job%d.sh' % part)