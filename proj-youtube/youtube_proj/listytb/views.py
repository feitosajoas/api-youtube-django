import requests

from isodate import parse_duration

from django.conf import settings
from django.shortcuts import render, redirect

def index(request):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    search_params = {
        'part' : 'snippet',
        'channelId' : 'UCsvA53cTCp3LO7n7BNGHBFg',
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'maxResults' : 6,
        'type' : 'video',
        'order' : 'date'
    }

    r = requests.get(search_url, params=search_params)

   

    results = r.json()['items']

    video_ids = []
    for result in results:
        video_ids.append(result['id']['videoId'])

    
    video_params = {
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'part' : 'snippet,contentDetails',
        'id' : ','.join(video_ids),
        'maxResults' : 6
    }

    r = requests.get(video_url, params=video_params)

    results = r.json()['items']

    videos = []
    for result in results:
        video_data = {
            'title' : result['snippet']['title'],
            'id' : result['id'],
            'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
            'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
            'thumbnail' : result['snippet']['thumbnails']['high']['url']
        }

        videos.append(video_data)

    
    context = {
        'videos' : videos
    }

    return render(request, 'index.html', context)
