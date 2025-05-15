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
    
    
def getDirectoryContents(mediaDir, reverse = False):
    """
    @return (sorted list of contained dirs, sorted list of contained files).
    
    @param mediaDir Root media (music or video) directory.
    @param reverse If True, dirs and files are sorted in reverse order.
    """
    dirs = []
    files = []
    for content in os.listdir(mediaDir):
        if os.path.isdir(mediaDir + "/" + content):
            dirs.append(content)
        if os.path.isfile(mediaDir + "/" + content):
            files.append(content)
    dirs.sort(reverse = reverse)
    files.sort(reverse = reverse)
    return (dirs, files)
    
    
def getSongURL(relativeDirectory, filename):
    """
    @return the URL under which the file given by filename is accessible.
    
    @param relativeDirectory Relative path from the root music directory to the directory where the file is stored.
    @param filename Filename of the file which is addressed.
    """
    return "/music/stream?relativeDirectory=" + relativeDirectory + "&song=" + filename
    
    
def getVideoURL(video):
    """
    @return the URL under which the given video is accessible as file.
    """
    return "/video/stream?file=" + video