
import rule34 as r
import requests
import asyncio
import time as t
import threading

search = input("Enter your Rule34 Search: ")

def download(URL, md5):
    print("{} at {} started".format(md5, t.time()))
    #rule34 = r.Rule34(asyncio.get_event_loop())
    #rule34.download(URL)
    myfile = requests.get(URL)
    open("out/" + md5+"."+URL.split(".")[3], 'wb').write(myfile.content)
    #print()

    print("{} at {} compleated".format(md5, t.time()))


async def test(searchstr):
    originaltime = t.time()
    rule34 = r.Rule34(asyncio.get_event_loop())
    #rule34 = r.Sync()
    zucc = await rule34.getImages(searchstr, singlePage=False)
    for x in zucc:
        #await download(x.file_url, x.md5)
        t1 = threading.Thread(target=download, args=(x.file_url, x.md5))
        t1.start()
    print ("finished at:{}".format(t.time() - originaltime))

async def main(srh):
    await test(srh)

asyncio.get_event_loop().run_until_complete(main(search))
#asyncio.run(main(search))