#!bin/bash
APP=fishfin
WORK_APP_NAME='fishfin'
PID=$APP.pid

#get server status
status() {
    echo

    if [ -f $PID ]
    then
        echo
        echo "Pid file: $( cat $PID ) [$PID]"
        echo
        ps -ef | grep $( cat $PID )
    else
        echo "No Pid file"
    fi
}



#start server
start() {
    if [ -f $PID ]
    then
        echo
        echo "already started. PID: [$( cat $PID )]"
    else
        echo "staring $PID ..."
        touch $PID
        if nohup gunicorn -k gevent --log-level=info -c gunicorn.conf app:app --preload 2>&1 &
        then echo $! >$PID
             echo "$(date '+%Y-%m-%d %X') : launch complete"
        else 
	     echo "Error... "
              /bin/rm $PID
        fi
    fi
}


#kill process command
kill_cmd() {
    SIGNAL=""; MSG="Killing "
    while true
    do
        LIST=`ps -ef | grep -v grep | grep $APP | grep $WORK_APP.wsgi | awk '{print $2}'`
        if [ "$LIST" ]
        then
            echo; echo "$MSG $LIST" ; echo
            echo $LIST | xargs kill $SIGNAL
            sleep 2
            SIGNAL="-9" ; MSG="Killing $SIGNAL"
            if [ -f $PID ]
            then
                /bin/rm $PID
            fi
        else
           echo; echo "All killed..." ; echo
           break
        fi
    done
}


#stop server
stop() {

    if [ -f $PID ]
    then
        if kill $( cat $PID )
        then echo "Done."
             echo "$(date '+%Y-%m-%d %X'): stopped"
        fi
        /bin/rm $PID
        kill_cmd
    else
        echo "No pid file. Already stopped?"
    fi
}


case "$1" in
    'start')
            start
            ;;
    'stop')
            stop
            ;;
    'restart')
            stop ; echo "Sleeping..."; sleep 1 ;
            start
            ;;
    'status')
            status
            ;;
    *)
            echo
            echo "Usage: $0 { start | stop | restart | status }"
            echo
            ;;
esac

