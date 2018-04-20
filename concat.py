import subprocess   
from tqdm import tqdm
from os import listdir
from os.path import isfile, join
import os.path
from moviepy.editor import *
import sys

mypath = './'
yes = {'yes','y', 'ye'}
no = {'no','n'}
yesToAll = {'', 'a'}
all = False

parentFolders = next(os.walk('.'))[1]

showreels = []
for folder in parentFolders:
    if folder.isdigit():
        for (dirpath, dirnames, filenames) in os.walk(mypath + folder):
                for filename in filenames:
                    if not filename.startswith('.') and filename.endswith('.mp4'):
                        showreels.append({ 
                            "path": folder + '/' + filename,
                            "name": filename,
                            "folder": folder + '/'
                        })
    
def write ():
    animationIn = VideoFileClip((mypath + 'animationen/' + item["folder"] + item["name"]))
    showreelIn = VideoFileClip( mypath + item["path"])
    out = concatenate_videoclips([animationIn, showreelIn], padding=-0.1)
    out.write_videofile(('/home/funiel/stuff/new/' + os.path.splitext(item["path"])[0] + '.mp4'), bitrate="5000k")  

for item in tqdm(showreels):
    outPath = '/home/funiel/stuff/new/' + os.path.splitext(item["path"])[0] + '.mp4'
    if not os.path.isfile(outPath):
        write()

    '''
    if os.path.isfile(outPath):
        if not all:
            
            choice = input("File already exists. Overwrite? \n").lower()
            if choice in yesToAll:
                all = True
                write()
            if choice in yes:
                write()
            if choice in no:
                all = False
            else:
                sys.stdout.write("Will skip this file")
        else:
            write()
    else:
        write()
    '''