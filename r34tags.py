from xml.dom import minidom
import rule34 as r
import requests
import asyncio
import time as t
import threading
import os
import easygui
from tkinter import *
import r34tags as rtag

global SSVar
global SRVar
global NCVar
global PVVar
global SIVar
global OOVar
global tagCache
tagCache = {}

class r34tags():
    def __init__(self, site):
        self.site = site
    def getTag(self, tagName):
        return requests.get("https://{}/index.php?page=dapi&s=tag&q=index&name={}".format(self.site, tagName)).content
    def getType(self, xmlData):
        xmlData = xmlData.decode()
        xmlData = xmlData.replace("\n", "")
        dataXML = minidom.parseString(xmlData)
        items = dataXML.getElementsByTagName('tag')
        return items[0].attributes['type'].value


def patchURL(url):
    if url.split(".")[0] == "https://us" or url.split(".")[0] == "https://hk" or url.split(".")[0] == "https://ny":
        URL = url[:21] + "/" + url[21:]
    elif url.split(".")[0] == "https://img":
        URL = url[:22] + "/" + url[22:]
    elif url.split(".")[0] == "https://cali":
        URL = url[:23] + "/" + url[23:]
    elif url.split(".")[0] == "https://miami":
        URL = url[:24] + "/" + url[24:]
    else:
        URL = url
    return URL

def secureDownload(url):
    myfile = None
    while myfile == None:
        try:
            myfile = requests.get(url)
        except:
            print("Error in file download, retrying")
            myfile = None
    return myfile

def downloadLITE(URL, md5, out): # Smaller Download function
    global threadcounter
    URL = patchURL(URL)  # Patch URL
    if not os.path.isfile(out + "/" + md5 + "." + URL.split(".")[3]) or "-allow-dupe" in sys.argv:
        myfile = secureDownload(URL)
        open(out + "/" + md5 + "." + URL.split(".")[3], 'wb').write(myfile.content)
    threadcounter -= 1

def download(URL, md5, out, r34, r34tag, creatorID, CLI, originalorder):
    global threadcounter
    global tagCache
    global SSVar
    global SRVar
    global NCVar
    global OOVar
    URL = patchURL(URL)  # Patch URL
    if not os.path.isfile(out + "/" + md5 + "." + URL.split(".")[3]) or "-allow-dupe" in sys.argv:
        if creatorID == None or (creatorID != None and r34.creator_ID == creatorID):
            myfile = secureDownload(URL)
            if SSVar.get() == SRVar.get():
                open(out + "/" + md5 + "." + URL.split(".")[3], 'wb').write(myfile.content)
            elif SSVar.get() == 1:
                open(out + "/" + str(r34.score) + "-" + md5 + "." + URL.split(".")[3], 'wb').write(myfile.content)
            elif SRVar.get() == 1:
                open(out + "/" + str((r34.width + r34.height)) + "-" + md5 + "." + URL.split(".")[3], 'wb').write(myfile.content)
            elif OOVar.get() == 1:
                open(out + "/" + str(originalorder) + "-" + md5 + "." + URL.split(".")[3], 'wb').write(myfile.content)
            else:
                raise ("Unidentified Value")


    threadcounter -= 1


async def main(searchstr, output, threadlimit, creatorID=None, CLI=True):
    try:
        os.mkdir(output)
    except Exception as e:
        print(e)

    print("FULL DEBUG BEGIN")
    r34tag = rtag.r34tags("rule34.xxx")
    originaltime = t.time()
    global threadcounter
    global downloadCounter
    global PVVar
    global SIVar
    global OOVar
    global NCVar
    downloadCounter = 0
    threadcounter = 0

    loop = asyncio.get_event_loop()
    rule34 = r.Rule34(loop)

    sys.stdout.write("\rGrabbing image list: {}            ".format(t.time() - originaltime))
    sys.stdout.flush()

    if NCVar.get() == 1:
        searchstr = searchstr + " original*"

    imageList = None

    while imageList == None:
        try:
            imageList = await rule34.getImages(searchstr, singlePage=False)
        except:
            print("\nError in image list, retrying")
            imageList = None

    sys.stdout.write("\rBeginning download threads: {}     ".format(t.time() - originaltime))
    sys.stdout.flush()

    count=1
    for x in imageList:
        if not CLI:
            if PVVar.get() == 0 and SIVar.get() == 0:
                URL = x.file_url
            elif PVVar.get() == 1:
                URL = x.preview_url
            elif SIVar.get() == 1:
                URL = x.sample_url
            else:
                URL = x.file_url
            while (threadcounter >= threadlimit and threadlimit != 0):
                t.sleep(0.1) # Wait for new thread
            t1 = threading.Thread(target=download, args=(URL, x.md5, output, x, r34tag, creatorID, CLI, count))
            t1.start()
        else:
            URL = x.file_url
            while (threadcounter >= threadlimit and threadlimit != 0):
                t.sleep(0.1)  # Wait for new thread
            t1 = threading.Thread(target=downloadLITE, args=(URL, x.md5, output))
            t1.start()
        threadcounter += 1
        downloadCounter += 1
        count += 1

    sys.stdout.write("\rAll downloading threads running:  [{}]".format( " "*threadlimit))
    sys.stdout.flush()

    while (not threadcounter == 0):
        sys.stdout.write("\rAll downloading threads running: [{}>{}]".format( "="*((threadlimit-threadcounter)-1), " "*threadcounter))
        sys.stdout.flush()

    print("\nFinished downloading at: {}        ".format(t.time() - originaltime))
    print("\n")
    easygui.msgbox("{} has finished downloading".format(searchstr))



# End CLI Code

# Begin GUI Code

class R34Frame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        root = self.master
        self.pack(fill=BOTH, expand=1)

        global search2
        global output2
        global sample2
        global threadcount2
        global printButton
        global createID2
        global preview2
        global sample2

        global SSVar
        global SRVar
        global NCVar
        global PVVar
        global SIVar
        global OOVar

        SSVar = IntVar()  # Sort Score Variable
        SRVar = IntVar()  # Sort Resolution Variable
        NCVar = IntVar()  # No Characters Variable
        PVVar = IntVar()  # Preview Variable
        SIVar = IntVar()  # Sample Image Variable
        OOVar = IntVar()  # Original Order Variable

        search2Label = Label(self, text="Rule34 Search:")
        search2Label.place(x=0, y=40)
        search2 = Text(root, height=1, width=38)
        search2.place(x=0, y=60)

        exitButton = Button(self, text="Exit", command=self.clickExitButton)
        exitButton.place(x=0, y=0)

        printButton = Button(self, text="Download", command=self.getTextInput)
        printButton.place(x=50, y=0)

        output2Label = Label(self, text="Output directory: ")
        output2Label.place(x=0, y=80)
        output2 = Text(root, height=1, width=38)
        output2.place(x=0, y=100)
        output2.insert(1.0, os.getcwd() + "/out")

        threadcount2Label = Label(self, text="Thread Count: ")
        threadcount2Label.place(x=0, y=120)
        threadcount2 = Text(root, height=1, width=38)
        threadcount2.place(x=0, y=140)

        SortScore2 = Checkbutton(root, text='Sort By Score', variable=SSVar, onvalue=1, offvalue=0)
        SortScore2.place(x=0, y=165)

        SortSize2 = Checkbutton(root, text='Sort By Size', variable=SRVar, onvalue=1, offvalue=0)
        SortSize2.place(x=0, y=185)

        OCOnly2 = Checkbutton(root, text='Original Characters Only', variable=NCVar, onvalue=1, offvalue=0, command=self.warning)
        OCOnly2.place(x=0, y=205)

        createID2Label = Label(self, text="Creator ID (optionaL):")
        createID2Label.place(x=0, y=225)
        createID2 = Text(root, height=1, width=38)
        createID2.place(x=0, y=245)

        preview2 = Checkbutton(root, text='Use Preview images (tiny version)', variable=PVVar, onvalue=1, offvalue=0)
        preview2.place(x=0, y=270)

        sample2 = Checkbutton(root, text='Use Sample Images (smaller version, better for storage)', variable=SIVar, onvalue=1, offvalue=0)
        sample2.place(x=0, y=290)

        #original2 = Checkbutton(root, text='Sort by Original Order', variable=OOVar, onvalue=1, offvalue=0)
        #original2.place(x=0, y=310)

    def warning(self):
        easygui.msgbox("Warning, Enabling OC only is experimental and some outputs may be unexpected")

    def getTextInput(self):
        global search2
        global output2
        global threadcount2
        global printButton
        global createID2

        global SSVar
        global SRVar
        global NCVar
        global PVVar
        global SIVar
        global OOVar


        print(SSVar.get())
        print(SRVar.get())
        print(NCVar.get())
        print(PVVar.get())
        print(SIVar.get())

        search = search2.get(1.0, END + "-1c")
        outputdir = output2.get(1.0, END + "-1c")
        threadcount = threadcount2.get(1.0, END + "-1c")
        creatorID = createID2.get(1.0, END + "-1c")

        print(search)
        print(outputdir)
        try:
            threadcount = int(threadcount)
            if creatorID != '':
                creatorID = int(creatorID)
            else:
                creatorID = None
            print(threadcount)

            # For python  3.7< compatibility
            R34Thread = asyncio.new_event_loop()
            R34T1 = threading.Thread(target=R34Thread.run_until_complete, args=(main(search, outputdir,threadcount,creatorID, False),))
            R34T1.start()

        except Exception as e:
            print(e)
            open("traceback.txt", "w").write(str(e))
            easygui.msgbox("Error in input value, Make sure thread is an Integer or That Search is valid. View console or traceback.txt for full traceback")
            easygui.msgbox(e)

    def clickExitButton(self):
        exit()

