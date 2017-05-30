#!/bin/bash

partition_no=${1:-3}
if [ $partition_no -eq 1 ]
then
	partition_no=""
fi
srun --partition kemi_gemma${partition_no} --pty bash
