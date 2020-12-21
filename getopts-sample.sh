#!/bin/sh
#
echo $0
echo $*

while getopts ab:c OPT; do
    case $OPT in
        a) echo A
           ;;
        b) echo B
           echo $OPTARG
           shift
           ;;
        c) echo C
           ;;
        *) echo $OPT
    esac
    shift
done
echo $*
