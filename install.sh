#!/usr/bin/env sh

apt install dos2unix
mv ./main.py /usr/bin/waitfor
chmod a+x /usr/bin/waitfor
dos2unix /usr/bin/waitfor
apt purge dos2unix