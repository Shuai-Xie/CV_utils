"""
https://www.learnopencv.com/selective-search-for-object-detection-cpp-python/
- f|q: f=fast, q=quality
- l|m: less box, more box
结果可看 产生的 box 效果一般
"""
import cv2

im = cv2.imread('imgs/breakfast.jpg')

# resize image
newHeight = 400
newWidth = int(im.shape[1] * newHeight / im.shape[0])
im = cv2.resize(im, (newWidth, newHeight))

# create Selective Search Segmentation Object using default parameters
ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()

# set input image on which we will run segmentation
ss.setBaseImage(im)

method = 'f'  # f=fast, q=quality

if method == 'f':  # fast but low recall
    ss.switchToSelectiveSearchFast()
elif method == 'q':  # high recall but slow
    ss.switchToSelectiveSearchQuality()
else:
    exit(1)

# run selective search segmentation on input image
rects = ss.process()  # f:453, q:1354
print('Total Number of Region Proposals: {}'.format(len(rects)))

# number of region proposals to show
numShowRects = 100
# increment to increase/decrease total number of reason proposals to be shown
increment = 50

while True:
    # create a copy of original image
    imOut = im.copy()

    # itereate over all the region proposals
    for i, rect in enumerate(rects):
        # draw rectangle for region proposal till numShowRects
        if i < numShowRects:
            x, y, w, h = rect  # 这种格式
            cv2.rectangle(imOut, (x, y), (x + w, y + h), (0, 0, 255), 1, cv2.LINE_AA)
        else:
            break

    # show output
    cv2.imshow("Output", imOut)

    # record key press
    k = cv2.waitKey(0) & 0xFF

    # more
    if k == ord('m'):
        numShowRects += increment  # increase total number of rectangles to show by increment
    # less
    elif k == ord('l') and numShowRects > increment:
        numShowRects -= increment  # decrease total number of rectangles to show by increment
    # quit
    elif k == ord('q'):
        break

cv2.destroyAllWindows()
