from googleapiclient.discovery import build
from collections import Counter
import pprint

# API 키 설정 - 실제 API 키로 교체하세요.
api_key = 'AIzaSyDoYnBNce440YAZJilV8fYLXtDOQC70whI'

# YouTube API 클라이언트 객체 생성
youtube = build('youtube', 'v3', developerKey=api_key)

# 분석할 유튜브 채널의 ID 설정 - 실제 채널 ID로 교체하세요.
channel_id = 'UCkZLa5fKPC9v550eOcfRHcg'  # 올바른 채널 ID로 교체

# 특정 채널의 동영상 목록 가져오기
request = youtube.search().list(
    part='snippet',  # 가져올 데이터의 부분 설정 (snippet 포함)
    channelId=channel_id,  # 채널 ID 설정
    maxResults=100  # 가져올 동영상 수를 지정 (여기서는 10개)
)
response = request.execute()  # API 요청 실행 및 응답 받기

# 응답 데이터 확인 (디버그 목적으로 추가)
pprint.pprint(response)

# 동영상 데이터 리스트 초기화
video_data = []

# 동영상 제목과 ID 출력 및 데이터 정리
for item in response['items']:
    # 'id' 키가 'videoId'를 포함하는지 확인 후 접근
    if 'videoId' in item['id']:
        video_info = {
            'title': item['snippet']['title'],  # 동영상 제목
            'videoId': item['id']['videoId'],  # 동영상 ID
            'description': item['snippet']['description'],  # 동영상 설명
            'publishedAt': item['snippet']['publishedAt']  # 동영상 게시 날짜
        }
        video_data.append(video_info)  # 동영상 정보를 리스트에 추가
        # 동영상 제목과 ID 출력
        print(f"Title: {item['snippet']['title']}, Video ID: {item['id']['videoId']}")
    else:
        # 동영상 ID가 없는 경우 출력
        print(f"Title: {item['snippet']['title']}, No Video ID found")

# 데이터 전처리 예제 (간단한 분석)
# 모든 동영상 제목을 단어별로 분리하여 빈도수 계산
all_words = ' '.join([video['title'] for video in video_data]).split()
common_words = Counter(all_words).most_common(10)
print("Most common words in video titles:")
print(common_words)