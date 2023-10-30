import pathlib
import sys
import pytube
import os
import colorama
import shutil

from pytube import exceptions

colorama.init(convert=True)


def desktop_path():
    """
    Returns the path to the desktop either in English or in Greek Windows version.
    :return: The path to Desktop
    """
    if os.path.exists(os.path.join(pathlib.Path.home(), 'Desktop')):
        return os.path.join(pathlib.Path.home(), 'Desktop')
    elif os.path.exists(os.path.join(pathlib.Path.home(), 'Επιφάνεια Εργασίας')):
        return os.path.join(pathlib.Path.home(), 'Επιφάνεια Εργασίας')


def download_video(video_url: str, target_path=None):
    """
    Downloads and returns the selected video file
    :param video_url: The url of the video
    :param target_path: The path for the video to be saved. If None, the default is the path to Desktop.
    :return: Downloaded Video file
    """
    try:
        yt = pytube.YouTube(video_url)
        video = yt.streams \
            .filter(only_audio=True) \
            .first()
        if not target_path:
            file = video.download(output_path=desktop_path())
        else:
            file = video.download(output_path=target_path)
        # result of success
        print(f"{colorama.Fore.GREEN}Song [{video.title}] has been successfully downloaded.{colorama.Style.RESET_ALL}")
        return file
    except pytube.exceptions.RegexMatchError as err:
        print(f'{colorama.Fore.RED}Link is not valid{colorama.Style.RESET_ALL}')
        if debug:
            raise err
        # Needs return here, otherwise it returns None
        if not target_path:
            return download_video(video_url, target_path=desktop_path())
        else:
            return download_video(video_url, target_path)
    except Exception as err:
        raise err


def download_playlist(url: str):
    """
    Downloads the given playlist
    :param url: (str) The url of the playlist
    :return: None
    """
    try:
        playlist = pytube.Playlist(url)
        playlist_folder = os.path.join(desktop_path(), playlist.title)
        try:
            os.mkdir(playlist_folder)
        except FileExistsError:
            shutil.rmtree(playlist_folder)
            print(f"Previous folder [{playlist_folder.title()}] was deleted")
            os.mkdir(playlist_folder)
            print(f"A new folder [{playlist_folder.title()}] is created")
        for video_url in playlist.video_urls:
            video = download_video(video_url=video_url, target_path=playlist_folder)
            convert_to_mp3(video)
        print(f"{colorama.Fore.GREEN}"
              f"Playlist [{playlist.title}] has been successfully downloaded and saved in {playlist_folder}."
              f"{colorama.Style.RESET_ALL}")
    except pytube.exceptions.RegexMatchError as err:
        print(f'{colorama.Fore.RED}Link is not valid{colorama.Style.RESET_ALL}')
        if debug:
            raise err
    except Exception as err:
        raise err


def convert_to_mp3(file):
    """
    Converts video to mp3
    :param file: The path to the given file
    :return: None | Recursion
    """
    base, ext = os.path.splitext(file)
    new_file = base + '.mp3'
    try:
        os.rename(file, new_file)
    except FileExistsError:
        os.remove(new_file)
        return convert_to_mp3(file)


def prompt() -> None:
    video_link = str(input("Paste the link to be downloaded (enter to exit): "))
    if video_link == "":
        sys.exit()
    # TODO: regex for playlist.
    elif 'playlist' in video_link:
        download_playlist(video_link)
    else:
        download_video(video_link)


debug = True

if __name__ == '__main__':
    while True:
        try:
            prompt()
        except (
                exceptions.PytubeError,
                exceptions.RegexMatchError,
                exceptions.ExtractError,
                exceptions.AgeRestrictedError,
                exceptions.LiveStreamError,
                exceptions.HTMLParseError
        ) as err:
            print(err)

# Workaround
# https://github.com/pytube/pytube/issues/1754#issuecomment-1675184514
# https://stackoverflow.com/a/72076299
