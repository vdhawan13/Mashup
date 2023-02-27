from pytube import YouTube
from pydub import AudioSegment
import urllib.request
import re
import os
import sys

def mp4_to_mp3(x,n):
    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(x))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    for i in range(n):
        yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[i]) 
        print("Songs downloading "+str(i+1)+" .......")
        mp4files = yt.streams.filter(only_audio=True).first().download(filename='song-'+str(i)+'.mp3')

    print("Songs downloaded")
    print("Creating mashup.....")

def merge_music(n,y):
    if os.path.isfile("song-0.mp3"):
        try:
            audio_1 = AudioSegment.from_file("song-0.mp3")[0:y*1000]
        except:
            audio_1 = AudioSegment.from_file("song-0.mp3",format="mp4")[0:y*1000]
    for i in range(1,n):
        aud_file = str(os.getcwd()) + "/song-"+str(i)+".mp3"
        try:
            f = AudioSegment.from_file(aud_file)
            audio_1 = audio_1.append(f[0:y*1000],crossfade=1000)
        except:
            f = AudioSegment.from_file(aud_file,format="mp4")
            audio_1 = audio_1.append(f[0:y*1000],crossfade=1000)
        
    return audio_1

def main():
    if len(sys.argv) == 5:
        x = sys.argv[1]
        x = x.replace(' ','') + "songs"
        try:
            n = int(sys.argv[2])
            y = int(sys.argv[3])
        except:
            sys.exit("Entered Parameters are Wrong")
        output_name = sys.argv[4]
    else:
        sys.exit('Please Provide 4 Parameters')

    mp4_to_mp3(x,n)
    audio_1 = merge_music(n,y)

    audio_1.export(output_name, format="mp3")
    print("Mashup created successfully")

if __name__ == '_main_':
    main()