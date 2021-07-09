#!/usr/bin/zsh

x=$(pwd);
cd /home/mmh97/anaconda3/bin;
source activate;
cd $x;

mkdir -p "source" "tactile";

for i in {1..1000};
do
python draw.py;
mv "test.jpg" "source/s_$i.jpg";
mv "test.svg" "tactile/t_$i.svg";
done
