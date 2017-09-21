from pytube import YouTube
from pprint import pprint
import sys


if len(sys.argv) > 2:
    vid = sys.argv[1]
    output_folder = sys.argv[2]
    download(vid, output_folder)
else:
    print('Usage - python3 download_youtube.py VIDEO_ID OUTPUT_FOLDER')
    sys.exit(1)

def empty(*args, **kwargs):
    pass

def download(video_id, output_folder, progress=empty, finished=empty):
    try:
        yt = YouTube("http://www.youtube.com/watch?v={}".format(vid))
    except e:
        print('Failed to get video with id', vid)
        sys.exit(1)


    yt.set_filename(yt.filename + '_' + vid)

    if len(yt.filter('mp4')) > 0:
        if len(yt.filter('mp4', '720p')) > 0:
            video = yt.get('mp4', '720p')
        else:
            video = yt.filter('mp4')[-1]
    else:
        print('No mp4 formatted videos')
        sys.exit(1)

    video.download('.', on_progress=progress, on_finish=finished)
