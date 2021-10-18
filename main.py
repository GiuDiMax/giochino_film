from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image
import vlc
from utils import *
import time

global scelte, b2_variabile, b11, title, year, number, root
scelte = []

def VideoClip():
    youtube_video(title, year)

def PauseVideo():
    global pause
    pause = False
    pause = pause_video(pause)

def StopVideo():
    stop_video()

def OnDoubleClick(event):
    global title, year, number
    item = tree.selection()[0]
    title = tree.item(item)['values'][0]
    year = tree.item(item)['values'][1]
    number = tree.item(item)['values'][2]
    for i in tree.get_children():
        tree.delete(i)
    info(number)

def Casuale():
    global title, year, number
    if pseudo_casual.get() == 1:
        reset()
        for i in tree.get_children():
            tree.delete(i)
        for j in range(10):
            title, year, number = casual()
            tree.insert("", tk.END, values=[title, year, number])
    else:
        title, year, number = casual()
        reset()
        if check_solution.get() == 1:
            info(number)

def frame_funzione():
    w = frame_window.winfo_width()
    check2 = False
    try:
        identity = tmdb.Movies(number)
        response = identity.images()
        check2 = True
    except:
        try:
            identity = tmdb.TV(number)
            response = identity.images()
            check2 = True
        except:
            check2 = False
    if check2 == True:
        frame = response['backdrops']
        if len(frame) == 0:
            pass
        else:
            for i in range(len(frame)+1):
                rand_num = randint(0, len(frame)-1)
                if frame[rand_num]['iso_639_1'] == None and rand_num not in scelte:
                    scelte.append(rand_num)
                    h = int(w/frame[rand_num]['aspect_ratio'])
                    frame = frame[rand_num]['file_path']
                    picurl = "https://image.tmdb.org/t/p/original" + frame
                    #global frame_window
                    #frame_window = tk.Toplevel(root)
                    #frame_window.geometry("1280x720")
                    image1 = Image.open(requests.get(picurl, stream=True).raw)
                    image1 = image1.resize((w, h), Image.ANTIALIAS)
                    test = ImageTk.PhotoImage(image1)
                    label1 = tk.Label(frame_window, image=test)
                    label1.image = test
                    label1.place(x=0, y=0)
                    b11 = tk.Button(frame_window, text="Altra", command=Prossima)
                    b11.place(x=15, y=15)
                    break

def FrameFilm():
    global scelte
    scelte = []
    frame_funzione()

def Prossima():
    frame_funzione()

def updatepic(picurl):
    image1 = Image.open(requests.get(picurl, stream=True).raw)
    image1 = image1.resize((300, 450), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(image1)
    label1 = tk.Label(image=test)
    label1.image = test
    label1.place(x=350, y=12)

def reset():
    updatepic("https://i.ibb.co/92WDdqn/random.jpg")
    infofilm.set("NUOVO FILM CASUALE CARICATO!")
    info2film.set("---")
    info3film.set("---")
    for i in tree.get_children():
        tree.delete(i)
    image1 = Image.open(requests.get("https://wallpaperaccess.com/full/752715.jpg", stream=True).raw)
    w = frame_window.winfo_width()
    h = frame_window.winfo_height()
    if w>1:
        image1 = image1.resize((w, h), Image.ANTIALIAS)
    else:
        image1 = image1.resize((1280, 720), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(image1)
    label1 = tk.Label(frame_window, image=test)
    label1.image = test
    label1.place(x=0, y=0)
    global scelte
    scelte = []
    try:
        b11.destroy()
    except:
        pass

def info(number):
    try:
        identity = tmdb.Movies(number)
        response = identity.info(language="it-IT")
        type = "movie"
    except:
        identity = tmdb.TV(number)
        response = identity.info(language="it-IT")
        type = "serie"
    url_pic = response['poster_path']

    if type == "movie":
        infofilm.set("TITOLO: " + response['title'])
        try:
            if str(response["original_title"]) != title:
                info2film.set("AKA: " + response["original_title"] + " - "+title)
            else:
                info2film.set("Titolo Originale: " + response["original_title"])
        except:
            info2film.set("Titolo Originale: " + title)
        try:
            info3film.set("RILASCIO: " + response["release_date"] + " (" + str(year) + ")")
        except:
            info3film.set("ANNO: " + str(year))
        response = identity.credits(language="it-IT")
        try:
            start = time.time()
            while True:
                updatepic("https://www.themoviedb.org/t/p/w500"+url_pic)
                if start > 0.5:
                    break
        except:
            pass
    elif type == "serie":
        infofilm.set("TITOLO: " + response['name'])
        try:
            if str(response["original_name"]) != title:
                info2film.set("AKA: " + response["original_name"] + " - "+title)
            else:
                info2film.set("Titolo Originale: " + response["original_name"])
        except:
            info2film.set("Titolo Originale: " + title)
        try:
            info3film.set("RILASCIO: " + response["first_air_date"] + " (" + str(year) + ")")
        except:
            info3film.set("RILASCIO: " + str(year))
        response = identity.credits(language="it-IT")
        try:
            start = time.time()
            while True:
                updatepic("https://www.themoviedb.org/t/p/w500"+url_pic)
                if start > 0.5:
                    break
        except:
            pass

    job_ok = ['Director of Photography', 'Director', 'Screenplay', 'Editor',
              'Writer', 'Original Music Composer', 'Producer']
    lista_crew = response['crew']
    lista_crew_print = "CREW: "
    for people in lista_crew:
        #print(people)
        if people['job'] in job_ok:
            try:
                tree.insert("", tk.END, values=[people['name'], people['job']])
            except:
                pass

    lista_cast = response['cast']
    lista_cast_print = "CAST: "
    if len(lista_cast) >= 10:
        lista_cast = lista_cast[:10]
    for people in lista_cast:
        try:
            tree.insert("", tk.END, values=[people['name'], "Act [" + people['character'] + "]"])
        except:
            pass

def Soluzione():
    info(number)

def AudioClip():
    identity = tmdb.Movies(number)
    response = identity.info(language="it-IT")
    title = response['title']
    youtube_audio(title, year)

root = tk.Tk(className='QUIZ FILM')
root.geometry("670x480")

global frame_window
frame_window = tk.Toplevel(root)
frame_window.geometry("1280x720")

check_solution = tk.IntVar()
chk = tk.Checkbutton(root, text='Sol. sempre visibile', variable=check_solution)
chk.place(x=15, y=45)
pseudo_casual = tk.IntVar()
psdcsl = tk.Checkbutton(root, text='Pseudocasuale', variable=pseudo_casual)
pseudo_casual.set(1)
psdcsl.place(x=200, y=45)
b1 = tk.Button(root, text="Film Casuale", command=Casuale)
b1.place(x=15, y=15)
b2_variabile = tk.Button(root, text="Soluzione", command=Soluzione)
b2_variabile.place(x=205, y=15)
b3 = tk.Button(root, text="Frame del Film", command=FrameFilm)
b3.place(x=105, y=15)
b1 = tk.Button(root, text="Video Clip", command=VideoClip)
b1.place(x=15, y=75)
b2 = tk.Button(root, text="Pausa/Riprendi", command=PauseVideo)
b2.place(x=95, y=75)
b3 = tk.Button(root, text="Stop", command=StopVideo)
b3.place(x=205, y=75)
b1 = tk.Button(root, text="Clip Audio", command=AudioClip)
b1.place(x=15, y=115)
b2 = tk.Button(root, text="Pausa/Riprendi", command=PauseVideo)
b2.place(x=95, y=115)
b3 = tk.Button(root, text="Stop", command=StopVideo)
b3.place(x=205, y=115)
infofilm = tk.StringVar()
labelfilm = tk.Label(root, textvariable=infofilm, anchor='c')
labelfilm.place(x=15, y=165)
info2film = tk.StringVar()
label2film = tk.Label(root, textvariable=info2film, anchor='c')
label2film.place(x=15, y=185)
info3film = tk.StringVar()
label3film = tk.Label(root, textvariable=info3film, anchor='c')
label3film.place(x=15, y=205)

tree = ttk.Treeview(root, column=("c1", "c2"), show='headings')
tree.column("#1", anchor=tk.CENTER, width=150)
tree.heading("#1", text="Nome")
tree.column("#2", anchor=tk.CENTER, width=150)
tree.heading("#2", text="Ruolo")
tree.place(x=15, y=235)
tree.bind("<Double-1>", OnDoubleClick)

Casuale()
reset()
root.mainloop()


