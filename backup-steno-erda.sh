#!/bin/bash
SOURCE_DIR=~/lustre
TARGET_DIR=pulling_steno/lustre

LOGFILE=$HOME/erda-backup.log
LOCK=/tmp/primdal-backup.lock
REMOTE_NAME=io.erda.dk
echo "$(date): Starting Nightly Backup" >> $LOGFILE
(
    # Obtain exclusive lock, else exit
    flock -x -n 200 || exit 42
    
    # Start the backup
    lftp -e "set ssl:verify-certificate no; set ftp:ssl-protect-data on; mirror -Rvc $SOURCE_DIR ~/$TARGET_DIR; quit" -p 21 $REMOTE_NAME

    # remove the lockfile

) 200>$LOCK

# Get the exit code
EXIT=$?
# If exit code is 0, everything is good
if [ $EXIT -eq 0 ]
then
  echo "$(date): Nightly Backup Successful" >> $LOGFILE
# If exit code is 42 (we set that above), flock triggered
elif [ $EXIT -eq 42 ]
then
  echo "$(date): Script already running" >> $LOGFILE
else
  echo "$(date): Something went wrong" >> $LOGFILE
fi
