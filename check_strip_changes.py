import cv2
import glob
import numpy as np

frames = sorted(glob.glob("D:/projects/monly/video_frames/*.jpg"))

# Let's crop the calendar strip region (around y=60 to y=170) in all frames where Calendar tab is active
# and check if the strip ever scrolled horizontally!
prev_strip = None
for fpath in frames:
    sec = float(fpath.split("_sec_")[1].replace(".jpg", ""))
    img = cv2.imread(fpath)
    # Status bar + top calendar week strip is approximately in top 15%
    h, w, _ = img.shape
    strip = img[int(h*0.06):int(h*0.17), :]
    
    if prev_strip is not None:
        diff = np.mean(cv2.absdiff(strip, prev_strip))
        if diff > 5:
            print(f"Sec {sec:5.1f} | Top strip changed (diff={diff:.1f})")
    prev_strip = strip
