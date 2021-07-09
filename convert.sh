#!/usr/bin/zsh

for i in *.svg;
do
name=$(echo "$i" | cut -f 1 -d '.');
rsvg-convert "$i" > "$name.jpg" -w 1000 -h 1000;
done
