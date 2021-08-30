#!/usr/bin/zsh

for i in *.svg;
do
name=$(echo "$i" | cut -f 1 -d '.');
rsvg-convert "$i" > "$name.jpg" -d 100 -p 100 --keep-aspect-ratio;
done
