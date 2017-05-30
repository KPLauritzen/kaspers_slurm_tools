#!/usr/bin/env python
import os
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--scriptname',
                   help='filename of Python script to run')
parser.add_argument('--hours', default=336, type=int,
                   help='max hours to run')
parser.add_argument('--py_args', default='', help='Argurments to be passed to Python')
parser.add_argument('--submit', action='store_true', default=False,
                    help='Submit now!')
parser.add_argument('--array', action='store_true', default=False,
                    help="Use SLURM's array feature")
parser.add_argument('--partition', help='What queue to submit to', default='kemi_gemma3')
parser.add_argument('--jobname', default=None, type=str,
					help='Optional: Set jobname')
parser.add_argument('--mem_per_cpu', default=4000, type=int,
                    help="(4000 for gemma2, 16000 for gemma3)")
parser.add_argument('--no_scratch', action='store_true', help='Turn off scratch dir')
parser.add_argument('--mail', type=str, help="fail, end or all.", default='fail')
parser.add_argument('--interpreter', type=str, help="python or gpaw-python", default='python')
parser.add_argument('--n_cpus', default=1, type=int,
                    help='Number of CPUs to parallelize across')
parser.add_argument('--jobid', action='store_true', help='Send the SLURM jobid to the script')
args = parser.parse_args()
py_args = args.py_args

scriptpath = args.scriptname
assert os.path.exists(scriptpath), 'Script does not exists'
scriptname = os.path.basename(scriptpath)

interpreter = args.interpreter

# SET THIS TO YOUR EMAIL
user_email = 'user@example.com'

if args.mail == 'all':
    send_mail_on = 'all'
elif args.mail == 'end':
    send_mail_on = 'end'
else:
    send_mail_on = 'fail'

if args.jobname is None:
    jobname = scriptname[:-3]
else:
    jobname = args.jobname
maxtime = "{0}:00:00".format(args.hours)
partition = args.partition
mem_per_cpu = args.mem_per_cpu
int_mem_per_cpu = int(mem_per_cpu)
n_cpus = args.n_cpus
total_mem = mem_per_cpu * n_cpus
if args.no_scratch:
    use_scratch = 'false'
else:
    use_scratch = 'true'


if args.array:
    array_str = "--offset=${SLURM_ARRAY_TASK_ID}"
    jobid_str = "%A_%a"
    if args.jobid:
        jobid_python_args = "--jobid=${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}"
else:
    array_str = ""
    jobid_str = "%j"
    if args.jobid:
        jobid_python_args = "--jobid=${SLURM_JOB_ID}"
if not args.jobid:
    jobid_python_args = ""

sub_filename = 'submit.sl'
submit_string = """#!/bin/bash
#
#SBATCH --job-name={jobname}
#SBATCH -o $HOME/logs/{jobid_str}-{jobname}.out
#SBATCH -e $HOME/logs/{jobid_str}-{jobname}.err
#SBATCH --ntasks={n_cpus}
#SBATCH --nodes=1
#SBATCH --time={maxtime}
#SBATCH --mail-type={send_mail_on}
#SBATCH --mail-user={user_email}
#SBATCH --get-user-env
#SBATCH --partition={partition}
#SBATCH --mem={total_mem}

echo INPUT FILE:
cat {sub_filename}
echo ------------------
echo PWD
pwd
SUBMIT_DIR=`pwd`

use_scratch={use_scratch}
echo use_scratch = $use_scratch

if [ "$use_scratch" = 'true' ]; then
    PWD=`pwd`
    PPWD=$PWD
    echo Original dir: $PPWD
    # GOTO scratch dir
    cd $SCRATCH
    echo Current dir: $SCRATCH
fi

start=`date +%s`

srun -n{n_cpus} {interpreter} {scriptpath} {py_args} {array_str} {jobid_python_args}

end=`date +%s`
runtime=$(($end - $start))
elapsed="Elapsed: $(($runtime / 3600))hrs $((($runtime / 60) % 60))min $(($runtime % 60))sec"
echo $elapsed

if [ "$use_scratch" = 'true' ]; then
    cp * ${{PPWD}}
fi
""".format(**locals())

with open(sub_filename, 'w') as submit_file:
    submit_file.write(submit_string)


if args.submit:
    if args.array:
        print "You should edit {0} manually before submitting".format(sub_filename)
        print "Then run 'sbatch --array 0-200 {0}'".format(sub_filename)
    else:
        os.system('sbatch {0}'.format(sub_filename))
