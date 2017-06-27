# Kaspers tools for working on Steno with SLURM
The stuff I use daily on Steno.

# Installation
Clone this repository and place the scripts in your `$PATH` somewhere. For example:
``` bash
cd ~
mkdir -p ~/bin
git clone https://github.com/KPLauritzen/kaspers_slurm_tools.git ~/bin
echo export PATH=~/bin:$PATH >> .bashrc
source .bashrc
```

# Usage

## `myjobs`
Edit the `USERNAME` variable at the top of the script. Then just run this from the commandline to see all the jobs that you currently have submitted to the queue.

## `watch_myjobs`
Simply runs `myjobs` every 60 seconds. Also prints the total number of jobs you have running. 

## `squeue_cancel`
Expects to get piped in a list of jobs from `myjobs`, then cancels them. The smart thing is that you can fit a `grep` pipe inbetween. So you can do
```
myjobs | grep bad_jobs | squeue_cancel
```
and only cancel the jobs that match `bad_jobs`. 
## `request_interactive_compute`
Starts an interactive session on a compute node Running this with no argument, will request a session on `kemi_gemma3`. Running `request_interactive_compute 1` requests on `kemi_gemma` and running `request_interactive_compute 2` requests on `kemi_gemma2`.

## `submit.py`
The script I use to generate SLURM batch submit files. It is mostly geared towards running other Python scripts, but it could easily be changed to allow other sorts of programs to run. 

You can specify all the parameters you need as arguments to this scripts. For example:
```
python submit.py --scriptname='/kemi/primdal/scripts/somescript.py` --jobname test_script --partition kemi_gemma2 --py_args='--somescript_arg --additional_script_arg'
```
It is assumed that `$HOME/logs` exists for the output of the scripts. 

## `backup-steno-erda.sh`
This is run as a cron job nightly. 
It creates a lockfile when it runs so that only one backup job can run at a time. 

# Additional stuff
Save all commands you have ever run, and search through them with my other project: [Eternal history](https://github.com/KPLauritzen/eternalhistory) 

Check that your submissions are not misusing CPU or memory with [`sfree`](https://github.com/larsbratholm/sfree).