# qtbackport-script

A backport script for preparing and uploading the qt sources to the PPA.

# How to use
First, you need python3 ofc. And then run the command below:
```bash
# optional, create the virtual environment to prevent your system from being dirty :)
$ python -m venv venv
# optional, activating your virtual environment (depends on your shell)
$ source venv/bin/activate
# Install the pip dependencies
$ pip install -r requirements.txt
# adding "deb-src" stuff if you needed
$ vim /etc/apt/sources.list.d/qt_backport.list
# create work directory
$ mkdir build && cd build
# We are good now :)
$ python backport_script.py
```
You must first prepare the sources with the "nodoc" option and then the "doc" one. You could also add extra packages by entering their source packages' names, for example, "qtmultimedia-opensource-src."
