from random import randint
import tmdbsimple as tmdb
tmdb.API_KEY = 'YOUR API'
import requests
import pandas as pd
import vlc
import pafy
from pytube import YouTube
import os

def casual():
    tmdb.REQUESTS_SESSION = requests.Session()
    db = pd.read_csv('output.csv')
    movie_n = randint(0, len(db)-1)
    title_lbd = db.iloc[movie_n]['Title']
    year_lbd = int(db.iloc[movie_n]['Year'])
    number = int(db.iloc[movie_n]['tmdb'])
    return title_lbd, year_lbd, number

def youtube_video(title, year):
    try:
        stop_video()
    except:
        pass
    from youtubesearchpython import VideosSearch
    global player, titolo_video
    videosSearch = VideosSearch(title + " " + str(year) + " Clip", limit=10)
    url = videosSearch.result()
    for urlx in url['result']:
        if "trailer" not in urlx['title'] and "clip" or "scene" or "scena" in urlx['title']:
            url = urlx['link']
            break
    yt = YouTube(url)
    try:
        yt.streams.filter(progressive=True, file_extension='mp4', resolution="480p").order_by('resolution').desc().first().download()
    except:
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
    '''
    bad_char = ["|","?","!","~","\\","/"]
    for char in bad_char:
        titolo_video = titolo_video.replace(char, "")
    os.rename(titolo_video, "file.mp4")
    '''
    import glob
    targetPattern = r"*.mp4"
    titolo_video = glob.glob(targetPattern)[0]
    os.rename(titolo_video, "file.mp4")
    #video = pafy.new(titolo2)
    #best = video.getbest()
    #playurl = best.url
    ins = vlc.Instance()
    player = ins.media_player_new()
    #code = urllib.request.urlopen(url).getcode()
    Media = ins.media_new("file.mp4")
    Media.get_mrl()
    player.set_media(Media)
    player.play()

    '''
    good_states = ["State.Playing", "State.NothingSpecial", "State.Opening"]
    while str(player.get_state()) in good_states:
        pass
    player.stop()
    '''

def youtube_audio(title, year):
    try:
        stop_video()
    except:
        pass
    from youtubesearchpython import VideosSearch
    global player
    videosSearch = VideosSearch(title + " " + str(year) + " Clip ITA", limit=10)
    url = videosSearch.result()
    for urlx in url['result']:
        if "trailer" not in urlx['title'] and "clip" or "scene" or "scena" in urlx['title']:
            url = urlx['link']
            try:
                video = pafy.new(url)
                break
            except:
                pass
    best = video.getbestaudio()
    playurl = best.url
    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    player.play()

def pause_video(pause):
    if pause:
        player.play()
        return False
    else:
        player.pause()
        return True

def stop_video():
    player.stop()
    try:
        os.remove("file.mp4")
    except:
        pass
