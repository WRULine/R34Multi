from r34tags import *  # import classes

# Begin Variable Definition
global SSVar  # Sort Score
global SRVar  # Sort Size
global NCVar  # Original Characters only
global PVVar  # Preview images
global SIVar  # Smaller Images
global OOVar  # Original Order
# OOVar To Be Implemented
# OOVar and Original Order has been temporarily removed
global tagCache
tagCache = {}

if __name__ == '__main__':
    global search2
    if "-cli" in sys.argv:
        global threadcounter

        search = input("Enter your Rule34 Search: ")
        output = input("Output directory (realtive to launch location): ")

        threadcount = int(input("Max Thread Count (0 for no limit):"))
        if threadcount == 0:
            print(
                "WARNING! This may cause your computer to slow down or even crash when dealing with high loads!\nRe-enter your limit to verify you want no thread limit")
            threadcount = int(input("Max Thread Count (0 for no limit):"))
        asyncio.get_event_loop().run_until_complete(main(search, output, threadcount))
    elif "-cmdline" in sys.argv:
        # verify all argeuments exist
        search = sys.argv[sys.argv.index("-search") + 1]
        search = search.replace("+", " ")

        output = sys.argv[sys.argv.index("-output") + 1]

        threadlimit = int(sys.argv[sys.argv.index("-threads") + 1])

        print("Search: " + search)
        print("Output: " + output)
        print("Threads: " + str(threadlimit))
        asyncio.get_event_loop().run_until_complete(main(search, output, threadlimit))
    else:
        root = Tk()
        root.geometry("400x400")
        root.wm_title("Rule34 Downloader GUI")
        app = R34Frame(master=root)
        app.mainloop()
