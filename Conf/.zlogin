#!/bin/sh
#export GTK_IM_MODULE=fcitx
#export QT_IM_MODULE=fcitx
#export XMODIFIERS="@im=fcitx"

export PATH=$PATH:.

#if [ $UID == 1000 ]
#then
#export LANG=zh_CN.UTF-8
#export LC_ALL=zh_CN.UTF-8
 if [[ -z $DISPLAY && $XDG_VTNR -eq 1 ]]
 then
	 exec startx
 fi
#fi
