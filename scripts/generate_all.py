#!/usr/bin/env python3
"""
批次生成自閉症特教教材語音：
100 題「什麼時候……？」日常認知問答
語音：微軟臺灣國語女聲 (zh-TW-HsiaoChenNeural)
語速：90% (-10%)
每題問題後停頓 3.0 秒，再播放參考答案
"""

import asyncio
import json
import os
import subprocess
import time
import edge_tts

DATA_FILE = "data/questions.json"
OUTPUT_DIR = "output/singles"
VOICE = "zh-TW-HsiaoChenNeural"
RATE = "-10%"
PAUSE_SEC = 3.0

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("output/tmp", exist_ok=True)

async def synth_with_retry(text, voice, rate, out_path, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            comm = edge_tts.Communicate(text, voice=voice, rate=rate)
            await comm.save(out_path)
            # Verify file exists and is > 0 bytes
            if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
                return True
        except Exception as e:
            print(f"[Warning] Failed attempt {attempt} for '{text}': {e}")
        await asyncio.sleep(1.0 * attempt)
    raise RuntimeError(f"Failed to synthesize '{text}' after {max_retries} attempts.")

async def process_question(item):
    qid = item["id"]
    question = item["question"]
    answer = item["answer"]
    
    clean_q = question.replace("？", "").replace("?", "").strip()
    final_out = os.path.join(OUTPUT_DIR, f"第{qid:03d}題_{clean_q}.mp3")
    
    if os.path.exists(final_out) and os.path.getsize(final_out) > 5000:
        print(f"[{qid:03d}/100] 已存在，跳過: {os.path.basename(final_out)}")
        return final_out

    tmp_q = f"output/tmp/q_{qid}.mp3"
    tmp_a = f"output/tmp/a_{qid}.mp3"

    # 1. 語音合成問題
    await synth_with_retry(question, VOICE, RATE, tmp_q)
    await asyncio.sleep(0.3)

    # 2. 語音合成答案
    await synth_with_retry(answer, VOICE, RATE, tmp_a)
    await asyncio.sleep(0.3)

    # 3. ffmpeg 拼接：問題 + 3.0秒靜音 + 答案
    cmd = [
        "ffmpeg", "-y",
        "-i", tmp_q,
        "-f", "lavfi", "-t", str(PAUSE_SEC), "-i", "anullsrc=r=24000:cl=mono",
        "-i", tmp_a,
        "-filter_complex", "[0:a][1:a][2:a]concat=n=3:v=0:a=1[out]",
        "-map", "[out]",
        "-metadata", f"title=第{qid}題：{clean_q}",
        "-metadata", "artist=特教生活問答",
        "-metadata", "album=100題生活情境認知",
        "-c:a", "libmp3lame", "-b:a", "128k",
        final_out
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    if os.path.exists(tmp_q): os.remove(tmp_q)
    if os.path.exists(tmp_a): os.remove(tmp_a)

    print(f"[{qid:03d}/100] 完成: {os.path.basename(final_out)}")
    return final_out

async def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
        
    print(f"開始生成 {len(questions)} 題逐字稿語音...")
    for item in questions:
        await process_question(item)
        await asyncio.sleep(0.2)
        
    print("全部 100 題單題 MP3 生成完畢！")

if __name__ == "__main__":
    asyncio.run(main())
