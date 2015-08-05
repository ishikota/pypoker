#!/bin/sh

fname=data_url.txt
while read line ; do
  wget -nc http://web.archive.org/web/${line}
done < ${fname}
