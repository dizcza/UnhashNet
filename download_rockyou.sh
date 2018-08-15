#!/usr/bin/env bash

echo "Downloading rockyou.txt"
wget https://downloads.skullsecurity.org/passwords/rockyou.txt.bz2
bzip2 -d rockyou.txt.bz2

echo "Leave words starting with 'a' or 'b' to 'abrockyou.txt'"
grep "^a\|^b" rockyou.txt | shuf -n 100000 -o abrockyou.txt

echo "Making MD5 hashes to 'abrockyou.md5'. This takes about 1 minute."
while read line; do
    echo $line | md5sum | cut -f1 -d' ';
done < abrockyou.txt > abrockyou.md5

echo "Done! You can run 'python main.py'"