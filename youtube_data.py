# youtube_data.py
import os
import pandas as pd
from googleapiclient.discovery import build

# API 키를 설정합니다.
API_KEY = 'AIzaSyDoYnBNce440YAZJilV8fYLXtDOQC70whI'  # 여기에 발급받은 API 키를 입력하세요.
CHANNEL_ID = 'UCkZLa5fKPC9v550eOcfRHcg'  # 여기에 분석하고자 하는 YouTube 채널 ID를 입력하세요.

# YouTube API 클라이언트를 초기화합니다.
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_details(video_id):
    """
    주어진 비디오 ID에 대한 상세 정보를 가져오는 함수입니다.
    """
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    response = request.execute()
    
    # 응답에서 필요한 정보를 추출합니다.
    video_details = {
        'title': response['items'][0]['snippet']['title'],
        'channel': response['items'][0]['snippet']['channelTitle'],
        'views': int(response['items'][0]['statistics'].get('viewCount', 0)),
        'likes': int(response['items'][0]['statistics'].get('likeCount', 0)),
        'comments': int(response['items'][0]['statistics'].get('commentCount', 0)),
        'category': response['items'][0]['snippet']['categoryId']
    }
    return video_details

def get_channel_videos(channel_id, max_results=50):
    """
    주어진 채널 ID에 속한 비디오 목록을 가져오는 함수입니다.
    """
    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        maxResults=max_results,
        order="date",
        type="video"
    )
    response = request.execute()
    
    # 검색 결과에서 비디오 ID를 추출합니다.
    video_ids = [item['id']['videoId'] for item in response['items']]
    return video_ids

def main():
    # 채널의 비디오 ID 목록을 가져옵니다.
    video_ids = get_channel_videos(CHANNEL_ID, max_results=10)

    # 각 비디오의 상세 정보를 가져와서 데이터프레임으로 만듭니다.
    video_details_list = []
    for video_id in video_ids:
        video_details = get_video_details(video_id)
        video_details_list.append(video_details)

    # 데이터프레임으로 변환합니다.
    df = pd.DataFrame(video_details_list)
    
    # CSV 파일로 저장합니다.
    df.to_csv('youtube_channel_videos.csv', index=False, encoding='utf-8-sig')
    print("데이터가 youtube_channel_videos.csv 파일로 저장되었습니다.")

if __name__ == "__main__":
    main()
