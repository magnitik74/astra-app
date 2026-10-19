import cv2
import os
import sys

video_path = r"C:\Users\Александр\Desktop\IMG_5940.MP4"
output_dir = r"D:\projects\monly\video_frames"

if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Error opening video {video_path}")
    sys.exit(1)

fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = total_frames / fps if fps > 0 else 0

print(f"Video opened: FPS={fps}, total_frames={total_frames}, duration={duration:.2f}s")

# We want key frames throughout the 85 seconds:
# E.g. every 2 seconds or at key interaction moments (e.g. 1 frame per second = ~85 frames)
# Let's extract 1 frame every 1.5 seconds or 0.8 seconds to capture all gestures, scrolling, modals, etc.
step_sec = 1.0 # 1 frame per second
step_frames = max(1, int(fps * step_sec))

saved_count = 0
frame_idx = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if frame_idx % step_frames == 0:
        sec = frame_idx / fps
        filename = f"frame_{saved_count:03d}_sec_{sec:05.1f}.jpg"
        filepath = os.path.join(output_dir, filename)
        # Resize to reasonable dimensions if needed, or keep original
        cv2.imwrite(filepath, frame)
        saved_count += 1
    
    frame_idx += 1

cap.release()
print(f"Extraction complete: saved {saved_count} frames to {output_dir}")
