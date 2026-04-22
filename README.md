# 📥 YouTube Video Downloader (Windows EXE)

A simple and powerful desktop YouTube downloader built with PySide6 + yt-dlp.

This tool allows you to download:

* 🎬 Videos
* 🖼️ Thumbnails
* 🎵 Audio (MP3)
* Or both video + thumbnail

No Python installation required — just download and run the `.exe`.

---

## 🚀 Download

👉 **Download the latest EXE here:**

```
https://github.com/<your-username>/<your-repo>/releases/latest/download/win_youtube_download.exe
```

⚠️ **Important:**
You must first upload your `.exe` file to **GitHub Releases**:

### How to add download link:

1. Go to your repo → **Releases**
2. Click **"Create a new release"**
3. Upload:

   * `win_youtube_download.exe`
4. Publish
5. Replace `<your-username>` and `<your-repo>` in the link above

---

## 🖥️ How to Use

### 1. Run the Application

* Double-click `win_youtube_download.exe`
* No installation required

---

### 2. First Launch (Auto Setup)

On first run, the app will automatically download required tools:

* `yt-dlp`
* `FFmpeg`
* `Node.js`

⏳ This may take a few minutes depending on your network.

---

### 3. Download a Video

1. Paste a YouTube link
2. (Optional) Select `cookies.txt`
3. Choose download mode:

   * Video only
   * Thumbnail only
   * Video + Thumbnail
   * Audio (MP3)
4. Select quality (if applicable)
5. Choose output folder
6. Click **Start Download**

---

## 🍪 About Cookies (Important)

Some videos (e.g. private, age-restricted, or members-only) require cookies.

### How to get cookies.txt:

You can export cookies using browser extensions like:

* "Get cookies.txt"

Then load it in the app.

---

## 📂 Output

Downloaded files will be saved to:

```
/video
```

(or your selected folder)

---

## ✨ Features

* GUI interface (no command line needed)
* Auto-install dependencies
* Supports multiple download modes
* Quality selection (1080p / 720p / etc.)
* Integrated logging panel
* No popup CMD window

---

## ⚠️ Notes

* Windows only (`.exe`)
* First run requires internet connection
* Antivirus may warn (common for PyInstaller apps)
* Make sure you have write permissions in the folder

---

## 🛠️ Build from Source (Optional)

If you want to build manually:

```bash
pip install -r requirements.txt
pyinstaller --onefile --noconsole win_youtube_download.py
```

---

## 📜 License

This project uses:

* yt-dlp
* FFmpeg

Please follow their respective licenses.

---

## 💡 Tips

* If download fails → try using cookies
* If video has no sound → FFmpeg may be missing (restart app)
* If blocked → try another format or lower quality

---

如果你想更進一步，我可以幫你優化兩個很關鍵的點（很推薦）：

1. ✅ README 加上 GIF 操作演示（更專業）
2. ✅ 幫你設計 GitHub Releases 自動化（CI/CD 自動打包 exe）

需要的話直接跟我說 👍
