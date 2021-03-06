#!/usr/bin/env bash

# script to help with BS

# Dependencies:
# - functions

# Save trace setting
XTRACE=$(set +o | grep xtrace)
set -x

# Keep track of this directory
SCRIPT_DIR=$(cd $(dirname "$0") && pwd)
BASE_DIR=${BASE_DIR:-$SCRIPT_DIR/..}
CONFIG=${CONFIG:-$BASE_DIR/etc/billingstack/billingstack.conf}

SCREEN_NAME=${SCREEN_NAME:-billingstack}
SCREEN_LOGDIR=${SCREEN_LOGDIR:-$BASE_DIR/logs}
SCREENRC=$BASE_DIR/$SCREEN_NAME-screenrc
USE_SCREEN=$(trueorfalse True $USE_SCREEN)

SERVICE_DIR=${SERVICE_DIR:-$BASE_DIR/status}

SERVICES="api,central,rater,biller,collector"

function ensure_dir() {
    local dir=$1
    [ ! -d "$dir" ] && {
        echo "Attempting to create $dir"
        mkdir -p $dir
    }
}


# Normalize config values to True or False
# Accepts as False: 0 no false False FALSE
# Accepts as True: 1 yes true True TRUE
# VAR=$(trueorfalse default-value test-value)
function trueorfalse() {
    local default=$1
    local testval=$2

    [[ -z "$testval" ]] && { echo "$default"; return; }
    [[ "0 no false False FALSE" =~ "$testval" ]] && { echo "False"; return; }
    [[ "1 yes true True TRUE" =~ "$testval" ]] && { echo "True"; return; }
    echo "$default"
}


# _run_process() is designed to be backgrounded by run_process() to simulate a
# fork.  It includes the dirty work of closing extra filehandles and preparing log
# files to produce the same logs as screen_it().  The log filename is derived
# from the service name and global-and-now-misnamed SCREEN_LOGDIR
# _run_process service "command-line"
function _run_process() {
    local service=$1
    local command="$2"

    # Undo logging redirections and close the extra descriptors
    exec 1>&3
    exec 2>&3
    exec 3>&-
    exec 6>&-

    if [[ -n ${SCREEN_LOGDIR} ]]; then
        exec 1>&${SCREEN_LOGDIR}/screen-${1}.${CURRENT_LOG_TIME}.log 2>&1
        ln -sf ${SCREEN_LOGDIR}/screen-${1}.${CURRENT_LOG_TIME}.log ${SCREEN_LOGDIR}/screen-${1}.log

        # TODO(dtroyer): Hack to get stdout from the Python interpreter for the logs.
        export PYTHONUNBUFFERED=1
    fi

    exec /bin/bash -c "$command"
    die "$service exec failure: $command"
}


# run_process() launches a child process that closes all file descriptors and
# then exec's the passed in command.  This is meant to duplicate the semantics
# of screen_it() without screen.  PIDs are written to
# $SERVICE_DIR/$SCREEN_NAME/$service.pid
# run_process service "command-line"
function run_process() {
    local service=$1
    local command="$2"

    # Spawn the child process
    _run_process "$service" "$command" &
    echo $!
}



# Helper to launch a service in a named screen
# screen_it service "command-line"
function screen_it {

    if is_service_enabled $1; then
        # Append the service to the screen rc file
        screen_rc "$1" "$2"

        if [[ "$USE_SCREEN" = "True" ]]; then
            screen -S $SCREEN_NAME -X screen -t $1

            if [[ -n ${SCREEN_LOGDIR} ]]; then
                screen -S $SCREEN_NAME -p $1 -X logfile ${SCREEN_LOGDIR}/screen-${1}.${CURRENT_LOG_TIME}.log
                screen -S $SCREEN_NAME -p $1 -X log on
                ln -sf ${SCREEN_LOGDIR}/screen-${1}.${CURRENT_LOG_TIME}.log ${SCREEN_LOGDIR}/screen-${1}.log
            fi

            # sleep to allow bash to be ready to be send the command - we are
            # creating a new window in screen and then sends characters, so if
            # bash isn't running by the time we send the command, nothing happens
            sleep 1.5

            NL=`echo -ne '\015'`
            screen -S $SCREEN_NAME -p $1 -X stuff "$2 || touch \"$SERVICE_DIR/$SCREEN_NAME/$1.failure\"$NL"
        else
            # Spawn directly without screen
            run_process "$1" "$2" >$SERVICE_DIR/$SCREEN_NAME/$service.pid
        fi
    fi
}


# Screen rc file builder
# screen_rc service "command-line"
function screen_rc {
    if [[ ! -e $SCREENRC ]]; then
        # Name the screen session
        echo "sessionname $SCREEN_NAME" > $SCREENRC
        # Set a reasonable statusbar
        echo "hardstatus alwayslastline '$SCREEN_HARDSTATUS'" >> $SCREENRC
        echo "screen -t shell bash" >> $SCREENRC
    fi
    # If this service doesn't already exist in the screenrc file
    if ! grep $1 $SCREENRC 2>&1 > /dev/null; then
        NL=`echo -ne '\015'`
        echo "screen -t $1 bash" >> $SCREENRC
        echo "stuff \"$2$NL\"" >> $SCREENRC
    fi
}

# Uses global ``ENABLED_SERVICES``
# is_service_enabled service [service ...]
function is_service_enabled() {
    services=$@
    return 0
}


function screen_setup() {

    # Set up logging of screen windows
    # Set ``SCREEN_LOGDIR`` to turn on logging of screen windows to the
    # directory specified in ``SCREEN_LOGDIR``, we will log to the the file
    # ``screen-$SERVICE_NAME-$TIMESTAMP.log`` in that dir and have a link
    # ``screen-$SERVICE_NAME.log`` to the latest log file.
    # Logs are kept for as long specified in ``LOGDAYS``.
    if [[ -n "$SCREEN_LOGDIR" ]]; then

        # We make sure the directory is created.
        if [[ -d "$SCREEN_LOGDIR" ]]; then
            # We cleanup the old logs
            find $SCREEN_LOGDIR -maxdepth 1 -name screen-\*.log -mtime +$LOGDAYS -exec rm {} \;
        else
            ensure_dir $SCREEN_LOGDIR
        fi
    fi

    if [[ ! -d "$SERVICE_DIR/$SCREEN_NAME" ]]; then
        mkdir -p "$SERVICE_DIR/$SCREEN_NAME"
    fi

    USE_SCREEN=$(trueorfalse True $USE_SCREEN)
    if [[ "$USE_SCREEN" == "True" ]]; then
        # Create a new named screen to run processes in
        screen -d -m -S $SCREEN_NAME -t shell -s /bin/bash
        sleep 1

        # Set a reasonable status bar
        if [ -z "$SCREEN_HARDSTATUS" ]; then
            SCREEN_HARDSTATUS='%{= .} %-Lw%{= .}%> %n%f %t*%{= .}%+Lw%< %-=%{g}(%{d}%H/%l%{g})'
        fi
        screen -r $SCREEN_NAME -X hardstatus alwayslastline "$SCREEN_HARDSTATUS"
    fi

    # Clear screen rc file
    SCREENRC=$BASE_DIR/$SCREEN_NAME-screenrc
    if [[ -e $SCREENRC ]]; then
        echo -n > $SCREENRC
    fi
}


screen_is_running() {
    # Check to see if we are already running DevStack
    # Note that this may fail if USE_SCREEN=False
    if type -p screen >/dev/null && screen -ls | egrep -q "[0-9].$SCREEN_NAME"; then
        echo "Already running a session."
        echo "To rejoin this session type 'screen -x $SCREEN_NAME'."
        echo "To destroy this session, type './$0 stop'."
        exit 1
    fi
}


function screen_destroy() {
    SCREEN=$(which screen)
    if [[ -n "$SCREEN" ]]; then
        SESSION=$(screen -ls | awk '/[0-9].billingstack/ { print $1 }')
        if [[ -n "$SESSION" ]]; then
            screen -X -S $SESSION quit
        fi
    fi

    rm -f "$SERVICE_DIR/$SCREEN_NAME"/*.failure
}


function start_svc() {
    svc="$(echo "$1" | sed 's/bs-//')"
    echo "Starting service: $svc"
    screen_it bs-$svc "billingstack-$svc --config-file $CONFIG"
}



function start() {
    local svc=$1

    [ "$svc" == 'all' ] && {
        for s in $(echo "$SERVICES" | tr ',' ' '); do
            start_svc $s
        done
        return
    }
    start_svc $svc
}


case $1 in
    start)
        screen_is_running
        screen_setup

        svc=$2
        [ -z "$svc" ] && svc=all
        echo "Starting service(s): $svc"
        start $svc
    ;;
    stop)
        screen_destroy
    ;;
esac
