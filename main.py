import pathlib
import sys
import pytube
import os
import colorama

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


def download_video(video_url):
    """
    Downloads and returns the selected video file
    :param video_url: The url of the video
    :return: Downloaded Video file
    """
    try:
        yt = pytube.YouTube(video_url)
        video = yt.streams \
            .filter(only_audio=True) \
            .first()
        file = video.download(output_path=desktop_path())
        # result of success
        print(f"{colorama.Fore.GREEN}Song [{video.title}] has been successfully downloaded.{colorama.Style.RESET_ALL}")
        return file
    except pytube.exceptions.RegexMatchError as err:
        print(f'{colorama.Fore.RED}Link is not valid{colorama.Style.RESET_ALL}')
        if debug:
            raise err
        return download_video()  # Needs return here, otherwise it returns None
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
        for video_url in playlist.video_urls:
            video = download_video(video_url=video_url)
            convert_to_mp3(video)
        print(
            f"{colorama.Fore.GREEN}Playlist [{playlist.title}] has been successfully downloaded.{colorama.Style.RESET_ALL}")
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


debug = False

if __name__ == '__main__':
    while True:
        video_link = str(input("Paste the link to be downloaded (enter to exit): "))
        if video_link == "":
            sys.exit()
        # TODO: regex for playlist.
        elif 'playlist' in video_link:
            download_playlist(video_link)
        else:
            download_video(video_link)
