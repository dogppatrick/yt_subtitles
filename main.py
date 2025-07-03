import yt_dlp
import whisper
import glob

from urllib.parse import urlparse, parse_qs


# setting up
model = whisper.load_model("medium")
export_dir = "./subtitles/"
download_dir = "./download_yt/"


def download_aduio_clip(url):
    ydl_opts = {
        "format": "worstaudio",
        "outtmpl": f"{download_dir}%(title)s.%(ext)s",  # Save in 'download_yt' folder
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        res_info = ydl.extract_info(url, download=True)
    return res_info


def get_playlist_urls(playlist_url):
    def extract_list_id(url: str) -> str | None:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        return qs.get("list", [None])[0]

    play_list_id = extract_list_id(playlist_url)
    if not play_list_id:
        print("wrong playlist_url")
        return []
    else:
        playlist_url = f"https://www.youtube.com/playlist?list={play_list_id}"

    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        return [entry["url"] for entry in info.get("entries", []) if "url" in entry]


def create_txt(fn, verbose: bool = False):
    result = model.transcribe(fn, language="zh", verbose=verbose)
    export_fn = export_dir + fn.split("\\")[-1][:-3] + "txt"

    def format_timestamp(seconds):
        seconds = int(seconds)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    with open(export_fn, "w", encoding="utf-8") as file:
        for segment in result["segments"]:
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"]
            file.write(f"[{start} --> {end}] {text}\n")
            # file.write(f"{text}\n")


# 自己一個一個加入 url
url_list = [
    "https://www.youtube.com/watch?v=h5d9rsBkd4Y&list=PLlk-i0VfFy44iTM8hWIUJ0ZLXh0fAFYeK&index=2",
    "https://www.youtube.com/watch?v=ReAe7QMzj8A&list=PLlk-i0VfFy44iTM8hWIUJ0ZLXh0fAFYeK&index=3",
]
[download_aduio_clip(url) for url in url_list]
video_list = glob.glob("./download_yt/*.mp4")
[create_txt(fn) for fn in video_list]


## 直接下載整個撥放清單
url_list = get_playlist_urls(
    "https://www.youtube.com/playlist?list=PLlk-i0VfFy44iTM8hWIUJ0ZLXh0fAFYeK"
)
# 下載影片
[download_aduio_clip(url) for url in url_list]
video_list = glob.glob("./download_yt/*.mp4")
[create_txt(fn) for fn in video_list]
