# iradio_js
Internet radio website based on pure HTML / JavaScript. Comes with a FLASK-based media center for local MP3 and video playback.

This readme file contains a how-to for Windows as well as for Rasbian (running on Raspberry PI).

# How-to for Windows
![Screenshot of the internet radio app in Firefox browser on Windows.](/../main/docs/iradio_home_windows.jpg)

## Install and use just the internet radio
* Clone the repository. We assume here you clone it to "c:\iradio_js".
* Open "c:\iradio_ja\iradio\home.html" in your local browser.
* Click one of the radio station buttons and listen to the music.
* To adjust the radio stations to use and the background colors, edit "c:\iradio_js\iradio\radio.html" or "c:\iradio_js\iradio\radio2.html" and adjust the array **PLAYABLE_AUDIO_OBJECTS** accordingly.

## Install and use the local MP3 and video playback in addition
In addition to the previous steps:
* Install Python 2.7.16 or newer.
* Copy video files (.mp4) of your choice to folder "c:\iradio_js\video".
* Copy MP3 music files of your choice to the music folder, where each music file needs to be located in an album directory, e.g. "c:\iradio_js\music\my_album\my_music.mp3". You can have multiple files per album and multiple albums as well.
* Start the Python- and FLASK-based MediaServer:
    python "c:\iradio_js\iradio\MediaServer.py" "c:\iradio_js\iradio\music" "c:\iradio_js\iradio\video"
* Open "c:\iradio_ja\iradio\home.html" in your local browser.
* Click on the flash button in the left toolbar to show your music albums. Click on an album to enter it and to play the music inside.
* Click on the play button in the left toolbar to show your videos. Use the HTML media controls to start/stop a video. Scroll down to see the other videos.

# How-to for Rasbian
This assumes that you have a Raspberry PI with Rasbian OS and a touch screen attached, and that you use username "pi".

![Screenshot of the internet radio app in Chromium browser on Rasbian.](/../main/docs/iradio_home_rasbian.jpg)

## Install and use just the internet radio
* Clone the repository. We assume here you clone it to "/home/pi/Desktop/iradio_js".
* Open "/home/pi/Desktop/iradio_js/iradio/home.html" in your local browser; I use chromium-browser.
* Click one of the radio station buttons and listen to the music.
* To adjust the radio stations to use and the background colors, edit "/home/pi/Desktop/iradio_js/iradio/radio.html" or "/home/pi/Desktop/iradio_js/iradio/radio2.html" and adjust the array **PLAYABLE_AUDIO_OBJECTS** accordingly.

## Install and use the local MP3 and video playback in addition
In addition to the previous steps:
* Install Python 2.7.16 or newer.
* Copy video files (.mp4) of your choice to folder "/video".
* Copy MP3 music files of your choice to folder "/music", where each music file needs to be located in an album directory, e.g. "/music/my_album/my_music.mp3". You can have multiple files per album and multiple albums as well.
* Configure the Python- and FLASK-based MediaServer to be started automatically on login, and show the internet radio automatically on login: open "/etc/xdg/lxsession/LXDE-pi/autostart" and add the following two lines:
    @python /home/pi/Desktop/iradio_js/iradio/MediaServer.py /music /video
    @chromium-browser --start-fullscreen --incognito --autoplay-policy=no-user-gesture-required ~/Desktop/iradio_js/iradio/home.html
* Restart your Raspberry.
* Click on the flash button in the left toolbar to show your music albums. Click on an album to enter it and to play the music inside.
* Click on the play button in the left toolbar to show your videos. Use the HTML media controls to start/stop a video. Scroll down to see the other videos.