import os


def genericHeader():
    html = """
      <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <link href="css/styles.css" rel="stylesheet" />
      </head>
      <body style="margin: 0; padding: 0;" >
        <div id="caption" class="info_text_cls">
          <p>App: Local Music</p>
        </div>
    """
    
    return html
    

def genericFooter():
    html = """
        <div id="info_text" class="info_text_cls">
          <p></p>
        </div>
      </body>
      </html>
    """
    
    return html
    
    
def getSortedListOfAlbums(musicDir):
    """
    Example call: localhost:5000/music/albums
    """
    # get list of files in current directory
    albums = []
    for (dirpath, dirnames, filenames) in os.walk(musicDir):
        albums.extend(dirnames)
        break
    albums.sort()
    return albums

    
def getListOfTitlesOfAlbum(musicDir, album):
    # get sorted list of files in the given album's directory
    titles = []
    for (dirpath, dirnames, filenames) in os.walk(musicDir + "/" + album):
        titles.extend(filenames)
        break
    
    titles.sort()
    return titles
    
    
def getTitleURL(album, title):
    """
    Returns the URL under which the given title of the given album is accessible as file.
    """
    return "/music/title?album=" + album + "&title=" + title
    
    
def getSortedListOfVideos(videoDir):
    """
    Example call: localhost:5000/video
    """
    # get list of files in current directory
    videos = []
    for (dirpath, dirnames, filenames) in os.walk(videoDir):
        videos.extend(filenames)
        break
    videos.sort()
    return videos
    
    
def getVideoURL(video):
    """
    Returns the URL under which the given video is accessible as file.
    """
    return "/video/title?file=" + video