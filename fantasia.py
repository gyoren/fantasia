import random
import os
import sys
import pygame
import pytimedinput
import tinytag

def clear(): # little clear function from SO that i snagged and compressed down to 2 lines
    _ = os.system('cls') if os.name == 'nt' else os.system('clear')

pygame.mixer.init()
clear()
# i recommend 1/5 for streaming and 1/10 ~ 1/20 for studying
volume = 1/int(input("Please type volume: 1/"))

# creating the song list (pygame only supports .ogg files as compressed audio)
# another piece of code from SO, spook found it (thx a lot)
if getattr(sys, 'frozen', False):
    musicPath = os.path.dirname(sys.executable) + "/audio/"
else:
    musicPath = os.path.dirname(os.path.realpath(__file__)) + "/audio/"

allOGG = []

for root, directories, filenames in os.walk(musicPath):
    for filename in filenames:
        allOGG.append(os.path.join(root,filename))

clear()

def main(): # this is the other code below but without the temp blacklist for obvious reasons
    global randomfile
    randomfile = random.choice(allOGG)
    # getting the duration with tinytag (divmod is for "minutes:seconds")
    durationraw = tinytag.TinyTag.get(randomfile).duration
    duration = divmod(round(durationraw), 60)
    # loading in the song and playing it
    pygame.mixer.music.load(randomfile)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()
    # using pytimedinput to let the user skip songs with the enter key
    # idk how to format the text in a different way without using regex (not learning how it works)
    # also, 4: is "/000" and :4 is ".ogg" so you can only see the name of the song
    songLocationSplit = randomfile.replace("\\", "/").split("/")
    pytimedinput.timedInput(songLocationSplit[-1][4:-4]
    .replace("`", "'").replace("_", "!").replace(",,,", "...")
    .replace("^e", "é").replace("-", "?").replace("^s", "/")
    .replace("^c", ":").replace(";", "-").replace("^q", '"')
    + f', length: {duration[0]}:{duration[1]:02}\nTrack from {songLocationSplit[-2]}',
    durationraw, True, 1)
    # clearing screen after song is skipped or ends
    clear()
    pygame.mixer.music.stop()

main()

tempblacklist = []
tempblacklist.append(randomfile)

while True: # see main() for comments
    randomfile = random.choice(allOGG)
    while randomfile in tempblacklist[-10:]:
        randomfile = random.choice(allOGG)
    durationraw = tinytag.TinyTag.get(randomfile).duration
    duration = divmod(round(durationraw), 60)
    pygame.mixer.music.load(randomfile)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()
    songLocationSplit = randomfile.replace("\\", "/").split("/")
    pytimedinput.timedInput(songLocationSplit[-1][4:-4]
    .replace("`", "'").replace("_", "!").replace(",,,", "...")
    .replace("^e", "é").replace("-", "?").replace("^s", "/")
    .replace("^c", ":").replace(";", "-").replace("^q", '"')
    + f', length: {duration[0]}:{duration[1]:02}\nTrack from {songLocationSplit[-2]}',
    durationraw, True, 1)
    clear()
    pygame.mixer.music.stop()
    tempblacklist.append(randomfile)
