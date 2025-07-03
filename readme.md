
# YouTube 音訊轉文字工具 🎵➡️📝

這是一個使用 OpenAI Whisper 將 YouTube 影片音訊轉換成中文文字的工具，支援單一影片或整個播放清單的批次處理。

# 免責聲明
本說明文件由 AI 助手 Claude 生成，僅供參考。

requirements.txt 可能不適用於所有作業系統或環境（本版本於 Windows 平台測試）。

關於 PyTorch 安裝及 GPU 設定問題，因環境差異較大，故不在本工具支援範圍內，  
請使用者依照官方文件或其他資源自行解決。


## 功能特色 ✨

- 🎬 **支援 YouTube 影片和播放清單**
- 🌏 **專為中文音訊優化**
- ⏰ **包含完整時間戳記**
- 📦 **一鍵批次處理**
- 🔄 **錯誤恢復機制**
- 📱 **適用於 Google Colab**

## 快速開始 🚀

### 1. 開啟 Google Colab
- 前往 [Google Colab](https://colab.research.google.com/)
- 上傳 `yt_subtitle.ipynb` 檔案

### 2. 修改影片連結
根據你的需求選擇其中一種方式：

**方式一：指定影片**
```python
# 在 Cell 5 中修改這個列表
url_list = [
    "https://www.youtube.com/watch?v=你的影片ID",
    "https://www.youtube.com/watch?v=另一個影片ID",
]
```

**方式二：整個播放清單**
```python
# 在 Cell 6 中修改這個連結
playlist_url = "https://www.youtube.com/playlist?list=你的播放清單ID"
```

### 3. 執行程式
- 依序執行每個 Cell (按 Shift+Enter)
- 第一次執行會自動下載 Whisper 模型
- 等待處理完成後下載結果

## 詳細使用說明 📋

### Cell 執行順序

| Cell | 說明 | 預估時間 |
|------|------|----------|
| 1 | 安裝套件 | 1-2 分鐘 |
| 2 | 匯入模組 | 10 秒 |
| 3 | 載入模型 | 1-3 分鐘 |
| 4 | 定義函數 | 5 秒 |
| 5/6 | 處理影片 | 取決於影片長度 |
| 7 | 查看結果 | 5 秒 |
| 8 | 預覽內容 | 10 秒 |
| 9 | 下載檔案 | 30 秒 |

### 輸出格式

生成的文字檔案包含兩種格式：

```
[00:01:23 --> 00:01:25] 這是轉換的文字內容
這是轉換的文字內容

[00:01:25 --> 00:01:28] 下一段的文字內容
下一段的文字內容
```

## 設定選項 ⚙️

### 模型選擇
在 Cell 3 中可以修改模型大小：

```python
# 速度與準確度平衡
model = whisper.load_model("medium")  # 預設

# 更快速度 (較低準確度)
model = whisper.load_model("small")

# 更高準確度 (較慢速度)
model = whisper.load_model("large")
```

### 語言設定
在 `create_txt` 函數中可以修改語言：

```python
# 中文 (預設)
result = model.transcribe(fn, language="zh")

# 英文
result = model.transcribe(fn, language="en")

# 自動偵測
result = model.transcribe(fn)
```

## 常見問題 ❓

### Q: 第一次執行很慢？
A: 第一次會下載 Whisper 模型檔案 (約 1-3 GB)，之後就會很快。

### Q: 某些影片下載失敗？
A: 可能原因：
- 影片被設為私人或已刪除
- 地區限制
- 版權保護
- 網路連線問題

### Q: 轉換結果不準確？
A: 建議：
- 選擇更大的模型 (`large`)
- 確認音訊品質良好
- 檢查是否為中文內容

### Q: 如何處理長影片？
A: 工具會自動分段處理，但建議：
- 使用 `medium` 或 `small` 模型節省時間
- 確保 Colab 連線穩定
- 可以分批處理

### Q: 檔案太大無法下載？
A: 系統會自動將多個檔案打包成 zip，單一檔案過大時建議：
- 分段處理影片
- 使用 Google Drive 同步

## 技術規格 🔧

### 系統需求
- Google Colab (免費版即可)
- 穩定的網路連線
- 足夠的 Google Drive 空間

### 支援格式
- **輸入**：YouTube 影片/播放清單連結
- **輸出**：UTF-8 編碼的 .txt 文字檔案
- **音訊**：自動下載最低品質音訊 (節省時間)

### 處理能力
- **單一影片**：無限制
- **播放清單**：建議 < 50 個影片
- **影片長度**：建議 < 2 小時/影片

## 錯誤處理 🛠️

程式包含完整的錯誤處理機制：

```python
✅ 下載成功會顯示綠色勾號
❌ 下載失敗會顯示紅色叉號和錯誤訊息
📊 處理完成後會顯示統計資訊
```

即使某個影片失敗，也不會影響其他影片的處理。

## 進階使用 🎯

### 自訂檔案名稱
修改 `download_audio_clip` 函數中的 `outtmpl` 參數：

```python
"outtmpl": f"{download_dir}%(uploader)s_%(title)s.%(ext)s"
```

### 保留時間戳記
修改 `create_txt` 函數來自訂輸出格式：

```python
# 只保留時間戳記
file.write(f"[{start} --> {end}] {text}\n")

# 只保留純文字
file.write(f"{text}\n")
```

### 批次處理多個播放清單
```python
playlists = [
    "播放清單1的URL",
    "播放清單2的URL",
]

for playlist in playlists:
    urls = get_playlist_urls(playlist)
    # 處理每個播放清單...
```

## 授權與聲明 📄

- 本工具僅供學習和研究使用
- 請遵守 YouTube 使用條款
- 請尊重影片創作者的版權
- 不得用於商業用途

## 更新日誌 📅

### v1.0.0 (2024-07-03)
- 初始版本發布
- 支援 YouTube 影片和播放清單
- 整合 Whisper 中文轉換
- 完整的錯誤處理機制
- Google Colab 優化

## 支援與回饋 💬

如果遇到問題或有建議，歡迎：
- 檢查常見問題部分
- 確認網路連線和影片連結
- 嘗試重新執行相關的 Cell

## 效能優化建議 ⚡

1. **選擇合適的模型大小**
   - 測試用：`small`
   - 一般用：`medium`
   - 高品質：`large`

2. **批次處理策略**
   - 一次處理 5-10 個影片
   - 避免同時處理過多長影片

3. **網路優化**
   - 使用穩定的網路連線
   - 避免在網路尖峰時間處理

4. **儲存空間管理**
   - 定期清理暫存檔案
   - 及時下載結果檔案

---

**祝你使用愉快！** 🎉