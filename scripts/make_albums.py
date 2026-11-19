#!/usr/bin/env python3
"""
合成專輯合輯音檔：
1. 6 大分類獨立合輯音檔（output/categories/）
2. 100 題完整連續播放大合輯（output/full_100_compilation.mp3）
依據姊姊規格：每題題目與答案間停頓 3 秒（已包含在單曲中），每題之間間隔 3 秒。
"""

import json
import os
import subprocess

DATA_FILE = "data/questions.json"
SINGLES_DIR = "output/singles"
CATEGORIES_DIR = "output/categories"
FULL_COMPILATION = "output/full_100_compilation.mp3"
PAUSE_BETWEEN_QUESTIONS = 3.0

os.makedirs(CATEGORIES_DIR, exist_ok=True)

def get_single_file(qid, clean_q):
    filename = f"第{qid:03d}題_{clean_q}.mp3"
    filepath = os.path.join(SINGLES_DIR, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing file: {filepath}")
    return filepath

def concat_files_with_silence(file_list, output_path, title, album_title):
    print(f"正在製作合輯: {title} ({len(file_list)} 題)...")
    inputs = []
    filter_parts = []
    
    # 建立 concat 列表或 filter_complex
    # 當檔案數量較多時（例如 100 題），使用 concat demuxer 最穩定
    # 我們在每首曲目之間插播一段 3 秒靜音音檔
    silence_file = "output/tmp/silence_3s.mp3"
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
            # 題與題之間插入 3 秒靜音（最後一題除外）
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

    # 按類別分組
    categories = {}
    all_files = []

    for item in questions:
        qid = item["id"]
        cat = item["category"]
        clean_q = item["question"].replace("？", "").replace("?", "").strip()
        filepath = get_single_file(qid, clean_q)
        
        all_files.append(filepath)
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(filepath)

    # 1. 製作 6 大分類合輯
    cat_names_map = {
        "第一類：身體需求與生理反應": "01_第一類_身體需求與生理反應(1-20題)",
        "第二類：生活作息": "02_第二類_生活作息(21-40題)",
        "第三類：穿著與天氣": "03_第三類_穿著與天氣(41-55題)",
        "第四類：學校與學習": "04_第四類_學校與學習(56-70題)",
        "第五類：外出與安全": "05_第五類_外出與安全(71-85題)",
        "第六類：季節、節日與事件": "06_第六類_季節節日與事件(86-100題)",
    }

    for cat_title, files in categories.items():
        prefix = cat_names_map.get(cat_title, cat_title)
        out_cat_file = os.path.join(CATEGORIES_DIR, f"{prefix}.mp3")
        concat_files_with_silence(files, out_cat_file, cat_title, "生活問答分類合輯")

    # 2. 製作 100 題全套完整大合輯
    concat_files_with_silence(all_files, FULL_COMPILATION, "100題生活情境問答完整大合輯", "特教生活問答全集")
    print("\n所有分類合輯與完整大合輯製作完成！")

if __name__ == "__main__":
    main()
