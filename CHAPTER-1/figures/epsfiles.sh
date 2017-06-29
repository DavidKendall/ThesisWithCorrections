#!/bin/bash
for f in *.png
do
	NAME=`echo "$f" | cut -d'.' -f1`
	echo "Converting $f To $NAME.eps"
	/usr/bin/convert $f $NAME.eps
done

for f in *.jpg
do
	NAME=`echo "$f" | cut -d'.' -f1`
	echo "Converting $f To $NAME.eps"
	/usr/bin/convert $f $NAME.eps
done
