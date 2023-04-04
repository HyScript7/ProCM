#!/usr/bin/env sh
echo Downloading and installing CSS \& JS libraries and dependencies.

wget https://unpkg.com/@popperjs/core@2.11.6/dist/umd/popper.min.js
wget https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.min.js
mv ./*.min.js ./js/

wget https://github.com/twbs/bootstrap/archive/v5.2.2.zip
unzip ./v5.2.2.zip
mkdir ./sass/bootstrap
mv ./bootstrap-5.2.2/scss ./sass/bootstrap/scss
rm -frd ./bootstrap-5.2.2
rm ./v5.2.2.zip

wget https://github.com/twbs/icons/releases/download/v1.10.4/bootstrap-icons-1.10.4.zip
unzip ./bootstrap-icons-1.10.4.zip
mkdir ./css/icons
mv ./bootstrap-icons-1.10.4/* ./css/icons
rm -frd ./bootstrap-icons-1.10.4
rm ./bootstrap-icons-1.10.4.zip
