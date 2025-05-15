import sys
import os
import flask
import json

import Utility
import Index
import PlayAlbum


class MediaServer:
    # holds a self reference of this class, once __init__ has been called
    INSTANCE = None
    
    # the flask server app; must exist already before MediaServer is created; therefore it is static
    FLASK_APP = flask.Flask(__name__)
    
    def __init__(self, codeDir, musicDir, videoDir):
        self.codeDir = codeDir
        self.musicDir = musicDir
        self.videoDir = videoDir
        
        MediaServer.INSTANCE = self
        MediaServer.FLASK_APP.run(debug=True, host='localhost') # use host='0.0.0.0' to allow all receiver IPs

        
    @FLASK_APP.route('/css/styles.css')
    def getStyles():
        """
        Returns styles.css.
        
        Example call: localhost:5000/css/styles.css
        """
        
        return flask.send_from_directory(MediaServer.INSTANCE.codeDir + "/css", "styles.css")
        
        
    @FLASK_APP.route('/images/back.png')
    def getImageBack():
        """
        Returns back.png.
        
        Example call: localhost:5000/images/back.png
        """
        
        return flask.send_from_directory(MediaServer.INSTANCE.codeDir + "/images", "back.png")
        
        
    @FLASK_APP.route('/music')
    def music():
        """
        Convenience method; returns the same as showFolder() with relativeDirectory = ".".
        """
        return Index.musicFolders(MediaServer.INSTANCE.musicDir, relativeDirectory = ".")
        
        
    @FLASK_APP.route('/music/showFolder')
    def showFolder():
        """
        Returns a HTML page which shows a folder or play view, depending on the folder contents.
        If there is at least 1 directory contained in the relativeDirectory (given as argument), a folder view is shown.
        Otherwise, a play album view is shown.
        
        arg relativeDirectory Path relative to the root media directory.
        
        Example call: localhost:5000/music/showFolder?relativeDirectory=./80er
        """
        argDict = flask.request.args
        relativeDirectory = argDict["relativeDirectory"]
        
        return Index.musicFolders(MediaServer.INSTANCE.musicDir, relativeDirectory = relativeDirectory)
        
        
    @FLASK_APP.route('/music/stream')
    def streamMusic():
        """
        Returns a certain song as file. This song can be used by some other HTML page to be played,
        e.g. via an audio tag.
        
        arg relativeDirectory Path relative to the root music directory, defining the directory where to find the file to play.
        arg song Filename to play.
        
        Example call: localhost:5000/music/stream?relativeDirectory=80er&song=06%20NIK%20KERSHAW%20-%20THE%20RIDDLE.mp3
        """
        argDict = flask.request.args
        relativeDirectory = argDict["relativeDirectory"]
        song = argDict["song"]
        
        return flask.send_from_directory(MediaServer.INSTANCE.musicDir + "/" + relativeDirectory, song)
        
        
    @FLASK_APP.route('/video')
    def video():
        """
        Returns a HTML page showing all videos.
        """
        
        return Index.video(MediaServer.INSTANCE)
        
        
    @FLASK_APP.route('/video/stream')
    def streamVideo():
        """
        Returns the given video as file. This video can be used by some other HTML page to be played,
        e.g. via a video tag.
        
        arg file Filename of the file inside the root video directory to play.
        
        Example call: localhost:5000/video/stream?file=So%20funktioniert%20ein%Muskel.mp4
        """
        argDict = flask.request.args
        fileArg = argDict["file"]
        
        return flask.send_from_directory(MediaServer.INSTANCE.videoDir, fileArg)

    
if (__name__ == "__main__"):
    if (len(sys.argv) != 3):
        print("Syntax: python " + sys.argv[0] + " <absolute music dir> <absolute video dir>");
        sys.exit(-1)
    
    codeDir = os.path.dirname(os.path.realpath(__file__))
    print("codeDir = " + codeDir)
    
    musicDir = sys.argv[1]
    print("musicDir = " + musicDir)
    
    videoDir = sys.argv[2]
    print("videoDir = " + videoDir)
    
    mediaServer = MediaServer(codeDir, musicDir, videoDir)
    