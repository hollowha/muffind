#!/usr/bin/env python3
"""
批次壓縮圖片檔案，專為muffin和chihuahua資料夾設計
使用PIL/Pillow庫來壓縮JPG圖片，盡量減小檔案大小同時保持可接受的畫質

使用方式：
    python compress_images.py

功能：
    - 自動壓縮muffin和chihuahua資料夾中的所有JPG圖片
    - 調整圖片尺寸到合適的大小（適合網頁顯示）
    - 優化JPEG品質設定
    - 顯示壓縮前後的檔案大小對比
    - 支援批次處理，顯示進度
"""

import os
import sys
from PIL import Image
import argparse
from pathlib import Path


def get_file_size(filepath):
    """取得檔案大小（以bytes為單位）"""
    return os.path.getsize(filepath)


def format_size(size_bytes):
    """將檔案大小格式化為可讀的字串"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def compress_image(input_path, output_path=None, max_width=600, max_height=600, quality=60):
    """
    壓縮單張圖片
    
    Args:
        input_path: 輸入圖片路徑
        output_path: 輸出圖片路徑（如果為None則覆蓋原檔案）
        max_width: 最大寬度
        max_height: 最大高度
        quality: JPEG品質 (1-100)
    
    Returns:
        tuple: (原始檔案大小, 壓縮後檔案大小)
    """
    if output_path is None:
        output_path = input_path
    
    # 記錄原始檔案大小
    original_size = get_file_size(input_path)
    
    try:
        # 開啟圖片
        with Image.open(input_path) as img:
            # 轉換為RGB模式（確保JPEG相容性）
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # 計算新的尺寸（保持長寬比）
            original_width, original_height = img.size
            
            # 只有當圖片比目標尺寸大時才調整大小
            if original_width > max_width or original_height > max_height:
                # 計算縮放比例
                width_ratio = max_width / original_width
                height_ratio = max_height / original_height
                scale_ratio = min(width_ratio, height_ratio)
                
                new_width = int(original_width * scale_ratio)
                new_height = int(original_height * scale_ratio)
                
                # 調整圖片大小（使用高品質的重採樣）
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 保存壓縮後的圖片
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        # 記錄壓縮後檔案大小
        compressed_size = get_file_size(output_path)
        
        return original_size, compressed_size
        
    except Exception as e:
        print(f"處理圖片時發生錯誤 {input_path}: {e}")
        return original_size, original_size


def compress_folder(folder_path, max_width=600, max_height=600, quality=60):
    """
    壓縮資料夾中的所有圖片
    
    Args:
        folder_path: 資料夾路徑
        max_width: 最大寬度
        max_height: 最大高度
        quality: JPEG品質
    
    Returns:
        tuple: (總原始大小, 總壓縮後大小, 處理的檔案數量)
    """
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"資料夾不存在: {folder_path}")
        return 0, 0, 0
    
    # 取得所有JPG檔案
    jpg_files = list(folder_path.glob("*.jpg")) + list(folder_path.glob("*.jpeg"))
    jpg_files += list(folder_path.glob("*.JPG")) + list(folder_path.glob("*.JPEG"))
    
    if not jpg_files:
        print(f"在資料夾 {folder_path} 中找不到JPG檔案")
        return 0, 0, 0
    
    total_original_size = 0
    total_compressed_size = 0
    processed_count = 0
    
    print(f"\n開始處理資料夾: {folder_path}")
    print(f"找到 {len(jpg_files)} 個圖片檔案")
    print("-" * 60)
    
    for i, jpg_file in enumerate(jpg_files, 1):
        print(f"處理中 ({i}/{len(jpg_files)}): {jpg_file.name}", end=" ... ")
        
        original_size, compressed_size = compress_image(
            str(jpg_file), 
            max_width=max_width, 
            max_height=max_height, 
            quality=quality
        )
        
        total_original_size += original_size
        total_compressed_size += compressed_size
        processed_count += 1
        
        # 計算壓縮比例
        if original_size > 0:
            compression_ratio = (1 - compressed_size / original_size) * 100
            print(f"完成 ({format_size(original_size)} -> {format_size(compressed_size)}, 壓縮 {compression_ratio:.1f}%)")
        else:
            print("完成")
    
    return total_original_size, total_compressed_size, processed_count


def main():
    parser = argparse.ArgumentParser(description="批次壓縮muffin和chihuahua資料夾中的圖片")
    parser.add_argument('--max-width', type=int, default=600, help='最大寬度 (預設: 600)')
    parser.add_argument('--max-height', type=int, default=600, help='最大高度 (預設: 600)')
    parser.add_argument('--quality', type=int, default=60, help='JPEG品質 1-100 (預設: 60)')
    parser.add_argument('--folders', nargs='+', default=['muffin', 'chihuahua'], 
                       help='要處理的資料夾名稱 (預設: muffin chihuahua)')
    
    args = parser.parse_args()
    
    # 檢查PIL是否可用
    try:
        from PIL import Image
    except ImportError:
        print("錯誤: 需要安裝Pillow庫")
        print("請執行: pip install Pillow")
        sys.exit(1)
    
    print("=" * 60)
    print("圖片批次壓縮工具")
    print("=" * 60)
    print(f"設定 - 最大尺寸: {args.max_width}x{args.max_height}, 品質: {args.quality}")
    
    total_original_size = 0
    total_compressed_size = 0
    total_files = 0
    
    # 處理每個資料夾
    for folder_name in args.folders:
        folder_path = Path(folder_name)
        
        if folder_path.exists():
            original_size, compressed_size, file_count = compress_folder(
                folder_path, 
                max_width=args.max_width, 
                max_height=args.max_height, 
                quality=args.quality
            )
            
            total_original_size += original_size
            total_compressed_size += compressed_size
            total_files += file_count
            
            if file_count > 0:
                folder_compression = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
                print(f"\n資料夾 {folder_name} 總結:")
                print(f"  處理檔案: {file_count} 個")
                print(f"  原始大小: {format_size(original_size)}")
                print(f"  壓縮後大小: {format_size(compressed_size)}")
                print(f"  節省空間: {format_size(original_size - compressed_size)} ({folder_compression:.1f}%)")
        else:
            print(f"\n警告: 資料夾 {folder_name} 不存在，跳過處理")
    
    # 顯示總結
    print("\n" + "=" * 60)
    print("壓縮完成！總結報告:")
    print("=" * 60)
    
    if total_files > 0:
        total_compression = (1 - total_compressed_size / total_original_size) * 100 if total_original_size > 0 else 0
        space_saved = total_original_size - total_compressed_size
        
        print(f"總處理檔案: {total_files} 個")
        print(f"總原始大小: {format_size(total_original_size)}")
        print(f"總壓縮後大小: {format_size(total_compressed_size)}")
        print(f"總節省空間: {format_size(space_saved)} ({total_compression:.1f}%)")
        
        if space_saved > 0:
            print(f"\n🎉 成功壓縮！節省了 {format_size(space_saved)} 的儲存空間")
        else:
            print("\n✅ 所有圖片已經是最佳大小")
    else:
        print("沒有找到任何圖片檔案可供處理")


if __name__ == '__main__':
    main()
