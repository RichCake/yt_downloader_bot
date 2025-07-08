import json
import os
import datetime as dt

from yt_dlp import YoutubeDL

OUTPUT_VIDEO_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")
if not os.path.exists(OUTPUT_VIDEO_FOLDER):
    os.mkdir(OUTPUT_VIDEO_FOLDER)

YT_DLP_CMD = ('yt-dlp -f "bv[ext=mp4][vcodec^=avc]+ba[ext=m4a]/b[ext=mp4]" --merge-output-format mp4 %s -P '
              + f'"{OUTPUT_VIDEO_FOLDER}" -o "hhghg.%(ext)s"')


def generate_unique_filename(prefix, suffix):
    now = dt.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S_%f")
    return f"{prefix}{timestamp}{suffix}"


def download(url):
    video_filename = generate_unique_filename("video_", ".mp4")
    opts = {
        'extract_flat': 'discard_in_playlist',
        'format': 'bv[ext=mp4][vcodec^=avc]+ba[ext=m4a]/b[ext=mp4]',
        'fragment_retries': 10,
        'ignoreerrors': 'only_download',
        'merge_output_format': 'mp4',
        'outtmpl': {'default': video_filename},
        'paths': {'home': OUTPUT_VIDEO_FOLDER},
        'postprocessors': [{'key': 'FFmpegConcat',
                            'only_multi_video': True,
                            'when': 'playlist'}],
        'retries': 10
    }
    with YoutubeDL(opts) as ydl:
        ydl.download(url)

    return os.path.join(OUTPUT_VIDEO_FOLDER, video_filename)
