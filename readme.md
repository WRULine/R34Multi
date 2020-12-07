## Rule34 Multithreaded Downloader
##### A downloader for [rule34.xxx](https://rule34.xxx) allowing for multithreaded downloading of images/webms.
##### The downloader is supported on all platforms **however python3.6 or newer and python pip is needed**

## Install and run
##### [ubuntu/debian] `sudo apt install python3 python3-pip python3-tk`
##### `python3 -m pip install -r requirements.txt`
##### `python3 main.py [your command line arguments]`

## Command line arguments
##### `-allow-dupe` to disable skipping over already existing images
##### `-cli` uses the CLI interface instead of the GUI

## Recommended settings
##### Thread count: *50*
###### When using thread counts above 50 on regular images you may experience issues with downloads being randomly closed
##### Platform: *Linux/Unix Based Operating Systems*
##### Python Version: *Python 3.6 or newer* (Tested on Python 3.6.9)
