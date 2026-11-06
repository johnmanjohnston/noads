#!/usr/bin/env python3
import subprocess
import time
import os
import psutil
from gi.repository import Playerctl, GLib
import gi
gi.require_version("Playerctl", "2.0")


main = None


def kill_spotify():
    playerctlVolume = subprocess.run(
        ["playerctl", "-p", "spotify", "volume"], capture_output=True, text=True)
    volumeBeforeClosing = float(playerctlVolume.stdout)

    print("kill_spotify() called")
    for proc in psutil.process_iter():
        # print(proc.name())
        if proc.name() == "spotify":
            proc.kill()

    subprocess.Popen(["spotify", "--disable-gpu"], start_new_session=True)

    time.sleep(1)
    os.system('qdbus org.kde.kglobalaccel /component/kwin org.kde.kglobalaccel.Component.invokeShortcut "Window Minimize"')
    os.system(f"playerctl -p spotify volume {volumeBeforeClosing}")


def on_metadata(player, metadata):
    # print(metadata)
    print(metadata["xesam:title"])

    if 'xesam:artist' in metadata.keys() and 'xesam:title' in metadata.keys():
        # print('on_metadata(): {artist} - {title}'.format(
        #    artist=metadata['xesam:artist'][0], title=metadata['xesam:title']))

        if metadata["xesam:title"] == "Listen to music, ad-free." or "/ad/" in str(metadata["xesam:url"]):
            kill_spotify()
            print("killed spotify")

            while True:
                time.sleep(0.1)
                status = os.system(
                    "playerctl -p spotify metadata | grep spotify")
                if status == 0:
                    break

            time.sleep(0.5)
            os.system("playerctl -p spotify next")


def on_play(player, status):
    print('Playing at volume {}'.format(player.props.volume))


def on_pause(player, status):
    print('Paused the song: {}'.format(player.get_title()))


def init():
    player = Playerctl.Player.new("spotify")
    player.connect('metadata', on_metadata)

    os.system("notify-send spotifyadlessd \"ad nuker attached\"")

    # wait for events
    main = None
    main = GLib.MainLoop()
    main.run()


init()
