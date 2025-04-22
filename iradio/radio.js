// ===========================================================================================================
// This JS file requires class PlayableAudioObject, const NUM_RADION_STATIONS and const PLAYABLE_AUDIO_OBJECTS
// to be defined. Therefore please use it only for the radio.html / radio2.html sites.
// ===========================================================================================================

// Index (to PLAYABLE_AUDIO_OBJECTS) defining the currently playing radio station.
// -1 if no station is currently selected (i.e. on startup).
var index_currently_playing = -1;

// We use a simple watchdog to handle connection break-offs.
// To detect if a radio station still works, we check every 3 seconds if the currentTime attribute of the audio DOM object changes
// (using watchdog_audio_play_time and watchdog_audio_play_time_previous). If it doesn't change, we recreate the DOM audio object
// and restart playing it. If this occurs 3 times (watchdog_restart_counter), we switch to the next radio station.
var watchdog_audio_play_time = -1;
var watchdog_audio_play_time_previous = -2;
var watchdog_restart_counter = 0;
const WATCHDOG_NUM_RESTARTS_FOR_STATION_SWITCH = 3;
const WATCHDOG_TIMEOUT_MS = 3000;


/**
 * Plays the first audio object, and sets up a watchdog for audio restart on audio halt.
 */
function onLoad () {
  createVisibleDOMObjects ();
  createAudioDOMObjects ();
  
  // default: play station 0 on page load
  play (0);
  
  audioWatchDog();
}


/**
 * Creates the 6 radion station buttons an two rows of 3 divs each and inserts them before the info_text div.
 */
function createVisibleDOMObjects () {
  const row0 = createVisibleDOMDivRowBeforeInfoText (0);
  for (var i = 0; i < 3; ++i)
  {
    const div_radion_station_button = createVisibleDOMDivRadioStationButton (i);
    row0.appendChild(div_radion_station_button);
  }
  
  const row1 = createVisibleDOMDivRowBeforeInfoText (1);
  for (var i = 3; i < 6; ++i)
  {
    const div_radion_station_button = createVisibleDOMDivRadioStationButton (i);
    row1.appendChild(div_radion_station_button);
  }
}


/**
 * Creates a div DOM element and inserts it before the info_text.
 *
 * @param row_id id of the row to create
 * @return the created row div DOM element
 */
function createVisibleDOMDivRowBeforeInfoText (row_id) {
  const info_text = document.getElementById("info_text");
  
  const row = document.createElement("div");
  {
    const row_id_attr = document.createAttribute("id");
    row_id_attr.value = "row" + String(row_id);
    row.setAttributeNode(row_id_attr);
  
    const row_style = document.createAttribute("style");
    row_style.value = "float: top";
    row.setAttributeNode(row_style);
  
    document.body.insertBefore(row, info_text);
  }
  
  return row;
}


/**
 * Creates a div radion station button for PLAYABLE_AUDIO_OBJECTS index idx.
 *
 * @return created div button
 */
function createVisibleDOMDivRadioStationButton (idx) {
  const divi = document.createElement("div");
  {
    const divi_id = document.createAttribute("id");
    divi_id.value = "div" + String(idx);
    divi.setAttributeNode(divi_id);
      
    const divi_class = document.createAttribute("class");
    divi_class.value = "station_button_cls";
    divi.setAttributeNode(divi_class);
      
    const divi_style = document.createAttribute("style");
    divi_style.value = "background: " + PLAYABLE_AUDIO_OBJECTS[idx].background + "; float: left";
    divi.setAttributeNode(divi_style);
      
    const divi_onclick = document.createAttribute("onclick");
    divi_onclick.value = "play (" + String(idx) + ")";
    divi.setAttributeNode(divi_onclick);
  }
    
  const paragraph = document.createElement("p");
  divi.appendChild(paragraph);
    
  const text = document.createTextNode(PLAYABLE_AUDIO_OBJECTS[idx].name);
  paragraph.appendChild(text);
  
  return divi;
}


/**
 * Initially creates the DOM audio objects.
 */
function createAudioDOMObjects () {
  for (var i = 0; i < PLAYABLE_AUDIO_OBJECTS.length; ++i)
  {
    createAudioDOMObject (i);
  }
}


/**
 * Create the audio object for index audio_info_index.
 *
 * @param audio_info_index
 */
function createAudioDOMObject (audio_info_index) {
  var audio_object = document.createElement ('audio');
  
  audio_object.id = PLAYABLE_AUDIO_OBJECTS[audio_info_index].id;
  audio_object.controls = false;
  audio_object.src = PLAYABLE_AUDIO_OBJECTS[audio_info_index].url;
  audio_object.type = 'audio/ogg';

  document.body.appendChild (audio_object);
  
  document.getElementById (PLAYABLE_AUDIO_OBJECTS[audio_info_index].id).ontimeupdate = function () { updateAudioPlayTime () };
}


/**
 * Deletes audio object with index audio_info_index.
 * NOTE: At least on Firefox, the old audio object still seems to interfere even though
 *       it has been destroyed! (Assumption here: this is not the case if the audio object
 *       stops playing due to error.)
 *
 * @param audio_info_index
 */
function deleteAudioObject (audio_info_index) {
  var audio_object = document.getElementById (PLAYABLE_AUDIO_OBJECTS[audio_info_index].id);
  audio_object.pause ();
  document.body.removeChild (audio_object);
}


/**
 * Plays audio object with index audio_info_index. If recreate is true, the target
 * audio object is destroyed and recreated.
 *
 * @param audio_info_index
 * @param recreate
 */
function play (audio_info_index, recreate) {
  // recreate: default false
  if (typeof (recreate) === 'undefined')
  {
    recreate = false;
  }

  // pause the currently playing audio object
  if (index_currently_playing >= 0)
  {
    var current_audio_object = document.getElementById (PLAYABLE_AUDIO_OBJECTS[index_currently_playing].id);
    current_audio_object.pause ();
  }
  
  // recreate the target audio object
  if (recreate)
  {
    deleteAudioObject (audio_info_index);
    createAudioDOMObject (audio_info_index);
  }
  
  // play the target audio object
  watchdog_audio_play_time = -1;
  watchdog_audio_play_time_previous = -2;
  var target_audio_object = document.getElementById (PLAYABLE_AUDIO_OBJECTS[audio_info_index].id);
  target_audio_object.play ();
  index_currently_playing = audio_info_index;
}


/**
 * @param str
 * @return If str has length 1: "0" + str; otherwise: str.
 */
function prependZero (str)
{
  if (str.length == 1)
    return "0" + str;
	
  return str;
}


/**
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


/**
 * Regularly called by the audio stream, updates the information shown in the status
 * bar:
 * - station info with #errors (watchdog_restart_counter)
 * - current time
 *
 * Note that watchdog_audio_play_time is used by the watchdog to detect network errors;
 * so updating this variable is required for normal operation!
 */
function updateAudioPlayTime() {
  watchdog_audio_play_time = document.getElementById (PLAYABLE_AUDIO_OBJECTS[index_currently_playing].id).currentTime;

  var info_text_object = document.getElementById ("info_text");

  var currentdate = new Date();
  var time_str = getTimeString (3600 * currentdate.getHours() 
      + 60 * currentdate.getMinutes()
      + currentdate.getSeconds());

  info_text_object.innerHTML = "<p>" + PLAYABLE_AUDIO_OBJECTS[index_currently_playing].name + "&nbsp;&nbsp; #err: " + watchdog_restart_counter + "&nbsp;&nbsp;&nbsp;" + time_str + "</p>";
}


/**
 * Re-calls itself regularly every WATCHDOG_TIMEOUT_MS ms (e.g. 3 s).
 * If watchdog_audio_play_time hasn't changed, restarts the current audio stream.
 */
function audioWatchDog () {
  if (watchdog_audio_play_time_previous == watchdog_audio_play_time)
  {
    ++watchdog_restart_counter;
	
	if (watchdog_restart_counter % WATCHDOG_NUM_RESTARTS_FOR_STATION_SWITCH != 0)
	{
      // playback has stopped => restart it with recreating the target audio object
	  play (index_currently_playing, true /*recreate*/);
	}
	else
	{
	  // WATCHDOG_NUM_RESTARTS_FOR_STATION_SWITCH errors in a row => switch to next radio station (stop current, start next)...
	  var current_audio_object = document.getElementById (PLAYABLE_AUDIO_OBJECTS[index_currently_playing].id);
      current_audio_object.pause ();
	  
	  play ((index_currently_playing + 1) % NUM_RADION_STATIONS);
	  
	  // ...and reset the watchdog counter
	  watchdog_restart_counter = 0;
	}
	
  }

  watchdog_audio_play_time_previous = watchdog_audio_play_time;
  
  setTimeout (audioWatchDog, WATCHDOG_TIMEOUT_MS);
}