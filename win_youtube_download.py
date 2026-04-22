import sys
import os
import subprocess
import shutil
import zipfile
import requests

from PySide6.QtWidgets import * 
# 導入所有視窗控件（如按鈕、視窗、佈局等）。
from PySide6.QtCore import Qt, QThread, Signal

# ── 路徑處理（支援 exe） ─────────────────
# 這個函數確保無論程式如何運行，BASE_DIR 都會指向程式所在的根目錄。
def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
BIN_DIR = os.path.join(BASE_DIR, "bin") # 在根目錄下定義一個 bin 資料夾路徑。通常用來存放外部依賴的工具。
os.makedirs(BIN_DIR, exist_ok=True)

# 將變量指向 bin 資料夾下的具體執行檔名。
YTDLP = os.path.join(BIN_DIR, "yt-dlp.exe")
FFMPEG = os.path.join(BIN_DIR, "ffmpeg.exe")
NODE = os.path.join(BIN_DIR, "node.exe")

DEFAULT_COOKIES = os.path.join(BASE_DIR, "cookies.txt") # 預設的 cookies 文件路徑。
DEFAULT_OUTPUT = os.path.join(BASE_DIR, "video")

# ── 工具尋找 ─────────────────
# 此代碼僅適用於 Windows 系統
# path：這是首選路徑。通常指程式自身目錄下的工具路徑。開發者希望優先使用這個路徑下的工具，因為版本可控且不依賴用戶電腦環境。
# fallback：這是一個備用名稱列表。如果首選路徑找不到文件，程式會嘗試在系統環境變數（PATH）中搜尋這些名稱。
def find_tool(path, fallback):
    # 如果這個文件存在（例如 bin/ffmpeg.exe 存在），直接返回該路徑。這意味著程式會優先使用自帶的工具，確保功能穩定。
    if os.path.isfile(path):
        return path
    for name in fallback:
        try:
            # 在系統的環境變數 PATH 中搜尋指定的程序名（例如 ffmpeg）。如果找到了，它會返回該程序的完整路徑。
            r = subprocess.run(["where", name], capture_output=True, text=True)
            # 如果在系統 PATH 中找到了工具，返回它的完整路徑。
            if r.returncode == 0:
                return r.stdout.splitlines()[0]
        except:
            pass
    # 如果本地路徑找不到，且遍歷了所有備用名稱在系統中也找不到，最終返回 None，表示工具缺失。
    return None

# ── Installer Thread ─────────────────
# 這是一個多線程類別，專門用於在背景自動下載並配置程式所需的第三方工具（yt-dlp、FFmpeg、Node.js）。
# 使用多線程是為了防止在執行耗時的下載和解壓縮操作時，導致主視窗介面「凍結」（無回應）。
class InstallThread(QThread):
    progress = Signal(int)  # 發射進度百分比（0-100），用於更新進度條。
    status = Signal(str)    # 發射當前的狀態文字（如「下載 yt-dlp...」），用於更新標籤。
    done = Signal() # 發射完成信號，通知主程式安裝已結束。

    def download(self, url, path):
        r = requests.get(url, stream=True)
        # stream=True：這是關鍵參數。它不會一次性將整個文件加載到內存中，而是以流的方式讀取。這對於下載大型文件（如 FFmpeg）非常重要，可以防止記憶體溢出。
        with open(path, "wb") as f:
            for chunk in r.iter_content(1024):  # 以 1024 字節（1KB）為單位分塊讀取並寫入文件。
                if chunk:
                    f.write(chunk)

    def run(self):
        try:
            self.status.emit("Downloading yt-dlp...")
            # 直接從 GitHub 的最新發佈頁下載 yt-dlp.exe 到之前定義的 YTDLP 路徑。
            self.download("https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe", YTDLP)
            self.progress.emit(20)  # 完成後將進度條設為 20%。

            self.status.emit("Downloading FFmpeg...")
            # FFmpeg 通常提供的是 zip 壓縮包，所以先下載到 ffmpeg.zip。
            zip_path = os.path.join(BIN_DIR, "ffmpeg.zip")
            self.download("https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip", zip_path)
            self.progress.emit(40)

            self.status.emit("Extracting FFmpeg...")
            with zipfile.ZipFile(zip_path) as z:
                z.extractall(os.path.join(BIN_DIR, "tmp"))
            # 解壓：將 zip 解壓到一個臨時資料夾 tmp。因為 FFmpeg 的 zip 包內部通常有一層資料夾結構（例如 ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe），不能直接使用。

            # 使用 os.walk 遞歸遍歷解壓後的臨時資料夾。
            for root, _, files in os.walk(os.path.join(BIN_DIR, "tmp")):
                # 找到 ffmpeg.exe 和 ffprobe.exe 後，將其複製到程式根目錄下的 BIN_DIR。
                if "ffmpeg.exe" in files:
                    shutil.copy(os.path.join(root, "ffmpeg.exe"), BIN_DIR)
                if "ffprobe.exe" in files:
                    shutil.copy(os.path.join(root, "ffprobe.exe"), BIN_DIR)

            # 刪除臨時資料夾 tmp 和下載的 zip 檔案，保持目錄整潔。
            shutil.rmtree(os.path.join(BIN_DIR, "tmp"))
            os.remove(zip_path)

            # 完成後進度設為 70%。
            self.progress.emit(70)

            self.status.emit("Downloading Node.js...")
            node_zip = os.path.join(BIN_DIR, "node.zip")
            # 下載特定版本 (v22.14.0) 的 Node.js Windows 二進位 zip 檔。
            self.download("https://nodejs.org/dist/v22.14.0/node-v22.14.0-win-x64.zip", node_zip)

            with zipfile.ZipFile(node_zip) as z:
                z.extractall(os.path.join(BIN_DIR, "tmp2"))
            for root, _, files in os.walk(os.path.join(BIN_DIR, "tmp2")):
                if "node.exe" in files:
                    shutil.copy(os.path.join(root, "node.exe"), BIN_DIR)
            shutil.rmtree(os.path.join(BIN_DIR, "tmp2"))
            os.remove(node_zip)

            self.progress.emit(100)
            self.status.emit("Installation complete")
            self.done.emit()    # 發射 done 信號，通知主程式可以進行下一步

        # 如果在下載、解壓或檔案操作過程中發生任何錯誤（例如網路斷線、磁碟空間不足、權限不足），except 會捕獲錯誤。
        except Exception as e:
            self.status.emit(str(e))    # 將錯誤信息通過 status 信號發送到介面顯示，而不是讓程式崩潰退出。

# ── 下載 Thread ─────────────────
class DownloadThread(QThread):
    log = Signal(str)   # 自定義信號，用於傳遞日誌信息。
    done = Signal(bool)

    def __init__(self, args):
        super().__init__()
        self.args = args

    def run(self):
        try:
            startupinfo = None
            creationflags = 0

            if os.name == "nt": # 判斷當前系統是否為 Windows。
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                creationflags = subprocess.CREATE_NO_WINDOW # 這些標誌告訴 Windows 系統不要創建新的控制台視窗。

            p = subprocess.Popen(
                self.args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                startupinfo=startupinfo,
                creationflags=creationflags
            )
            for line in p.stdout:
                self.log.emit(line.strip())
            p.wait()    # 確保子進程完全結束。
            self.done.emit(p.returncode == 0)
        except Exception as e:
            self.log.emit(str(e))
            self.done.emit(False)

# ── 主視窗 ─────────────────
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 設定視窗標題和大小 (900x700)，並建立一個垂直佈局 (QVBoxLayout) 來放置控件。
        self.setWindowTitle("YouTube Video Downloader")
        self.resize(900, 700)

        self.layout = QVBoxLayout(self)

        # 檢查核心工具 yt-dlp.exe 是否存在。
        if not os.path.exists(YTDLP):
            self.init_installer()   # 顯示安裝介面（下載依賴工具）。
        else:
            self.init_ui()  # 顯示主要的youtube下載操作介面。

    # ── Installer UI ─────────────────
    def init_installer(self):
        self.clear()    

        # 此函數會清空當前介面，顯示一個進度條和標籤。
        self.label = QLabel("First run, installing dependencies...")
        self.progress = QProgressBar()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progress)

        self.thread = InstallThread()
        self.thread.progress.connect(self.progress.setValue)    # 更新進度條
        self.thread.status.connect(self.label.setText)  # 更新狀態文字
        self.thread.done.connect(self.init_ui)  # 完成後切換到主介面
        self.thread.start()

    # ── 主 UI ─────────────────
    def init_ui(self):
        self.clear()

        # 1. 尋找工具路徑
        self.ytdlp = find_tool(YTDLP, ["yt-dlp"])
        self.node = find_tool(NODE, ["node"])
        self.ffmpeg = find_tool(FFMPEG, ["ffmpeg"])

        # URL
        self.url = QLineEdit()  # 讓用戶貼上 YouTube 連結。
        self.url.setPlaceholderText("Enter YouTube link")

        # cookies
        # 一個文字框 (預設填入 cookies.txt 路徑若存在) 和一個「瀏覽」按鈕。
        self.cookies = QLineEdit(DEFAULT_COOKIES if os.path.exists(DEFAULT_COOKIES) else "")
        btn_cookie = QPushButton("Browse")
        btn_cookie.clicked.connect(self.pick_cookie)    # 函數會打開文件選擇對話框。

        cookie_layout = QHBoxLayout()
        cookie_layout.addWidget(self.cookies)
        cookie_layout.addWidget(btn_cookie)

        # 模式
        self.mode = QComboBox() # 下拉選單，提供四種模式。
        self.mode.addItems(["Download Video Only", "Download Thumbnail Only", "Video + Thumbnail", "Download Audio Only (MP3)"])
        self.mode.currentTextChanged.connect(self.update_quality_state) # 當模式改變時，決定是否禁用畫質選項（例如下載 MP3 不需要選畫質）。

        # 品質
        self.quality = QComboBox()  # 下拉選單選擇解析度 (1080p, 720p 等)。
        self.quality.addItems(["Best Quality", "1080p", "720p", "480p", "360p"])

        # output
        # 文字框顯示輸出目錄，按鈕觸發 pick_output 選擇資料夾。
        self.output = QLineEdit(DEFAULT_OUTPUT)
        btn_output = QPushButton("Browse")
        btn_output.clicked.connect(self.pick_output)

        out_layout = QHBoxLayout()
        out_layout.addWidget(self.output)
        out_layout.addWidget(btn_output)

        # 按鈕
        # 「開始下載」按鈕，點擊觸發 start_download。
        self.btn = QPushButton("Start Download")
        self.btn.clicked.connect(self.start_download)

        # # progress
        # self.progress = QProgressBar()
        # self.progress.setRange(0, 0)

        # log
        # 唯讀模式，用於顯示 yt-dlp 的執行日誌。
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        # layout
        self.layout.addWidget(QLabel("YouTube Link"))
        self.layout.addWidget(self.url)

        self.layout.addWidget(QLabel("cookies"))
        self.layout.addLayout(cookie_layout)

        self.layout.addWidget(QLabel("Download Mode"))
        self.layout.addWidget(self.mode)

        self.layout.addWidget(QLabel("Video Quality"))
        self.layout.addWidget(self.quality)

        self.layout.addWidget(QLabel("Save Folder"))
        self.layout.addLayout(out_layout)

        self.layout.addWidget(self.btn)
        # self.layout.addWidget(self.progress)
        self.layout.addWidget(self.log)

    def clear(self):
        while self.layout.count():
            c = self.layout.takeAt(0)
            if c.widget():
                c.widget().deleteLater()

    # ── UI actions ─────────────────
    def pick_cookie(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select cookies.txt")
        if path:
            self.cookies.setText(path)

    def pick_output(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if path:
            self.output.setText(path)

    def update_quality_state(self):
        if self.mode.currentText() in ["Download Video Only", "Video + Thumbnail"]:
            self.quality.setEnabled(True)
        else:
            self.quality.setEnabled(False)

    # ── 下載 ─────────────────
    # 負責將用戶的 GUI 設定轉換為 yt-dlp 能理解的命令列參數。
    def start_download(self):
        url = self.url.text().strip()
        if not url:
            QMessageBox.warning(self, "Notice", "Please enter a link")
            return

        os.makedirs(self.output.text(), exist_ok=True)

        quality_map = {
            "Best Quality": "bestvideo+bestaudio/best",
            "1080p": "bestvideo[height<=1080]+bestaudio",
            "720p": "bestvideo[height<=720]+bestaudio",
            "480p": "bestvideo[height<=480]+bestaudio",
            "360p": "bestvideo[height<=360]+bestaudio",
        }

        args = [self.ytdlp]

        # 添加外部工具路徑 (如果找到的話)
        if self.node:
            args += ["--js-runtimes", f"node:{self.node}"]
        if self.ffmpeg:
            args += ["--ffmpeg-location", os.path.dirname(self.ffmpeg)]

        # 添加 Cookies
        if self.cookies.text():
            args += ["--cookies", self.cookies.text()]

        # 根據模式添加參數
        mode = self.mode.currentText()

        if mode == "Download Thumbnail Only":
            args += ["--write-thumbnail", "--skip-download"]

        elif mode == "Video + Thumbnail":
            args += [
                "-f", quality_map[self.quality.currentText()],
                "--write-thumbnail",
                "--convert-thumbnails", "jpg"
            ]

        elif mode == "Download Audio Only (MP3)":
            args += ["-x", "--audio-format", "mp3"]

        else:
            args += ["-f", quality_map[self.quality.currentText()]]

        args += ["-o", os.path.join(self.output.text(), "%(title)s.%(ext)s")]
        args += [url]

        self.log.clear()
        self.thread = DownloadThread(args)
        self.thread.log.connect(self.log.append)    # 將日誌顯示到介面
        self.thread.done.connect(self.download_done)
        self.thread.start()

    def download_done(self, ok):
        if ok:
            QMessageBox.information(self, "Done", "Download complete")
        else:
            QMessageBox.critical(self, "Error", "Download failed")


# ── 啟動 ─────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QWidget { background:#1a1a2e; color:white; font-size:14px; }
        QLineEdit, QTextEdit, QComboBox { background:#16213e; }
        QPushButton { background:#e94560; padding:6px; }
    """)

    w = MainWindow()
    w.show()

    sys.exit(app.exec())