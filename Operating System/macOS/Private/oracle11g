#!/bin/bash

startDocker="N"
endDocker="N"
dockerRunERR=true

docker ps -a > /dev/null 2>&1
if [ "$?" == "0" ]; then
    docker ps | grep oracle11g > /dev/null 2>&1
    if [ "$?" != "0" ]; then
        docker start oracle11g > /dev/null 2>&1 &
        if [ "$?" == "0" ]; then
            dockerRunERR=false
            echo -n "Starting docker container "
            for ((i=0;i<5;i++))
            do
                echo -n "."
                sleep 2
            done
            echo " done"
        fi
    else
        dockerRunERR=false
    fi
elif [ "$?" == "127" ]; then
    echo -e "\n\033[31mERR\033[m: Fatal: This script must required Docker engine.\nPlease install Docker.app at ~/Applications."
    exit 127
fi
if [ $dockerRunERR == true ]; then
    echo -en "\033[33mWARN\033[m: Not running Docker engine detected. Launch Docker engine? (Y/n) > "
    read startDocker
    if [ "$startDocker" == "Y" -o "$startDocker" == "y" -o x$startDocker == x ]; then
        echo -n "Launching Docker engine "
        echo -n "."
    else
        echo -e "\n\033[31mERR\033[m: This script must required Docker engine."
        exit 1
    fi
    ls ~/Applications/Docker.app/Contents/MacOS/ 2> /dev/null | grep Docker > /dev/null
    if [ "$?" != "0" ]; then
        echo -e "\n\033[31mERR\033[m: Fatal: This script must required Docker.app."
        exit 1
    else
        ~/Applications/Docker.app/Contents/MacOS/Docker &
        echo -n "."
    fi
    sleep 2
    rm -f default.profraw 1
    for ((i=0;i<2;i++))
    do
        echo -n "."
        sleep 20
    done
    echo -n "."
    echo " done"
    docker ps | grep oracle11g > /dev/null
    if [ "$?" != "0" ]; then
        docker start oracle11g > /dev/null &
        echo -n "Starting docker container "
        for ((i=0;i<5;i++))
        do
            echo -n "."
            sleep 2
        done
        echo " done"
    fi
fi
if [ "$1" == "shell" ]; then
    docker exec -it oracle11g mysqlplus #bash #rlwrap sqlplus
    echo -en "\033[33mWARN\033[m: Terminate container and Docker engine? (y/N) > "
    read startDocker
    if [ "$startDocker" == "Y" -o "$startDocker" == "y" ]; then
        echo -n "Stopping docker container "
        docker stop oracle11g > /dev/null &
        for ((i=0;;i++))
        do
            docker ps | grep oracle11g > /dev/null
            if [ "$?" != "0" ]; then
                sleep 1
                killall Docker
                break
            fi
            echo -n "."
            sleep 2
        done
        echo " done"
        killall Docker
    else
        echo "Please stop container and engine manually."
    fi
else
    exit 1
fi
exit 0
