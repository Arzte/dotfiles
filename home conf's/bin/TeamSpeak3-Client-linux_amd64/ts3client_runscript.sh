#!/bin/bash

export KDEDIRS=
export KDEDIR=
export QTDIR=.
export QT_PLUGIN_PATH=.
export LD_LIBRARY_PATH=".:$LD_LIBRARY_PATH"

D1=$(readlink -f "$0")
D2=$(dirname "${D1}")
cd "${D2}"

if [ -e ts3client_linux_x86 ]; then
	./ts3client_linux_x86 $@
else
	./ts3client_linux_amd64 $@
fi
