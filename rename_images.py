#!/usr/bin/env python3
"""
批次標準化資料夾下所有 JPG 檔名
使用方式：
    python rename_images.py <資料夾路徑> <前綴名>
範例：
    python rename_images.py ./chihuahua chihuahua_
會將資料夾中所有 .jpg/.jpeg 檔案依照排序重命名為：
    chihuahua_001.jpg, chihuahua_002.jpg, ...
"""
import os
import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="批次標準化資料夾下所有 JPG 檔名"
    )
    parser.add_argument(
        'folder',
        help='目標資料夾路徑，內含要重新命名的 JPG 檔'
    )
    parser.add_argument(
        'prefix',
        help='檔名前綴 (不含數字或副檔名)，例如 "chihuahua_"'
    )
    return parser.parse_args()


def main():
    args = parse_args()
    folder = args.folder
    prefix = args.prefix

    # 驗證資料夾存在
    if not os.path.isdir(folder):
        print(f"錯誤：找不到資料夾 \"{folder}\"")
        sys.exit(1)

    # 取得所有 JPG / JPEG 檔案 (不區分大小寫)
    files = [f for f in os.listdir(folder)
             if os.path.isfile(os.path.join(folder, f))
             and f.lower().endswith(('.jpg', '.jpeg'))]

    if not files:
        print("資料夾中找不到任何 JPG 或 JPEG 檔案。")
        sys.exit(0)

    # 依原始檔名排序，確保順序固定
    files.sort()

    # 計算數字格式長度 (根據檔案數量決定補零位數)
    total = len(files)
    digits = len(str(total))

    # 開始重命名
    for idx, filename in enumerate(files, start=1):
        ext = os.path.splitext(filename)[1].lower()
        new_name = f"{prefix}{str(idx).zfill(digits)}{ext}"
        src = os.path.join(folder, filename)
        dst = os.path.join(folder, new_name)

        # 如果新檔名和舊檔名相同則跳過
        if src == dst:
            continue

        # 避免覆蓋：若目標檔已存在，先跳過並提示
        if os.path.exists(dst):
            print(f"跳過：目標檔已存在 {new_name}")
            continue

        os.rename(src, dst)
        print(f"已重命名：{filename} -> {new_name}")

    print("全部檔案重命名完成！")


if __name__ == '__main__':
    main()
