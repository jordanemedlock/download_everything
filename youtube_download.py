from pytube import YouTube
from pprint import pprint
import sys

def download_video(video_id='', folder='.', progress=None, finish=None):
    url = 'http://www.youtube.com/watch?v={}'.format(video_id)

    try:
        yt = YouTube(url)
    except Exception as e:
        print('Failed to get video with url', url)
        return

    yt.set_filename(yt.filename + ' ' + str(video_id))

    if len(yt.filter('mp4')) > 0:
        if len(yt.filter('mp4', '720p')) > 0:
            video = yt.get('mp4', '720p')
        else:
            video = yt.filter('mp4')[-1]
    else:
        print('No mp4 formatted videos')
        return

    try:
        video.download(folder, on_progress=progress, on_finish=finish)
    except Exception as e:
        print('Failed to download file with exception:', e)
        return

if __name__ == '__main__':
    if len(sys.argv) > 1:
        vid = sys.argv[1]
        download_video(video_id=vid, finish=lambda x: print('Finished downloading', x))
        print('Downloading video')
    else:
        print('Usage - python3 youtube_download.py VIDEO_ID')
        sys.exit(1)


