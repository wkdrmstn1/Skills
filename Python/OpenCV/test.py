import requests

# 1. Flask 서버 주소
url = "http://192.168.0.5:5000/api/logs"

# 2. 테스트할 이미지 파일 (실제 존재하는 이미지 파일명으로 변경)
file_path = "g.jpg" 

try:
    with open(file_path, 'rb') as f:
        # 3. 로봇이 보내는 것과 동일한 형식 구성
        files = {'image': f}
        data = {
            'situation': '테스트 상황 감지',
            'position': '테스트 구역'
        }
        
        # 4. 서버로 전송
        response = requests.post(url, files=files, data=data)
        
    print(f"상태 코드: {response.status_code}")
    print(f"응답 내용: {response.json()}")

except FileNotFoundError:
    print("에러: 폴더에 test.jpg 파일이 없습니다. 아무 사진이나 이름을 바꿔서 넣어주세요.")
except Exception as e:
    print(f"에러 발생: {e}")