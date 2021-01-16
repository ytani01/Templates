#!/bin/sh -e
#
# Robot Music Box install script
#
#   (c) 2021 Yoichi Tanibayashi
#
############################################################
help() {
    cat <<'END'

[インストール後のディレクトリ構造]

 $HOME/ ... ホームディレクトリ
    |
    +- bin/ .. BINDIR シェルスクリプトなど
    |   |
    |   +- Mypkg .. WRAPPER_SCRIPT
    |   +- boot-Mypkg.sh .. 起動スクリプト
    |
    +- mypkg/ .. WORKDIR
    |   |
    |   +- log/
    |   |
    |   +- webroot/ .. WEBROOT
    |   |   |
    |   |   +- templates/
    |   |   +- static/
    |   |       |
    |   |       +- css/
    |   |       +- js/
    |   |       +- images/
    |   |       :
    |   |
    |   +- upload/
    |   +- data/
    |   :
    |
    +- env1/ .. python3 Virtualenv(venv) 【ユーザが作成する】
        |
        +- repo1/ .. MYDIR
        |   |
        |   +- build/ .. BUILD_DIR
        |
        +- subpackage1/
        |
        :

END
}

############################################################
MYNAME=`basename $0`
MYDIR=`dirname $0`


MY_PKG="mypkg"
WRAPPER_SCRIPT="Mypkg"


echo "MY_PKG=$MY_PKG"
echo "WRAPPER_SCRIPT=$WRAPPER_SCRIPT"

BINDIR="$HOME/bin"
mkdir -pv $BINDIR

WORKDIR="$HOME/$MY_PKG"
echo "WORKDIR=$WORKDIR"
mkdir -pv $WORKDIR

WEBROOT="$WORKDIR/webroot"
echo "WEBROOT=$WEBROOT"
mkdir -pv $WEBROOT

LOGDIR="$WORKDIR/log"
echo "LOGDIR=$LOGDIR"
mkdir -pv $LOGDIR

WRAPPER_SRC="$WRAPPER_SCRIPT.in"
echo "WRAPPER_SRC=$WRAPPER_SRC"

PKGS_TXT="pkgs.txt"

GITHUB_TOP="git@github.com:ytani01"

CUILIB_PKG="cuilib"
CUILIB_DIR="CuiLib"
CUILIB_GIT="${GITHUB_TOP}/${CUILIB_DIR}.git"

BUILD_DIR="$MYDIR/build"
mkdir -pv $BUILD_DIR

INSTALLED_FILE="$BUILD_DIR/installed"
echo -n > $INSTALLED_FILE

FAST_MODE=0

#
# fuctions
#
cd_echo() {
    cd $1
    echo "### [ `pwd` ]"
    echo
}

install_external_python_pkg() {
    _PKG=$1
    _DIR=$2
    _GIT=$3

    cd_echo $VIRTUAL_ENV

    echo "### install/update $_PKG"
    echo

    if [ ! -d $_DIR ]; then
        git clone $_GIT || exit 1
    fi

    cd_echo ./$_DIR
    git pull
    pip install .
    echo
}

usage() {
    echo
    echo "  Usage: $MYNAME [-u] [-h]"
    echo
    echo "    -f  fastmode"
    echo "    -u  uninstall"
    echo "    -h  show this usage"
    echo
}

uninstall() {
    cd_echo $MYDIR

    echo "### remove installed files"
    echo
    rm -f `cat $INSTALLED_FILE`
    echo

    echo "### uninstall my python package"
    echo
    pip uninstall -y $MY_PKG
    echo

    echo "### remove build/"
    echo
    rm -rfv build
}

#
# main
#
cd_echo $MYDIR
MY_VERSION=`python setup.py --version`
echo "MY_VERSION=$MY_VERSION"

MYDIR=`pwd`
echo "MYDIR=$MYDIR"
echo

while getopts fuh OPT; do
    case $OPT in
        f) FAST_MODE=1;echo "FAST_MODE=$FAST_MODE";;
        u) uninstall; exit 0;;
        h) usage; help; exit 0;;
        *) usage; exit 1;;
    esac
    shift
done

#
# install Linux packages
#
if [ -f $PKGS_TXT ]; then
    PKGS=`cat $PKGS_TXT`
    if [ ! -z $PKGS ]; then
        echo "### install Linux packages"
        echo
        sudo apt install `cat $PKGS_TXT`
        echo
    fi
fi

#
# venv
#
if [ -z $VIRTUAL_ENV ]; then
    while [ ! -f ./bin/activate ]; do
        cd ..
        if [ `pwd` = "/" ]; then
            echo
            echo "ERROR: Please create and activate Python3 Virtualenv(venv) and run again"
            echo
            echo "\$ cd ~"
            echo "\$ python -m venv env1"
            echo "\$ . ~/env1/bin/activate"
            echo
            exit 1
        fi
    done
    echo "### activate venv"
    . ./bin/activate
fi
cd_echo $VIRTUAL_ENV

#
# make $WRAPPER_SCRIPT
#
cd_echo $MYDIR

echo "### build $WRAPPER_SCRIPT"
sed -e "s?%%% MY_PKG %%%?$MY_PKG?" \
    -e "s?%%% MY_VERSION %%%?$MY_VERSION?" \
    -e "s?%%% VENVDIR %%%?$VIRTUAL_ENV?" \
    -e "s?%%% WORKDIR %%%?$WORKDIR?" \
    -e "s?%%% WEBROOT %%%?$WEBROOT?" \
    $WRAPPER_SRC > $BUILD_DIR/$WRAPPER_SCRIPT

chmod +x $BUILD_DIR/$WRAPPER_SCRIPT
echo $BUILD_DIR/$WRAPPER_SCRIPT >> $INSTALLED_FILE

echo '-----'
cat $BUILD_DIR/$WRAPPER_SCRIPT | sed -n -e '1,/\#* main/p'
echo '  :'
echo '-----'
echo

#
# install scripts
#
echo "### install scripts"
echo
cp -fv $BUILD_DIR/$WRAPPER_SCRIPT $BINDIR
echo $BINDIR/$WRAPPER_SCRIPT >> $INSTALLED_FILE
echo

#
# work dir
#
cd_echo $MYDIR/webroot
echo "### webroot"
echo
cp -rfv * $WEBROOT
echo

#
# update pip, setuptools, and wheel
#
if [ $FAST_MODE -lt 1 ]; then
    echo "### insall/update pip etc. .."
    echo
    pip install -U pip setuptools wheel
    hash -r
    echo
    pip -V
    echo
fi

#
# install my python packages
#
if [ $FAST_MODE -lt 1 ]; then
    install_external_python_pkg $CUILIB_PKG $CUILIB_DIR $CUILIB_GIT
fi

#
# install my package
#
cd_echo $MYDIR
echo "### install my python package"
echo
pip install .
echo

#
# display usage
#
echo "### usage"
echo
$WRAPPER_SCRIPT -h
echo
