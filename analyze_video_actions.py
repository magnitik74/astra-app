import glob
from PIL import Image
import numpy as np

# Let's inspect frames to see when calendar, tarot, player, etc. are shown
frames = sorted(glob.glob("D:/projects/monly/video_frames/*.jpg"))

# Let's crop header/body regions to see transitions:
# In each frame, let's extract:
# 1. Top region (status bar & header)
# 2. Middle region
# 3. Bottom tab bar
# And print description of actions

print(f"Analyzing {len(frames)} frames...")
