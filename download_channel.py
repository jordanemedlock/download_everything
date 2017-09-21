from get_videos import find_videos
from youtube_download import download_video
import os
import sys

def download_whole_channel(channel_name, folder='.', verbose=True):
    directory = os.path.join(folder, channel_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    for vid in find_videos(channel_name=channel_name):
        download_video(video_id=vid['id'], folder=directory, finish=print if verbose else None)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Missing channel name')
        sys.exit(1)
    download_whole_channel(sys.argv[1])

