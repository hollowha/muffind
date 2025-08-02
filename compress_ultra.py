#!/usr/bin/env python3
"""
超級壓縮版本 - 更激進的壓縮設定
使用更低的品質設定和更小的尺寸來達到最大的壓縮比例

使用方式：
    python compress_ultra.py --quality 40 --max-width 400 --max-height 400
    python compress_ultra.py --quality 30 --max-width 300 --max-height 300  # 極限壓縮
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


def compress_image_ultra(input_path, output_path=None, max_width=400, max_height=400, quality=40, progressive=True):
    """
    超級壓縮模式 - 使用更激進的設定
    
    Args:
        input_path: 輸入圖片路徑
        output_path: 輸出圖片路徑（如果為None則覆蓋原檔案）
        max_width: 最大寬度（預設400px）
        max_height: 最大高度（預設400px）
        quality: JPEG品質 (1-100，預設40）
        progressive: 使用漸進式JPEG
    
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
            
            # 更激進的尺寸調整策略
            if original_width > max_width or original_height > max_height:
                # 計算縮放比例
                width_ratio = max_width / original_width
                height_ratio = max_height / original_height
                scale_ratio = min(width_ratio, height_ratio)
                
                new_width = int(original_width * scale_ratio)
                new_height = int(original_height * scale_ratio)
                
                # 調整圖片大小
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 使用更激進的JPEG設定
            save_kwargs = {
                'format': 'JPEG',
                'quality': quality,
                'optimize': True,
                'progressive': progressive,
                'subsampling': 0,  # 使用4:2:0色度子採樣（最大壓縮）
                'qtables': 'web_low'  # 使用網頁優化的低品質量化表
            }
            
            # 保存壓縮後的圖片
            img.save(output_path, **save_kwargs)
        
        # 記錄壓縮後檔案大小
        compressed_size = get_file_size(output_path)
        
        return original_size, compressed_size
        
    except Exception as e:
        print(f"處理圖片時發生錯誤 {input_path}: {e}")
        return original_size, original_size


def compress_folder_ultra(folder_path, max_width=400, max_height=400, quality=40):
    """
    超級壓縮資料夾中的所有圖片
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
    
    print(f"\n🚀 超級壓縮模式 - 處理資料夾: {folder_path}")
    print(f"找到 {len(jpg_files)} 個圖片檔案")
    print(f"設定: 尺寸{max_width}x{max_height}, 品質{quality}")
    print("-" * 60)
    
    for i, jpg_file in enumerate(jpg_files, 1):
        print(f"處理中 ({i}/{len(jpg_files)}): {jpg_file.name}", end=" ... ")
        
        original_size, compressed_size = compress_image_ultra(
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
        
        # 每處理100個檔案顯示進度
        if i % 100 == 0:
            current_savings = total_original_size - total_compressed_size
            current_percentage = (1 - total_compressed_size / total_original_size) * 100 if total_original_size > 0 else 0
            print(f"📊 進度報告: 已處理 {i}/{len(jpg_files)} 個檔案，目前節省 {format_size(current_savings)} ({current_percentage:.1f}%)")
    
    return total_original_size, total_compressed_size, processed_count


def main():
    parser = argparse.ArgumentParser(description="超級壓縮模式 - 最大程度壓縮圖片")
    parser.add_argument('--max-width', type=int, default=400, help='最大寬度 (預設: 400，極限建議: 300)')
    parser.add_argument('--max-height', type=int, default=400, help='最大高度 (預設: 400，極限建議: 300)')
    parser.add_argument('--quality', type=int, default=40, help='JPEG品質 1-100 (預設: 40，極限建議: 30)')
    parser.add_argument('--folders', nargs='+', default=['muffin', 'chihuahua'], 
                       help='要處理的資料夾名稱 (預設: muffin chihuahua)')
    parser.add_argument('--backup', action='store_true', help='壓縮前備份原始檔案')
    
    args = parser.parse_args()
    
    # 檢查PIL是否可用
    try:
        from PIL import Image
    except ImportError:
        print("錯誤: 需要安裝Pillow庫")
        print("請執行: pip install Pillow")
        sys.exit(1)
    
    # 顯示警告
    print("⚠️  警告: 超級壓縮模式")
    print("=" * 60)
    print("這個模式會大幅壓縮圖片，可能會明顯影響畫質！")
    print(f"設定 - 最大尺寸: {args.max_width}x{args.max_height}, 品質: {args.quality}")
    print("建議的壓縮級別:")
    print("  - 品質 50-40: 可接受的畫質損失，大幅節省空間")
    print("  - 品質 40-30: 明顯畫質損失，極大節省空間")
    print("  - 品質 30以下: 嚴重畫質損失，最大節省空間")
    print()
    
    # 確認是否繼續
    if not args.backup:
        confirm = input("⚠️  這將直接覆蓋原始檔案！是否繼續？(y/n): ").lower().strip()
        if confirm != 'y':
            print("已取消操作")
            sys.exit(0)
    
    total_original_size = 0
    total_compressed_size = 0
    total_files = 0
    
    # 處理每個資料夾
    for folder_name in args.folders:
        folder_path = Path(folder_name)
        
        if folder_path.exists():
            # 如果需要備份
            if args.backup:
                backup_folder = folder_path.parent / f"{folder_name}_backup"
                if not backup_folder.exists():
                    print(f"📁 創建備份資料夾: {backup_folder}")
                    backup_folder.mkdir()
                    # 複製所有檔案到備份資料夾
                    import shutil
                    for file in folder_path.glob("*.jpg"):
                        shutil.copy2(file, backup_folder / file.name)
                    for file in folder_path.glob("*.jpeg"):
                        shutil.copy2(file, backup_folder / file.name)
            
            original_size, compressed_size, file_count = compress_folder_ultra(
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
                print(f"\n📊 資料夾 {folder_name} 總結:")
                print(f"  處理檔案: {file_count} 個")
                print(f"  原始大小: {format_size(original_size)}")
                print(f"  壓縮後大小: {format_size(compressed_size)}")
                print(f"  節省空間: {format_size(original_size - compressed_size)} ({folder_compression:.1f}%)")
        else:
            print(f"\n⚠️  警告: 資料夾 {folder_name} 不存在，跳過處理")
    
    # 顯示總結
    print("\n" + "🎯" * 20)
    print("超級壓縮完成！最終報告:")
    print("🎯" * 20)
    
    if total_files > 0:
        total_compression = (1 - total_compressed_size / total_original_size) * 100 if total_original_size > 0 else 0
        space_saved = total_original_size - total_compressed_size
        
        print(f"📈 總處理檔案: {total_files} 個")
        print(f"📊 總原始大小: {format_size(total_original_size)}")
        print(f"📉 總壓縮後大小: {format_size(total_compressed_size)}")
        print(f"💾 總節省空間: {format_size(space_saved)} ({total_compression:.1f}%)")
        
        if space_saved > 0:
            print(f"\n🎉 超級壓縮成功！額外節省了 {format_size(space_saved)} 的儲存空間")
            print(f"💡 相比原始設定，總壓縮率提升到 {total_compression:.1f}%")
        else:
            print("\n✅ 圖片已經達到最佳壓縮狀態")
    else:
        print("❌ 沒有找到任何圖片檔案可供處理")


if __name__ == '__main__':
    main()
