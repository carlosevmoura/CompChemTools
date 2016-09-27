#!/bin/bash
#
# <bitbar.title>RSync Status</bitbar.title>
# <bitbar.version>v0.1</bitbar.version>
# <bitbar.author>Carlos Eduardo de Moura</bitbar.author>
# <bitbar.author.github>carlosevmoura</bitbar.author.github>
# <bitbar.desc>Synchronization status of remote folder</bitbar.desc>
# <bitbar.dependencies>Bash, RSync</bitbar.dependencies>
#
# RSync Status
# by Carlos Eduardo de Moura (@carlosevmoura)
#
SYNC_SERVER=" "
REMOTE_DIR=" "
LOCAL_DIR=" "
SERVER_NAME=" "

if [ "$1" == 'update' ]; then
    rsync --remove-source-files "$SYNC_SERVER":"$REMOTE_DIR"/* "$LOCAL_DIR"/ >& /dev/null
    rsync "$LOCAL_DIR"/Send/* "$SYNC_SERVER":"$REMOTE_DIR"/ >& /dev/null
    exit
fi

echo "⇊ | size=22"
echo '---'
TIMESTAMP=`date "+%d/%m/%Y (%H:%M:%S)"`
echo "$SERVER_NAME | terminal=false bash=$0 param1=update refresh=true"
echo "Updated in $TIMESTAMP"
