#!/bin/sh
sudo apt install python3 python3-pip
mkdir out
python3 -m pip install rule34 asyncio requests
python3 main.py
