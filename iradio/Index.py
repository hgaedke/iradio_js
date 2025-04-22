from MediaServer import MediaServer
import Utility


def music(mediaServer):
    # get music albums
    musicAlbums = Utility.getSortedListOfAlbums(mediaServer.musicDir)
    
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
      </script>
      </head>
      <body style="margin: 0; padding: 0;" >
        <div id="caption" class="info_text_cls">
          <p>App: Local Media</p>
        </div>
    """
    
    background1 = "#FFC0C0"
    background2 = "#C0C0FF"
    
    for i in range(len(musicAlbums)):
        album = musicAlbums[i]
        
        if (i % 2 == 0):
            background = background1
        else:
            background = background2
        
        urlPlayAlbum = "/music/playAlbum?album=" + album
        
        html += "<div id=\"div_album_" + str(i) + "\">\n"
        # note that using " instead of ' is your DEATH!
        html += "  <div class=\"album_play_button_cls\" style=\"float: left; background: " + background + "\" onclick=\"openURL('" + urlPlayAlbum + "')\">\n"
        html += "    <p>" + album + "</p>\n"
        html += "  </div>\n"
        html += "</div>\n"
        
    html += Utility.genericFooter()
    return html
    
def video(mediaServer):
    # get videos
    videos = Utility.getListOfVideos(mediaServer.videoDir)
    
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