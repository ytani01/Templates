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
    +- bin/ ... シェルスクリプトなど
    |   |
    |   +- Mypkg
    |   +- boot-Mypkg.sh ... 起動スクリプト
    |
    +- env1/  ... python3 Virtualenv(venv) 【ユーザが作成する】
        |
        +- repo1/ ... git repository
        |
        :

END
}

############################################################
MYNAME=`basename $0`
MYDIR=`dirname $0`


WRAPPER_SCRIPT="Mypkg1"


WRAPPER_SRC="$WRAPPER_SCRIPT.in"
MY_PKG=`echo $WRAPPER_SCRIPT | tr "A-Z" "a-z"`

echo "WRAPPER_SCRIPT=$WRAPPER_SCRIPT"
echo "WRAPPER_SRC=$WRAPPER_SRC"
echo "MY_PKG=$MY_PKG"

PKGS_TXT="pkgs.txt"

GITHUB_TOP="git@github.com:ytani01"

CUILIB_PKG="cuilib"
CUILIB_DIR="CuiLib"
CUILIB_GIT="${GITHUB_TOP}/${CUILIB_DIR}.git"

BINDIR="$HOME/bin"
mkdir -pv $BINDIR

BUILD_DIR="$MYDIR/build"
mkdir -pv $BUILD_DIR

INSTALLED_FILE="$BUILD_DIR/installed"
echo -n > $INSTALLED_FILE

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

    cd_echo $_DIR
    git pull
    pip install .
    echo
}

usage() {
    echo
    echo "  Usage: $MYNAME [-u] [-h]"
    echo
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
MYDIR=`pwd`
echo "MYDIR=$MYDIR"
echo

while getopts uh OPT; do
    case $OPT in
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
    . ../bin/activate
fi
cd_echo $VIRTUAL_ENV

#
# make $WRAPPER_SCRIPT
#
cd_echo $MYDIR

echo "### build $WRAPPER_SCRIPT"
sed -e "s?%%% MY_PKG %%%?$MY_PKG?" \
    $WRAPPER_SRC > $BUILD_DIR/$WRAPPER_SCRIPT

echo '-----'
cat $BUILD_DIR/$WRAPPER_SCRIPT | sed -n -e '1,/\#* main/p'
echo '  :'
echo

#
# install scripts
#
echo "### install scripts"
echo
cp -fv $BUILD_DIR/$WRAPPER_SCRIPT $BINDIR
echo $BUILD_DIR/$WRAPPER_SCRIPT >> $INSTALLED_FILE
echo

#
# update pip, setuptools, and wheel
#
echo "### insall/update pip etc. .."
echo
pip install -U pip setuptools wheel
hash -r
echo
pip -V
echo

#
# install my python packages
#
install_external_python_pkg $CUILIB_PKG $CUILIB_DIR $CUILIB_GIT

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
