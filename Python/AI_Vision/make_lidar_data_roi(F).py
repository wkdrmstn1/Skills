# 관심영역에 대해서만 시각화 

import numpy as np
import matplotlib.pyplot as plt 

# 각도 생성
angles_deg = np.linspace(0, 360, 360)

# 라디안 변환 : 넘파이는 각도를 라디안으로 이해하고 있다!
angles_rad =  np.deg2rad(angles_deg)

# 가짜 라이다 센싱 거리 채우기 
distance = np.full(360, 1.5)
distance[30:90] = 0.8

# roi 설정 : 기준은 거리와 각도
cond_dist = distance <= 3.5
cond_ang = (angles_deg >= 0) & (angles_deg <= 180)
cond_total = cond_dist & cond_ang

# 극좌표계 구하는 공식 
x = distance * np.cos(angles_rad)
y = distance * np.sin(angles_rad)

# 데이터 필터링 
filtered_x = x[cond_total]
filtered_y = y[cond_total]

# 그래프로 시각화 
plt.figure(figsize=(6, 6))
plt.scatter(0, 0, color="blue", label="turtlebot3")
plt.scatter(filtered_x, filtered_y, color="red", label="LiDar Points")
plt.legend()
plt.show()