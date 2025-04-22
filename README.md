# iradio_js
Internet radio website based on pure HTML / JavaScript. Comes with a FLASK-based media center for local MP3 and video playback.

This readme file contains a how-to for Windows as well as for Rasbian (running on Raspberry PI).

# How-to for Windows
![Screenshot of the internet radio app in Firefox browser on Windows.](/../main/docs/iradio_home_windows.jpg)

## Install and use just the internet radio
* Clone the repository. We assume here you clone it to "c:\iradio_js".
* Open "c:\iradio_ja\iradio\home.html" in your local browser.
* Click one of the radio station buttons and listen to the music.

## Install and use the local MP3 and video playback in addition
In addition to the previous steps:
* Install Python 3.8.3 or newer.
* Copy video files (.mp4) of your choice to folder "c:\iradio_js\video".
* Copy MP3 music files of your choice to the music folder, where each music file needs to be located in an album directory, e.g. "c:\iradio_js\music\my_album\my_music.mp3". You can have multiple files per album and multiple albums as well.
* Start the Python- and FLASK-based MediaServer:
    python "c:\iradio_js\iradio\MediaServer.py" "c:\iradio_js\iradio\music" "c:\iradio_js\iradio\video"
* Open "c:\iradio_ja\iradio\home.html" in your local browser.
* Click on the flash button in the left toolbar to show your music albums. Click on an album to enter it and to play the music inside.
* Click on the play button in the left toolbar to show your videos. Use the HTML media controls to start/stop a video. Scroll down to see the other videos.