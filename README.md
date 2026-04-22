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
https://github.com/JeffereyWu-AI/win-youtube-downloader/releases/latest/download/win_youtube_download.exe
```
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
2. Select `cookies.txt`
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




## 🛠️ Build from Source (Optional)

If you want to build manually:

```bash
pyinstaller --onefile --noconsole win_youtube_download.py
```

---

## 📜 License

This project uses:

* yt-dlp
* FFmpeg

Please follow their respective licenses.




