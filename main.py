#!/usr/bin/env python3
from gi.repository import Playerctl, GLib
import psutil
import os
import time
import subprocess
import shlex

main = None

def kill_spotify():
    print("kill_spotify() called")
    for proc in psutil.process_iter():
        # print(proc.name())
        if proc.name() == "spotify":
            proc.kill()

    subprocess.Popen(["spotify"], start_new_session=True)
    
    time.sleep(1)


def on_metadata(player, metadata):
    # print(metadata)
    print(metadata["xesam:title"])

    if 'xesam:artist' in metadata.keys() and 'xesam:title' in metadata.keys():
        #print('on_metadata(): {artist} - {title}'.format(
        #    artist=metadata['xesam:artist'][0], title=metadata['xesam:title']))

        if metadata["xesam:title"] == "Listen to music, ad-free." or "/ad/" in str(metadata["xesam:url"]):
            kill_spotify()
            print("killed spotify")


def on_play(player, status):
    print('Playing at volume {}'.format(player.props.volume))


def on_pause(player, status):
    print('Paused the song: {}'.format(player.get_title()))

def init():
    player = Playerctl.Player()
    player.connect('metadata', on_metadata)

    # wait for events
    main = None 
    main = GLib.MainLoop()
    main.run()

init()
