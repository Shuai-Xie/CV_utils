import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('13038_3401_road.png', cv2.IMREAD_UNCHANGED)

alpha = img[:, :, -1]
print(np.unique(alpha))

alpha[alpha > 0] = 255

plt.imshow(alpha, cmap='gray')
plt.show()
