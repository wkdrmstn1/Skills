import cv2

# 최초로 얻은 프레임을 백업
cap = cv2.VideoCapture(0)
ret, prev_frame = cap.read()

if not ret:
    print("웹캠에서 영상을 가져올 수 없습니다.")
    cap.release()
    exit()

# 첫 프레임을 그레이스케일로 변환
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 이번 프레임을 그레이스케일로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 두 프레임 간 차이 계산
    diff = cv2.absdiff(prev_gray, gray)

    # 차이를 보기 좋게 이진화(Threshold)
    _, diff_thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # 화면에 표시
    cv2.imshow("Current Frame", frame)
    cv2.imshow("Frame Difference", diff)
    cv2.imshow("Threshold Movement", diff_thresh)

    # 이번 프레임을 다음 반복문의 prev_frame으로 사용
    prev_gray = gray.copy()
    
    if cv2.waitKey(10) ==  ord('q'): # ESC 키
        break

cap.release()
cv2.destroyAllWindows()