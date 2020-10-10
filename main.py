
import rule34 as r
import requests
import asyncio
import time as t
import threading

global threadcounter

search = input("Enter your Rule34 Search: ")
output = input("Output directory (realtive to launch location): ")

threadcount = int(input("Max Thread Count (0 for no limit):"))
if threadcount == 0:
    print("WARNING! This may cause your computer to slow down or even crash when dealing with high loads!\nRe-enter your limit to verify you want no thread limit")
    threadcount = int(input("Max Thread Count (0 for no limit):"))

def download(URL, md5, out, rule34=None):
    global threadcounter
    URL = URL[:21] + "/" + URL[21:] #Patch URL
    print("{} at {} started".format(md5, t.time()))
    myfile = requests.get(URL)
    open(output+ "/" + md5+"."+URL.split(".")[3], 'wb').write(myfile.content)
    print("{} at {} compleated".format(md5, t.time()))
    threadcounter -= 1

async def main(searchstr, output, threadlimit):
    originaltime = t.time()
    global threadcounter
    threadcounter = 0

    loop = asyncio.get_event_loop()
    rule34 = r.Rule34(asyncio.get_event_loop())
    zucc = await rule34.getImages(searchstr, singlePage=False)
    for x in zucc:
        while (threadcounter >= threadlimit and threadlimit != 0):
            print("Thread Limit Reached")
            await asyncio.sleep(0.1)
        t1 = threading.Thread(target=download, args=(x.file_url, x.md5, output, rule34))
        t1.start()
        threadcounter += 1
    print("finished at:{}".format(t.time() - originaltime))

asyncio.get_event_loop().run_until_complete(main(search,output, threadcount))
