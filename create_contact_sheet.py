import cv2
import os
import glob
from PIL import Image, ImageDraw, ImageFont

frames = sorted(glob.glob("D:/projects/monly/video_frames/*.jpg"))
print(f"Total frames: {len(frames)}")

# Let's select every 3rd frame or 30 key frames:
# We can make 3 contact sheets (10 images each) or 1 large grid
# e.g. 6 columns x 10 rows (60 images)
selected_frames = frames[::2] # ~45 frames

# Load images, resize to width 200, height proportional
thumb_w = 200
thumb_h = int(thumb_w * 16 / 9) # or match aspect ratio
first_img = Image.open(selected_frames[0])
aspect = first_img.height / first_img.width
thumb_h = int(thumb_w * aspect)

cols = 6
rows = (len(selected_frames) + cols - 1) // cols

grid_img = Image.new("RGB", (cols * thumb_w, rows * thumb_h), (20, 20, 25))
draw = ImageDraw.Draw(grid_img)

for idx, fpath in enumerate(selected_frames):
    r = idx // cols
    c = idx % cols
    img = Image.open(fpath).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    grid_img.paste(img, (c * thumb_w, r * thumb_h))
    
    # draw label
    basename = os.path.basename(fpath).replace(".jpg", "")
    draw.text((c * thumb_w + 5, r * thumb_h + 5), basename, fill=(255, 255, 0))

out_path = "D:/projects/monly/video_overview_grid.jpg"
grid_img.save(out_path, quality=85)
print(f"Overview grid saved to {out_path} ({grid_img.size})")
