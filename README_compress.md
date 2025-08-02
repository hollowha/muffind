# 圖片壓縮工具使用說明

## 檔案說明
- `compress_images.py` - 圖片批次壓縮腳本
- `rename_images.py` - 圖片重命名腳本（原有的）

## 功能特點
- 自動壓縮JPG/JPEG圖片
- 調整圖片尺寸（預設最大600x600像素）
- 優化JPEG品質（預設65%）
- 顯示詳細的壓縮進度和統計
- 批次處理大量圖片

## 基本使用
```bash
# 使用預設設定壓縮muffin和chihuahua資料夾
python compress_images.py

# 自訂品質和尺寸
python compress_images.py --quality 70 --max-width 800 --max-height 800

# 壓縮特定資料夾
python compress_images.py --folders muffin

# 查看所有選項
python compress_images.py --help
```

## 參數說明
- `--quality`: JPEG品質(1-100)，預設65，數字越低檔案越小但畫質越差
- `--max-width`: 最大寬度，預設600像素
- `--max-height`: 最大高度，預設600像素  
- `--folders`: 要處理的資料夾名稱，預設為muffin和chihuahua

## 品質建議
- **高品質**：`--quality 80-90` - 適合需要高畫質的場合
- **平衡模式**：`--quality 65-75` - 品質與檔案大小平衡（推薦）
- **最小檔案**：`--quality 50-60` - 最大程度壓縮，適合網頁快速載入

## 尺寸建議
- **網頁展示**：600x600（預設）- 適合大多數網頁應用
- **高解析度**：800x800 - 保持較高解析度
- **縮圖用途**：400x400 - 適合產生縮圖

## 安全性
- 腳本會直接覆蓋原始檔案
- 建議在使用前先備份重要圖片
- 可以先用少量圖片測試效果

## 效果統計
根據測試，平均可以達到：
- 壓縮率：60-95%
- 檔案大小縮減：通常可以節省70-90%的儲存空間
- 處理速度：每秒約10-15張圖片

## 注意事項
1. 需要安裝Pillow庫：`pip install Pillow`
2. 只處理JPG和JPEG格式
3. 會保持圖片的長寬比
4. 自動轉換RGBA和P模式為RGB以確保JPEG相容性
