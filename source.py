import Tkinter as tk
import ttk
import threading
import pickle
import os
from collections import OrderedDict as od
import webbrowser
import execjs
import PyV8
import cfscrape
from bs4 import BeautifulSoup as bs
import datetime
import time
import requests
from requests.adapters import HTTPAdapter
import execjs

class Anime:
    def __init__(self, name, home):
        self.name = name
        self.epdict = {}
        self.home = home
        self.current = 0
def writedict(adict):
    listfile = open(r'animelist.txt', 'wb')
    pickle.dump(adict, listfile)
    listfile.close()
    
root = tk.Tk()
root.geometry("419x220")
root.title("InstaKiss!")
root.wm_iconbitmap('lips.ico')
root.resizable(height = False, width = False)

note = ttk.Notebook(root)
homeframe = tk.Frame(note, padx = 2,bg = 'white')
animeframe = tk.Frame(note, bg = 'white', padx = 11)
mangaframe = tk.Frame(note, bg = 'white', padx = 11)
addframe = tk.Frame(note, padx = 2,bg = 'white')
delframe = tk.Frame(note, padx = 2,bg = 'white')
note.add(homeframe, text = "Home")
note.add(animeframe, text = "  My Shows  ")
note.add(addframe, text = "Add Show")
note.add(delframe, text = "Drop Show")
note.place(x = 0, y = 0)

photo = tk.PhotoImage(file = "Homescreen2.gif")
homelabel = tk.Label(homeframe, image = photo, bg = 'white')
homelabel.grid(padx = (82,0), pady = 5)

leftframe = tk.Frame(animeframe, bg = 'white')
rightframe = tk.Frame(animeframe, bg = 'white')
leftframe.grid(row = 0, column = 0)
rightframe.grid(row = 0, column = 1)
animelist = tk.Listbox(leftframe, width = 40, selectmode = tk.SINGLE, height = 9)
episodecombo = ttk.Combobox(rightframe, height = 9)
watchbutton = tk.Button(rightframe, text = 'Watch selected episode', bg = 'CadetBlue2')
setepbutton = tk.Button(rightframe, text = 'Set as previous episode ', bg = 'CadetBlue3')
contbutton = tk.Button(leftframe, text = 'Continue show', bg = 'CadetBlue1')
backupbutton = tk.Button(rightframe, text = 'Back up List', bg = 'white')
animelist.grid(row = 0, column = 0, padx = (0,10), pady = (10,5))
animelist.configure(exportselection=False)
episodelabel = tk.Label(rightframe, text = "Episode", padx = 1, bg = 'white')
episodelabel.grid(row = 1, sticky = "N", pady = (4, 0))
episodecombo.grid(row = 2, sticky = "N", pady = (0, 0))
watchbutton.grid(row = 3, pady = (10,0))
setepbutton.grid(row = 4, pady = (10, 33))
backupbutton.grid(row = 5, pady = (10, 3) )
contbutton.grid(row = 1, pady = (2, 7), padx = (0, 17))

namelabel = tk.Label(addframe, text = "Name", bg = "white")
nameentry = tk.Entry(addframe, bg = 'white', width = 50)
urllabel = tk.Label(addframe, text = "Link to Episode List from a Kiss Site", bg = 'white')
urlentry = tk.Entry(addframe, bg = 'white', width = 50)
instancelabel = tk.Label(addframe, text = "Ex.: http://kissanime.com/Anime/Sailor-Moon", bg = 'white', font = ("TkDefaultFont", 8,"italic"))
addbutton = tk.Button(addframe, text = 'Add show!', bg = "DarkOliveGreen1")
namelabel.grid(row = 0, padx = (55,0), pady = (7, 0))
nameentry.grid(row = 1, pady = (0, 7), padx = (55,0))
instancelabel.grid(row = 4, pady = (0, 5), padx = (55,0))
urllabel.grid(row = 2, pady = (0, 2), padx = (57,0))
urlentry.grid(row = 3, padx = (55,0), pady = (0, 1))

addbutton.grid(row = 5, pady = (10, 0), padx = (57,0))

namelabel2 = tk.Label(delframe, text = "Name", bg = "white")
nameentry2 = tk.Entry(delframe, bg = 'white', width = 50)
namelabel2.grid(row = 0, padx = (55,95), pady = (27, 0))
nameentry2.grid(row = 1, pady = (5, 7), padx = (54,85))
delbutton = tk.Button(delframe, text = " Remove show", bg = 'coral')
delbutton.grid(row = 4, pady = (10, 0), padx = (2, 40))
resetbutton = tk.Button(delframe, text = " Reset to Default Shows", bg = 'tomato')
resetbutton.grid(row = 5, pady = (10, 0), padx = (0,40))




#------------------------------Anime--------------------------------------------
defaultlist = [("Tom and Jerry", "http://kisscartoon.me/Cartoon/Tom-and-Jerry-Classic-Collection"),
("Sailor Moon", "http://kissanime.com/Anime/Sailor-Moon"),
("Amachan", "http://kissasian.com/Drama/Amachan")
]

defaultmanga = [()]

namedict = {}

def updatelist():
    unpicklefile = open(r'animelist.txt', 'rb')
    global allanime
    allanime = pickle.load(unpicklefile)
    unpicklefile.close()
    for name in sorted(allanime):
        animelist.insert(tk.END, name)
updatelist()
#----------------------Anime Selection GUI Programming--------------------------
urlbits = [None, None]

def graburl():
    try:
        webbrowser.open_new_tab(urlbits[1])
    except TypeError:
        pass

def getanime(event):
    urlbits[0] = allanime[animelist.get(animelist.curselection())] #anime
    episodecombo['values'] = urlbits[0].epdict.keys()
    episodecombo.update()
def getepisode(event):
    urlbits[1] = urlbits[0].epdict[episodecombo.get()] #episode

def setlast():
    allanime[animelist.get(animelist.curselection())].current = episodecombo.current()
    writedict(allanime)


def continueanime():
    urlbits[1] = urlbits[0].epdict.items()[urlbits[0].current +1][1]
    allanime[animelist.get(animelist.curselection())].current += 1
    writedict(allanime)
    scraper = cfscrape.create_scraper()
    content =  scraper.get(urlbits[0].home).content
    soup = bs(content)
    for link in soup.find_all('a'):
        try:
            if urlbits[1] in  link['href']:
                url = urlbits[0].home[0:21] + link['href']
                webbrowser.open_new_tab(url)
        except TypeError:
            pass




animelist.bind('<<ListboxSelect>>', getanime)
episodecombo.bind('<<ComboboxSelected>>', getepisode)
watchbutton.configure(command = graburl)
setepbutton.configure(command = setlast)
contbutton.configure(command = continueanime)

#----------------------------Add Anime to Program-------------------------------
def create_epdict(ep_dict, url):
    scraper = cfscrape.create_scraper()
    content =  scraper.get(url).content
    soup = bs(content)
    epdict = {}
    eplist = []
    titlelist = []
    if "Drama" in url:
        for link in soup.find_all('a'):
                if 'href' in str(link):
                    try:
                        if "Episode-" in link['href']:
                            possible = link['href'].split("Episode-")[1]
                            possible = "/Episode-" + possible
                            fullurl = url + possible
                            fulltitle = link['title'].split("Episode ")[1][:9]
                            integers = [str(i) for i in range(0,10)]
                            if possible:
                                episode = possible[:7]
                            if fulltitle[0] in integers and fulltitle[1] in integers and fulltitle[2] in integers:
                                title = fulltitle[:3]
                            elif fulltitle[0] in integers and fulltitle[1] in integers:
                                title = fulltitle[:2]
                            else:
                                title = fulltitle[0]
                            eplist.append(fullurl.encode('ascii'))
                            titlelist.append(title.encode('ascii'))

                    except TypeError:
                        pass
        epdict = od((zip(titlelist[::-1][0:], eplist[::-1][0:])))
        return epdict
    else:
        for link in soup.find_all('a'):
                try:
                    if "Episode-" in link['href']:
                        possible = link['href'].split("Episode-")[1]
                        possible = "/Episode-" + possible
                        fullurl = url + possible
                        fulltitle = link['title'].split("Episode ")[1][:9]
                        integers = [str(i) for i in range(0,10)]
                        if fulltitle[4] in integers and fulltitle[5] in integers and fulltitle[6] in integers:
                            title = fulltitle[:7]
                        elif fulltitle[3:6] == " - " and fulltitle[6::9] in integers and fulltitle[7::9] in integers and fulltitle[8::9] in integers:
                            title = fulltitle[:9]
                        elif 'v' in fulltitle[:4].lower():
                            title = fulltitle[0:5]
                        else:
                            title = fulltitle[:3]
                        eplist.append(fullurl.encode('ascii'))
                        titlelist.append(title.encode('ascii'))
                except TypeError:
                    pass
        epdict = od((zip(sorted(titlelist),sorted(eplist))))
        return epdict

def create_anime():
    epdict = {}
    url = urlentry.get()
    name = nameentry.get()
    anime = Anime(name, url)
    anime.epdict = create_epdict(epdict, url)
    allanime['%s' %name] = anime
    writedict(allanime)
    animelist.delete(0, tk.END)
    updatelist()

def create_manga():
    epdict = {}
    url = urlentry.get()
    name = nameentry.get()
    manga = Anime(name, url)
    manga.epdict = create_epdictm(epdict, url)
    allmanga['%s' %name] = manga
    writemdict(allmanga)
    mangalist.delete(0, tk.END)
    updatemlist()


def resetlist():
    allanimeo = {}
    for tup in defaultlist:
        epdict = {}
        url = tup[1]
        name = tup[0]
        anime = Anime(name, url)
        anime.epdict = create_epdict(epdict, url)
        allanimeo['%s' %name] = anime
        writedict(allanimeo)
        animelist.delete(0, tk.END)
        updatelist()

addbutton['command'] = create_anime
#--------------------------Remove Anime from Program----------------------------
def delanime():
    name = nameentry2.get()
    unpicklefile = open(r'animelist.txt', 'rb')
    anilist = pickle.load(unpicklefile)
    unpicklefile.close()
    unpicklefile = open(r'animelist.txt', 'wb')
    del anilist['%s' %name]
    writedict(anilist)
    unpicklefile.close()
    animelist.delete(0, tk.END)
    updatelist()



def resetdefault():
    def resetlist2():
        allanimeo = {}
        for tup in defaultlist:
            epdict = {}
            url = tup[1]
            name = tup[0]
            anime = Anime(name, url)
            anime.epdict = create_epdict(epdict, url)
            allanimeo['%s' %name] = anime
            writedict(allanimeo)
            animelist.delete(0, tk.END)
            updatelist()
        t.destroy()
    t = tk.Toplevel(bg = 'white')
    sure = tk.Label(t, text = "Are you sure?", bg = "white", height = 2, width = 20)
    y = tk.Button(t, text = "Yes, reset my show list.", command = resetlist2, bg = 'pink')
    n = tk.Button(t, text = "No, I want to keep my list.", command = t.destroy, bg = 'lightcyan')
    sure.grid(row = 0, padx = 5, pady = (5,0))
    y.grid(row = 1, pady = (5,0))
    n.grid(row = 2, pady = (5,5))

delbutton['command'] = delanime
resetbutton['command'] = resetdefault
#--------------------------------Back up List-----------------------------------
def backupbuttonfunc():
     bup = tk.Toplevel(bg = 'white')
     def backup():
        if not os.path.exists(r"BackupLists"):
            os.mkdir("BackupLists")
        if backentry.get() or backentry.get() != "" :
            name = r'BackupLists\\%s.txt' %str(backentry.get())
            backupfile = open(name, 'wb')
            pickle.dump(allanime, backupfile)
            backupfile.close()
            bup.destroy()
        else:
            name = r'BackupLists\\%s.txt' %(str(datetime.datetime.now().date()) + "-" + str(datetime.datetime.now().hour) + "-" + str(datetime.datetime.now().minute))
            backupfile = open(name, 'wb')
            pickle.dump(allanime, backupfile)
            backupfile.close()
            bup.destroy()
        popup = tk.Toplevel(bg = 'white')
        tk.Label(popup, text = "Backup successful!", bg = 'white', height = 3).pack()
     bupf = tk.Frame(bup, bg = 'white')
     bupf.pack()
     backlabel = tk.Label(bupf, text = "Name the backup file:", bg = 'white')
     backentry = tk.Entry(bupf, width = 30)
     create = tk.Button(bupf, command = backup, text = "Create", bg = 'khaki')
     cancel = tk.Button(bupf, command = bup.destroy, text = "Cancel", bg = 'white')
     backlabel.grid(row = 0, columnspan = 2, pady = (10,0))
     backentry.grid(row = 1, columnspan = 2, padx = 10, pady = (0,5))
     create.grid(row = 2, column = 0, padx = (20,0))
     cancel.grid(row = 2, column = 1, pady = (0,5), padx = (0,20))

backupbutton['command']= backupbuttonfunc
#---------------------------------Run-------------------------------------------
if __name__ == "__main__":
    root.mainloop()
