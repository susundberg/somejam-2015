#!/bin/sh
set -e

pip freeze | grep -v "argparse==" | grep -v "chardet==" | grep -v "colorama==" | grep -v "html5lib==" |grep -v "six=="|grep -v "urllib3==" > requirements.txt
