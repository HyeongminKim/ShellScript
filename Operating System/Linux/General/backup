#!/bin/bash

if [ "$1" == "help" ]; then
    echo "OVERVIEW : This script will backup $HOME and $HOME/Documents, $HOME/.local/etc will save $HOME/Desktop"
    echo "USAGE : $0 [backup@example.com] [ssh port (default port 22)]"
    exit 0
fi
rm ~/Desktop/StudyBackup.tgz 2> /dev/null
rm ~/Desktop/Documents.tgz 2> /dev/null
rm ~/Desktop/etc.tgz 2> /dev/null
sleep 2
tar zcvf ~/Desktop/StudyBackup.tgz $HOME > /dev/null
tar zcvf ~/Desktop/Documents.tgz $HOME/Documents > /dev/null
tar zcvf ~/Desktop/etc.tgz $HOME/.local/etc > /dev/null
sleep 2
if [ x$1 == x ]; then
    echo "USAGE : $0 [backup@example.com] [ssh port (default port 22)]"
    echo -n "Would you like add target backup server? (Y/n) > "
    read input
    if [ "$input" == "Y" -o "$input" == "y" -o x$input == x ]; then
        echo -n "Please insert target ip address. > "
        read target
        echo -n "Please insert target port number. > "
        read port
        if [ x$target == x ]; then
            echo "Abort. "
            exit 1
        elif [ x$port == x -o "$port" == "22" ]; then
            echo "Please insert $target password. using scp(port: 22)"
            scp ~/Desktop/StudyBackup.tar.gz ~/Desktop/Documents.tar.gz ~/Desktop/etc.tar.gz $target:~/Desktop
            if [ "$?" == "0" ]; then
                echo "Target $target backup successful. Check ~/Desktop folder."
                rm ~/Desktop/StudyBackup.tar.gz ~/Desktop/Documents.tar.gz ~/Desktop/etc.tar.gz
            else
                echo "Target $target backup failed. Please copy backup file manually. "
                echo "Backup path is $HOME/Desktop"
                exit 1
            fi
        else
            echo "Please insert $target password. using scp(port: $port)"
            scp -P $port ~/Desktop/StudyBackup.tar.gz ~/Desktop/Documents.tar.gz ~/Desktop/etc.tar.gz $target:~/Desktop
            if [ "$?" == "0" ]; then
                echo "Target $target backup successful. Check ~/Desktop folder."
                rm ~/Desktop/StudyBackup.tar.gz ~/Desktop/Documents.tar.gz ~/Desktop/etc.tar.gz
            else
                echo "Target $target backup failed. Please copy backup file manually. "
                echo "Backup path is $HOME/Desktop"
                exit 1
            fi
        fi
    else
        echo "Null target ip address. Please copy backup file manually. "
        echo "Backup path is $HOME/Desktop"
        exit 0
    fi
elif [ "$1" == "override" ]; then
    echo "Backup path is $HOME/Desktop"
    exit 0
elif [ x$2 != x ]; then
    echo "Please insert $1 password. using scp(port: $2)"
    scp -P $2 ~/Desktop/StudyBackup.tar.gz ~/Desktop/Documents.tar.gz ~/Desktop/etc.tar.gz $1:~/Desktop
    if [ "$?" == "0" ]; then
        echo "Target $1 backup successful. Check ~/Desktop folder."
        rm ~/Desktop/StudyBackup.tar.gz ~/Desktop/Documents.tar.gz ~/Desktop/etc.tar.gz
    else
        echo "Target $1 backup failed. Please copy backup file manually. "
        echo "Backup path is $HOME/Desktop"
        exit 1
    fi
else
    echo "Please insert $1 password. using scp(port: 22)"
    scp ~/Desktop/StudyBackup.tar.gz ~/Desktop/Documents.tar.gz ~/Desktop/etc.tar.gz $1:~/Desktop
    if [ "$?" == "0" ]; then
        echo "Target $1 backup successful. Check ~/Desktop folder."
        rm ~/Desktop/StudyBackup.tar.gz ~/Desktop/Documents.tar.gz ~/Desktop/etc.tar.gz
    else
        echo "Target $1 backup failed. Please copy backup file manually. "
        echo "Backup path is $HOME/Desktop"
        exit 1
    fi
fi
