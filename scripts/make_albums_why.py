#!/usr/bin/env python3
"""
合成「為什麼……？」因果認知問答專輯合輯音檔：
1. 5 大分類獨立合輯音檔（output/categories_why/）
2. 100 題完整連續播放大合輯（output/why_100_compilation.mp3）
依據教學規格：每題題目與答案間停頓 5 秒（已包含在單曲中），每題之間間隔 2 秒。
"""

import json
import os
import subprocess

DATA_FILE = "data/questions_why.json"
SINGLES_DIR = "output/singles_why"
CATEGORIES_DIR = "output/categories_why"
FULL_COMPILATION = "output/why_100_compilation.mp3"
PAUSE_BETWEEN_QUESTIONS = 2.0

os.makedirs(CATEGORIES_DIR, exist_ok=True)
os.makedirs("output/tmp", exist_ok=True)

def get_single_file(qid, clean_q):
    filename = f"第{qid:03d}題_{clean_q}.mp3"
    filepath = os.path.join(SINGLES_DIR, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing file: {filepath}")
    return filepath

def concat_files_with_silence(file_list, output_path, title, album_title):
    print(f"正在製作合輯: {title} ({len(file_list)} 題)...")
    
    silence_file = "output/tmp/silence_2s.mp3"
    cmd_silence = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-t", str(PAUSE_BETWEEN_QUESTIONS),
        "-i", "anullsrc=r=24000:cl=mono",
        "-c:a", "libmp3lame", "-b:a", "128k",
        silence_file
    ]
    subprocess.run(cmd_silence, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    concat_list_file = f"output/tmp/concat_{os.path.basename(output_path)}.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for idx, single_path in enumerate(file_list):
            f.write(f"file '{os.path.abspath(single_path)}'\n")
            if idx < len(file_list) - 1:
                f.write(f"file '{os.path.abspath(silence_file)}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list_file,
        "-metadata", f"title={title}",
        "-metadata", "artist=特教生活問答",
        "-metadata", f"album={album_title}",
        "-c", "copy",
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(concat_list_file): os.remove(concat_list_file)
    print(f"  -> 完成: {output_path}")

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)

    categories = {}
    all_files = []

    for item in questions:
        qid = item["id"]
        cat = item["category"]
        clean_q = item["question"].replace("？", "").replace("?", "").replace("/", "_").strip()
        filepath = get_single_file(qid, clean_q)
        
        all_files.append(filepath)
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(filepath)

    # 1. 製作 5 大分類合輯
    cat_names_map = {
        "第一類：身體需求與日常生活": "01_第一類_身體需求與日常生活(1-20題)",
        "第二類：天氣、穿著與環境": "02_第二類_天氣穿著與環境(21-40題)",
        "第三類：學校與外出安全": "03_第三類_學校與外出安全(41-60題)",
        "第四類：情緒與人際互動": "04_第四類_情緒與人際互動(61-80題)",
        "第五類：生活情境與因果推理": "05_第五類_生活情境與因果推理(81-100題)",
    }

    for cat_title, files in categories.items():
        prefix = cat_names_map.get(cat_title, cat_title)
        out_cat_file = os.path.join(CATEGORIES_DIR, f"{prefix}.mp3")
        concat_files_with_silence(files, out_cat_file, cat_title, "因果認知分類合輯")

    # 2. 製作 100 題完整連續大合輯
    concat_files_with_silence(all_files, FULL_COMPILATION, "100題為什麼因果認知完整大合輯", "100題因果認知問答")
    print("全部「為什麼」合輯製作完成！")

if __name__ == "__main__":
    main()
