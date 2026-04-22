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

👉 [⬇️ Download Windows EXE here](https://github.com/JeffereyWu-AI/win-youtube-downloader/releases/latest/download/win_youtube_download.exe)

---

## 🍪 Cookies Required (Important)

This app **requires cookies** to download most YouTube videos.

### Why?

YouTube blocks many downloads unless you're logged in.

### 🧩 Step-by-step (Chrome)

1. Open **Google Chrome**
2. Install chrome extension: "Get cookies.txt LOCALLY"
3. Log in to YouTube
4. Click the extension → export `cookies.txt`
5. Load it in the app later


### ⚠️ Notes

* Cookies file may expire → re-export if download fails
* Keep your cookies private (contains login session)

---

## 🖥️ How to Use

### 1. Run the Application

* Double-click `win_youtube_download.exe`
* No installation required


### 2. First Launch (Auto Setup)

On first run, the app will automatically download required tools:

* `yt-dlp`
* `FFmpeg`
* `Node.js`

⏳ This may take a few minutes depending on your network.



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


## ✨ Features

* GUI interface (no command line needed)
* Auto-install dependencies
* Supports multiple download modes
* Quality selection (1080p / 720p / etc.)



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




