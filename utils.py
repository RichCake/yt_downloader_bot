import os
from pprint import pprint

import ffmpeg


def get_video_resolution(path):
    """
    Возвращает разрешение видео с помощью ffmpeg
    :param path: Полный или относительный путь к файлу.
    :return: (width, height) или None в случае ошибки
    """
    try:
        info = ffmpeg.probe(path)["streams"]
        [video_info] = filter(lambda x: x["codec_type"] == "video", info)
        w, h = video_info["coded_width"], video_info["coded_height"]
        return w, h
    except ffmpeg.Error as e:
        print("ОШИБКА ОТ ffmpeg:")
        print(e)
    except Exception as e:
        print("ОШИБКА ЧТЕНИЯ ВЫВОДА ffprobe")
        print(e)
