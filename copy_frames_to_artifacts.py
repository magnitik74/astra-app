import shutil
import os

src_dir = r"D:\projects\monly\video_frames"
dst_dir = r"C:\Users\Александр\.gemini\antigravity\brain\8dc77ab2-b9dd-4a62-9311-ed7a2c195cb3"

frames_to_copy = [
    ("frame_015_sec_014.5.jpg", "moonly_video_01_main_feed_day18.jpg"),
    ("frame_017_sec_016.4.jpg", "moonly_video_02_card1_beauty_badge.jpg"),
    ("frame_020_sec_019.3.jpg", "moonly_video_03_horoscope_fullscreen.jpg"),
    ("frame_025_sec_024.1.jpg", "moonly_video_04_horoscope_spheres_paywall.jpg"),
    ("frame_030_sec_029.0.jpg", "moonly_video_05_lunar_day_nakshatras.jpg"),
    ("frame_040_sec_038.6.jpg", "moonly_video_06_tarot_practices_fan_deck.jpg"),
    ("frame_045_sec_043.4.jpg", "moonly_video_07_weekly_practices_plan.jpg"),
    ("frame_065_sec_062.7.jpg", "moonly_video_08_karma_practice_detail.jpg"),
    ("frame_070_sec_067.6.jpg", "moonly_video_09_sticky_header_and_transits.jpg"),
    ("frame_075_sec_072.4.jpg", "moonly_video_10_meditation_player_3d_clay.jpg"),
    ("frame_080_sec_077.2.jpg", "moonly_video_11_planetary_transits_arc.jpg")
]

for src_name, dst_name in frames_to_copy:
    src_path = os.path.join(src_dir, src_name)
    dst_path = os.path.join(dst_dir, dst_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"Copied {src_name} -> {dst_name}")

print("All key frames copied successfully!")
