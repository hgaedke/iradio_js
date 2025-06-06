import Utility


def create(mediaDir, relativeDirectory):
    '''
    @return a HTML page for playing the audio files contained in relativeDirectory.
    
    @param mediaDir Absolute path of the media root directory.
    @param relativeDirectory Path of the directory to play files from, relative to the root media directory.
    '''
    (dirs, songs) = Utility.getDirectoryContents(mediaDir + "/" + relativeDirectory)
    albumName = extractAlbumNameFromPath(relativeDirectory)
    
    # === HTML output ===
    html = """
      <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <link href="/css/styles.css" rel="stylesheet" />
        <script type="text/javascript" src="js/common.js"></script> 
      <script>
      
class AudioInfo {
  constructor (name, src) {
    this.name = name;
    this.src = src;
  }
}
      
var audio_infos = [
    """
    
    for i in range(len(songs)):
        song = songs[i]
        html += "new AudioInfo (\"" + song + "\", \"" + Utility.getSongURL(relativeDirectory, song) + "\")"
        
        if (i < len(songs) - 1):
            html += ","
        html += "\n"
        
    html += """
];

var currently_playing = -1; // index (of audio_infos) of the currently played song

    """

    html += "var num_titles = " + str(len(songs)) + ";\n"
    
    html += """

/*!
 * Initializes the audio object and plays the first song.
 */
function onLoadLocalMedia () {
  // set ended listener
  var audio_obj = document.getElementById ('audio');
  audio_obj.addEventListener("ended", playNext);
  
  playTitle(0);
  
  updateTime();
}

/*!
 * Playes the song with index title_no.
 */
function playTitle(title_no) {
  var audio_obj = document.getElementById ('audio');
  
  if (currently_playing != -1) {
    // pause and rewind audio
    audio_obj.pause();
    audio_obj.currentTime = 0;
  
    // un-highlight the current song in the song list
    var title_old_p = document.getElementById ('title_of_album_' + currently_playing + '_p');
    title_old_p.innerHTML = audio_infos[currently_playing].name;
  }
  
  // switch to new song
  currently_playing = title_no;
  
  // set audio_source to src of current song index
  var audio_source = document.getElementById ('audio_source');
  audio_source.src = audio_infos[currently_playing].src;
  
  // highlight the song in the song list
  var title_p = document.getElementById ('title_of_album_' + title_no + '_p');
  title_p.innerHTML = "<b>" + audio_infos[currently_playing].name + "</b>";
  
  // load new audio source (important, as the previous one is still in the cache)
  audio_obj.load();
  
  // play audio
  audio_obj.play ();
  
  // make sure that the current song is centered (if possible)
  scrollToTitle(currently_playing);
}

/*!
 * Playes the next song.
 */
function playNext() {
  playTitle((currently_playing + 1) % num_titles);
}

/*!
 * Centers (if possible) song no. title_no.
 */
function scrollToTitle(title_no) {
  var titlesDiv = document.getElementById('list_of_titles');
  var titleDivHeight = titlesDiv.clientHeight;
  
  var firstTitle = document.getElementById('title_of_album_0');
  
  var currentTitle = document.getElementById('title_of_album_' + title_no);
  var currentTitleHeight = currentTitle.clientHeight;
  
  // absolute y pos of first song
  var y0 = firstTitle.offsetTop;
  
  // relative y pos of current song
  var yActualRel = currentTitle.offsetTop - y0;
  
  // target relative y pos of current song is in the middle of the div, helf song height above
  var yTargetRel = titlesDiv.clientHeight / 2 - currentTitle.clientHeight / 2;
  
  // calculate transformation from yActualRel to yTargetRel
  var scrollY = yActualRel - yTargetRel;
  
  // scroll
  titlesDiv.scrollTop = scrollY;
}

/*!
 * Shows the index page.
 */
function backToParentDir() {
  url = String(window.location);
  let indexSlash = url.lastIndexOf("/");
  if (indexSlash != -1) {
    url = url.substring(0, indexSlash);
  }
  
  window.location = url;
}

/*!
 * @param str
 * @return If str has length 1: "0" + str; otherwise: str.
 */
function prependZero (str)
{
  if (str.length == 1)
    return "0" + str;
	
  return str;
}

/*!
 * @param seconds
 * @return A formatted time string "hh:mm:ss" from seconds.
 */
function getTimeString (seconds)
{
  var play_time_sec = Math.floor(seconds) % 60;
  var play_time_min = Math.floor(seconds / 60) % 60;
  var play_time_hour = Math.floor(seconds / 3600) % 24;
  
  var play_time_sec_str = prependZero (String (play_time_sec));
  var play_time_min_str = prependZero (String (play_time_min));
  var play_time_hour_str = prependZero (String (play_time_hour));
	
  return play_time_hour_str + ":" + play_time_min_str + ":" + play_time_sec_str;
}

/*!
 * Regularly called (first by onLoad, then by itself. Updates the time in the headline.
 */
function updateTime() {
  var time_object = document.getElementById ("time");

  var currentdate = new Date();
  var time_str = getTimeString (3600 * currentdate.getHours() 
      + 60 * currentdate.getMinutes()
      + currentdate.getSeconds());

  time_object.innerHTML = "<p>" + time_str + "</p>";
  
  setTimeout (updateTime, 100); // 100 ms until next update
}
    """
    
    html += """
      </script>
      </head>
      <body style="margin: 0; padding: 0;" onload="onLoadLocalMedia ();">
        <div id="caption" class="info_text_cls">
          <p>App: Local Music</p>
        </div>
        <div id="back_and_album">
          <div id="back" class="back_button_cls" onclick="backToParentDir()">
            <p><img src="/images/back.png" height="60"></p>
          </div>
          <div id="album_info" class="album_info_cls">
    """
    html += "          <p>" + albumName + "</p>\n"
    html += """
          </div>
          <div id="time" class="time_cls">
            <p></p>
          </div>
        </div>
        <div id="list_of_titles" style="width: 99%; height: 60%; overflow: auto;">
    """
    
    background1 = "#FFC0C0"
    background2 = "#C0C0FF"
    
    for i in range(len(songs)):
        song = songs[i]
        if (i % 2 == 0):
            background = background1
        else:
            background = background2
        
        html += "<div id=\"title_of_album_" + str(i) + "\" class=\"title_of_album_cls\" style=\"background: " + background + "\" onclick=\"playTitle(" + str(i) + ")\">\n"
        html += "  <p id=\"title_of_album_" + str(i) + "_p\">" + song + "</p>\n"
        html += "</div>\n"
    
    html += """
        </div>
        <div id="audio_control" class="audio_control_cls">
          <p>
            <audio controls id="audio" style="width: 99%;">
    """
    html += "              <source id=\"audio_source\" src=\"" + Utility.getSongURL(relativeDirectory, songs[0]) + "\" type=\"audio/ogg\">\n"
    html += """
            </audio>
          </p>
        </div>
      </body>
    </html>
    """
    
    return html
    
    
def extractAlbumNameFromPath(directory):
    '''
    @return The substring of directory representing the part after the last slash.
    @param directory A directory path.
    '''
    indexSlash = directory.rfind("/")
    return directory[indexSlash + 1 : len(directory)]