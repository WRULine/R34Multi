#!/bin/sh
sudo apt install python3.7 python3-pip python-pip
mkdir out
python3.7 -m pip install rule34 asyncio requests
python3.7 main.py
