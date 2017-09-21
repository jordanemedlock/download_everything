
from temboo.Library.YouTube.Search import ListSearchResults
from temboo.Library.YouTube.Playlists import ListPlaylistsByChannel
from temboo.Library.YouTube.PlaylistItems import ListItemsByPlaylist
from temboo.core.session import TembooSession
import json
import sys

session = TembooSession("jordanemedlock", "BlackPin", "yQbxb5hKgUehRlnfuqVJD7KF0v8BDQeX")

def find_channel_id(channel_name):
    choreo = ListSearchResults(session)
    
    inputs = choreo.new_input_set()

    inputs.set_Query(channel_name)

    results = choreo.execute_with_results(inputs)

    response = results.get_Response()

    obj = json.loads(response)

    items = obj['items']

    for item in items:
        if item['id']['kind'] == 'youtube#channel':
            return item['id']['channelId']


def find_videos_from_channel_id(channel_id, page_token=None):
    def inner(page_token):
        choreo = ListSearchResults(session)
        inputs = choreo.new_input_set()
        inputs.set_ChannelID(channel_id)
        if page_token is not None:
            inputs.set_PageToken(page_token)
        results = choreo.execute_with_results(inputs)
        response = results.get_Response()
        return json.loads(response)

    while True:
        obj = inner(page_token)
        items = obj['items']

        it = (
            { 'title': item['snippet']['title'], 'id': item['id']['videoId'] } 
            for item in items 
            if item['id']['kind'] == 'youtube#video'
        )

        page_token = obj['nextPageToken'] if 'nextPageToken' in obj else None
        
        for item in it:
            yield item

        if page_token is None:
            break


def find_playlists_for_channel_id(channel_id, page_token=None):
    def inner(page_token):
        choreo = ListPlaylistsByChannel(session)
        inputs = choreo.new_input_set()
        inputs.set_credential('YouTubeListPlaylists')
        inputs.set_ChannelID(channel_id)
        if page_token is not None:
            inputs.set_PageToken(page_token)
        results = choreo.execute_with_results(inputs)
        response = results.get_Response()
        return json.loads(response)
    
    while True:
        obj = inner(page_token)
        items = obj['items']

        it = (
            { 'title': item['snippet']['title'], 'id': item['id'] } 
            for item in items 
        )

        page_token = obj['nextPageToken'] if 'nextPageToken' in obj else None
        
        for item in it:
            yield item

        if page_token is None:
            break


def find_videos_from_playlist(playlist, page_token=None):
    def inner(page_token):
        choreo = ListItemsByPlaylist(session)
        inputs = choreo.new_input_set()
        inputs.set_credential('YouTubeListPlaylists')
        inputs.set_PlaylistID(playlist)
        if page_token is not None:
            inputs.set_PageToken(page_token)
        results = choreo.execute_with_results(inputs)
        response = results.get_Response()
        return json.loads(response)
    
    while True:
        obj = inner(page_token)
        items = obj['items']

        it = (
            { 'title': item['snippet']['title'], 'id': item['snippet']['resourceId']['videoId'] } 
            for item in items 
        )

        page_token = obj['nextPageToken'] if 'nextPageToken' in obj else None
        
        for item in it:
            yield item

        if page_token is None:
            break


def find_videos(channel_name=None, channel_id=None, playlist_id=None):
    if channel_name is not None:
        return find_videos(channel_id=find_channel_id(channel_name))
    if channel_id is not None:
        return find_videos_from_channel_id(channel_id)
    if playlist_id is not None:
        return find_videos_from_playlist(playlist_id)
    print('No argument set')
    

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('No channel name provided')
        sys.exit(1)
    iterator = find_videos(channel_name=sys.argv[1])
    for vid in iterator:
        print('{}\t{}'.format(vid['title'], vid['id']))
