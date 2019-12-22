from skimage.segmentation import slic, mark_boundaries
from skimage import io
import matplotlib.pyplot as plt
import numpy as np

img = io.imread('imgs/rgb.jpg')

segs = [5, 10]

# Segments image using k-means clustering in Color-(x,y,z) space
segments = slic(img, n_segments=segs[0], compactness=10)  # int64, ndarray
out = mark_boundaries(img, label_img=segments)
# label_img : (M, N) array of int
# Label array where regions are marked by different integer values.

plt.subplot(121)
plt.title("n_segments={}".format(segs[0]))
plt.imshow(out)

segments2 = slic(img, n_segments=segs[1], compactness=10)
out2 = mark_boundaries(img, segments2)
plt.subplot(122)
plt.title("n_segments={}".format(segs[1]))
plt.imshow(out2)

plt.show()
