from MediaServer import MediaServer
import Utility
import PlayAlbum


def musicFolders(musicDir, relativeDirectory):
    '''
    Shows a folder view, if relativeDirectory contains at least 1 directory. Otherwise shows a play album view.
    
    param musicDir Path to the global music directory.
    param relativeDirectory Relative path from global music directory to the directory which contents shall be shown.
    '''
    # contains only folders? => folder view
    # else => playable view
    (dirs, files) = Utility.getDirectoryContents(musicDir + "/" + relativeDirectory)
    if dirs:
        return musicFolderView(musicDir, relativeDirectory)
    else:
        return PlayAlbum.create(musicDir, relativeDirectory)
        

def musicFolderView(musicDir, relativeDirectory):
    '''
    Shows a folder view for musicDir + "/" + relativeDirectory.
    
    param musicDir Path to the global music directory.
    param relativeDirectory Relative path from global music directory to the folder which contents shall be shown.
    '''
    
    # get contained folders (files are irrelevant)
    (dirs, files) = Utility.getDirectoryContents(musicDir + "/" + relativeDirectory)
    
    # === HTML output ===
    html = """
      <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <link href="/css/styles.css" rel="stylesheet" />
      <script>
/*!
 * Opens the given URL in the current frame.
 */
function openURL (url) {
  window.location = url;
}

/*!
 * Shows the parent dir.
 */
function backToParentDir() {
  url = String(window.location);
  let indexSlash = url.lastIndexOf("/");
  if (indexSlash != -1) {
    url = url.substring(0, indexSlash);
  }
  
  window.location = url;
}
      </script>
      </head>
      <body style="margin: 0; padding: 0;" >
        <div id="caption" class="info_text_cls">
          <p>App: Local Music</p>
        </div>
    """
    
    # back button (if not root)
    if relativeDirectory != ".":
        html += """
            <div id="back_button">
              <div id="back" class="back_button_cls" onclick="backToParentDir()">
                <p><img src="/images/back.png" height="60"></p>
              </div>
        """
    
    background1 = "#FFC0C0"
    background2 = "#C0C0FF"
    
    for i in range(len(dirs)):
        directory = dirs[i]
        
        if (i % 2 == 0):
            background = background1
        else:
            background = background2
        
        urlShowFolder = "/music/showFolder?relativeDirectory=" + relativeDirectory + "/" + directory
        
        html += "<div id=\"div_folder_" + str(i) + "\">\n"
        # note that using " instead of ' is your DEATH!
        html += "  <div class=\"open_folder_button_cls\" style=\"float: left; background: " + background + "\" onclick=\"openURL('" + urlShowFolder + "')\">\n"
        html += "    <p>" + directory + "</p>\n"
        html += "  </div>\n"
        html += "</div>\n"
        
    html += Utility.genericFooter()
    return html
    
    
def video(mediaServer):
    # get videos in reverse order, so that the newest (assuming date in front) is shown first
    (dirs, videos) = Utility.getDirectoryContents(mediaServer.videoDir, reverse = True)
    
    # === HTML output ===
    html = """
      <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <link href="/css/styles.css" rel="stylesheet" />
      </head>
      <body style="margin: 0; padding: 0;" >
        <div id="caption" class="info_text_cls">
          <p>App: Local Videos</p>
        </div>
    """
    
    background1 = "#FFC0C0"
    background2 = "#C0C0FF"
    
    for i in range(len(videos)):
        video = videos[i]
        
        if (i % 2 == 0):
            background = background1
        else:
            background = background2
        
        html += "<div id=\"div_video_" + str(i) + "\" style=\"background-color:" + background + ";\">\n"
        html += "  <p>\n"
        html += "    <video width=\"100%\" controls>\n"
        html += "      <source src=\"" + Utility.getVideoURL(video) + "\" type=\"video/mp4\">\n"
        html += "      Your browser does not support the video tag.\n"
        html += "    </video>\n"
        html += "  </p>\n"
        html += "</div>\n"
        
    html += Utility.genericFooter()
    return html