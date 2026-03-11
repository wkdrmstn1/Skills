import numpy as np
import matplotlib.pyplot as plt 

# 각도 생성
angles_deg = np.linspace(0, 360, 360)

# 라디안 변환 : 넘파이는 각도를 라디안으로 이해하고 있다!
angles_rad =  np.deg2rad(angles_deg)

# 가짜 라이다 센싱 거리 채우기 
distance = np.full(360, 1.5)

# 극좌표계 구하는 공식 
x = distance * np.cos(angles_rad)
y = distance * np.sin(angles_rad)

# 그래프로 시각화 
plt.figure(figsize=(6, 6))
plt.scatter(0, 0, color="blue", label="turtlebot3")
plt.scatter(x, y, color="red", label="LiDar Points")
plt.legend()
plt.show()