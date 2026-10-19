import glob
import cv2
import numpy as np

frames = sorted(glob.glob("D:/projects/monly/video_frames/*.jpg"))

# Let's inspect each frame from frame 14 to 88:
# We can check the difference between consecutive frames to detect touches/scrolling/navigation!
diffs = []
for i in range(14, len(frames)):
    f1 = cv2.imread(frames[i-1])
    f2 = cv2.imread(frames[i])
    diff = np.mean(cv2.absdiff(f1, f2))
    diffs.append((frames[i], diff))

# Let's find significant change points
print("Key transition points (diff > 15):")
for fpath, d in diffs:
    sec = float(fpath.split("_sec_")[1].replace(".jpg", ""))
    if d > 12:
        print(f"Time {sec:5.1f}s | Frame {fpath} | Diff = {d:.2f}")
