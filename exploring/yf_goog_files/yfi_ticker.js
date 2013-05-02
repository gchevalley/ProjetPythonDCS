if(typeof(YAHOO.Finance) == "undefined" || typeof(YAHOO.Finance.TickerPanel) == "undefined") {
  // Ticker panel for user settings/preferences
  YAHOO.namespace("YAHOO.Finance.TickerPanel"); 
}

if(typeof(YAHOO.Finance) == "undefined" || typeof(YAHOO.Finance.Ticker) == "undefined") {
  // Stock ticker
  YAHOO.namespace("YAHOO.Finance.Ticker");
}

if(typeof(YAHOO.Finance) == "undefined" || typeof(YAHOO.Finance.StreamingTickerPanel) == "undefined") {
  // Panel for streaming on/off; ticker on/off
  YAHOO.namespace("YAHOO.Finance.StreamingTickerPanel"); 
}

// Initilize global variables
// Ticker Speed
var TICKER_SPEED_SLOW = 0;
var TICKER_SPEED_MEDIUM = 1;
var TICKER_SPEED_FAST = 2
var stockTickerSpeed = TICKER_SPEED_SLOW;
// Ticker Scroll
var TICKER_SCROLL_ON = 0;
var TICKER_SCROLL_OFF = 1;
var stockTickerScroll = TICKER_SCROLL_ON;
// Ticker Display
var TICKER_DISPLAY_RECENT_QUOTES = 0;
var TICKER_DISPLAY_MARKET_SUMMARY = 1;
var stockTickerDisplay = TICKER_DISPLAY_RECENT_QUOTES;
// Absolute vs Percent change
var TICKER_DISPLAY_ABSOLUTE_CHANGE = 0;
var TICKER_DISPLAY_PERCENT_CHANGE = 1;
var stockTickerChange = TICKER_DISPLAY_PERCENT_CHANGE;
// Color
var TICKER_COLOR_GREEN = 0;
var TICKER_COLOR_TEAL = 1;
var stockTickerColor = TICKER_COLOR_GREEN;
// TT on/off
var STOCK_TICKER_ON = 1;
var STOCK_TICKER_OFF = 0;
var stockTickerONOFF = STOCK_TICKER_ON;
var ttDisplayed = true;

var tArray = []; // Symbol array
var tickerX = []; // X coordinates of the tickers displayed
var tickerSymIndex = []; // Index into the tArray symbol array
var firstTickerIndex = 0; // Index of the first ticker displayed
var ttStreamStarted = false;
var marketSumIndex = -1;
var marketSumDn = [];

function yfi_stock_ticker_click(event){
  var i=0;
//  console.log("Mouse Down event." +
//            " ClientX = " + event.clientX +
//          " ClientY = " + event.clientY +
//        " ScreenX = " + event.screenX +
//      " ScreenY = " + event.screenY);

  // Get Canvas left offset
  var canvas = document.getElementById("stock_ticker");
  var obj = canvas;
  var canLeftOffset = 0;
  while (obj != undefined && obj.tagName != 'BODY') {
      canLeftOffset += obj.offsetLeft;
      obj = obj.offsetParent;
  }   
//  console.log("Canvas left offset = " + canLeftOffset);

  var canMouseXOffset = event.clientX - canLeftOffset;
//  console.log("Canvas mouse click X offset = " + canMouseXOffset);

  for (i=0; i<tickerX.length; i++) {
//    console.log("Checking symbol " + tArray[tickerSymIndex[i]] + " xoffset " + tickerX[i]);
    if (tickerX[i] > canMouseXOffset) {
      break;
    }
  }
  
  if (i>0) {
    // console.log("Ticker clicked: " + tArray[tickerSymIndex[i-1]]);
       tt_href = '/q?s='+tArray[tickerSymIndex[i-1]];
    // ULT
       var slk = tArray[tickerSymIndex[i-1]];
       var sec = "stockticker";
       var keyw = tArray[tickerSymIndex[i-1]];
       var pg_ssk = YAHOO.util.Dom.get("spaceid");
       var ttUltObj = {
            "keyw": keyw,
            "sec": sec,
            "slk": slk
       };
       if (pg_ssk) {
            ttUltObj[YAHOO.ULT.SRC_SPACEID_KEY] = pg_ssk.innerHTML;
       }
	
       // console.log("BEACON: " + YAHOO.ULT.BEACON + ",  ttUltObj: " + YAHOO.lang.JSON.stringify(ttUltObj));
       setTimeout(function() {
            YAHOO.ULT.beacon_click(ttUltObj);
       }, 100);
       window.location.href = '/q?s='+tArray[tickerSymIndex[i-1]];
  } else {
    // console.log("No ticker found under the mouse");
  }
}

YAHOO.util.Event.addListener("stock_ticker", "click", yfi_stock_ticker_click);

// Initialize ticker panel. 
YAHOO.Finance.TickerPanel=function(){
	document.getElementById('yfi_stock_ticker_settings').style.display="block";
        tickerPanel = new YAHOO.widget.Panel("yfi_stock_ticker_settings", {width:"260px", visible:false, constraintoviewport:true } );
	tickerPanel.render();
        YAHOO.util.Event.addListener("yfi_stock_ticker_settings_icon", "click", tickerPanel.show, tickerPanel, true);
        YAHOO.util.Event.addListener("submitStSettings", "click", tickerPanelSubmit);

}

// Initialize streaming ticker panel. 
// Initialize streaming ticker panel.
YAHOO.Finance.StreamingTickerPanel=function(){
	document.getElementById('yfi_streaming_ticker_panel').style.display="block";
        stickerPanel = new YAHOO.widget.Panel("yfi_streaming_ticker_panel", {width:"160px", visible:false, constraintoviewport:true } );
        stickerPanel.render();
        YAHOO.util.Event.addListener("yfi_pg_settings_icon", "click", stickerPanel.show, stickerPanel, true);
}

// Load streaming ticker panel
YAHOO.Finance.StreamingTickerPanel();

var removeStockTicker = function(event) {
	tptoggleOnoffText(0);
}

var hideTT = function() {
        ttDisplayed = false;
        document.getElementById('yfi_ticker_container').style.display="none";
        document.getElementById('yfi_stock_ticker_settings').style.display="none";
}

var showTT = function() {
        ttDisplayed = true;
	document.getElementById('yfi_ticker_container').style.display="block";
        document.getElementById('yfi_stock_ticker_settings').style.display="block";
}

// call when user clicks TT ON/OFF preference
var tptoggleOnoffText = function(txt) {
        var ttCookie = "TT"; // User preferences for stock ticker
        var yfiCookie = "PRF"; // Get recent quotes tickers
	var yDom = YAHOO.util.Dom;
	var userSignedIn = yDom.get("yfi_user_signed_in").value;

	var sq_cookie_val = YFS.util.cookieMgr.existsInCookie("PRF", "sq=0");
        // console.log("sq_cookie_val = " + sq_cookie_val);
        // If streaming is turned off, do not change any ticker-tape setting
        if (sq_cookie_val) {
                txt = 0;
        }

	// console.log("txt = "+txt);
        if (txt == "1") {
	// console.log ("txt val="+txt);
		setSubCookie(ttCookie,"tt_userPref", 1);
		if (userSignedIn === "0") {
			saveTTSettingsUDB(1);
		}
		showTT();
                document.getElementById('tt_on').style.display="inline";
                document.getElementById('tt_off').style.display="none";
             
		YAHOO.Finance.Ticker();
        } else {
	// console.log ("txt off val="+txt);
		setSubCookie(ttCookie,"tt_userPref", 0);
		if (userSignedIn === "0") {
			saveTTSettingsUDB(0);
		}
		hideTT();
                document.getElementById('tt_off').style.display="inline";
		document.getElementById('tt_on').style.display="none";
        }
}

// When this function is called, it assumes that streaming is ON
// Check TT cookie and show Ticker Tape
var checkAndShowTT = function() {
        var ttCookie = "TT"; // User preferences for stock ticker
        var ttCookie_val = getSubCookie(ttCookie, "tt_userPref");

        if (ttCookie_val == 0) {
                hideTT();
		document.getElementById('tt_off').style.display="inline";
                document.getElementById('tt_on').style.display="none";
        } else {
                showTT();
		document.getElementById('tt_on').style.display="inline";
                document.getElementById('tt_off').style.display="none";
        }
}

var enableTTSettings = function(enable) {	   	
	if(enable == 0) {
		var disableclr = "grey";
		document.getElementById('ticker_onoff').style.color = disableclr;
        	document.getElementById('tt_on').style.color= disableclr;
        	document.getElementById('tt_off').style.color= disableclr;

		tptoggleOnoffText(0);
	} else {
		var enableclr = "#444444";
		var enable_href_clr = "#1A4588";
		document.getElementById('ticker_onoff').style.color = enableclr;
	 	document.getElementById('tt_on').style.color= enable_href_clr;
                document.getElementById('tt_off').style.color= enable_href_clr;

	}
}

var initToggle = function() {
        var yDom = YAHOO.util.Dom;
        var ttCookie = "TT"; // User preferences for stock ticker
        var yfi_tt_on = document.getElementById('yfi_tt_on').value;
        var userSignedIn = yDom.get("yfi_user_signed_in").value;
	var sq_cookie_val = YFS.util.cookieMgr.existsInCookie("PRF", "sq=0");

        // If user is signed in, set the TT cookie based on user's preference
        if (userSignedIn === "0") {
                // console.log("User is signed in. User TT preference = " + yfi_tt_on);
                setSubCookie(ttCookie, "tt_userPref", yfi_tt_on);
        } else {
                // console.log("User is NOT signed in");
        }

        // console.log("sq_cookie_val = " + sq_cookie_val);
        if (sq_cookie_val) {
                hideTT();
                enableTTSettings(0);
                
        } else {
		checkAndShowTT();
                enableTTSettings(1);
	}
}


YAHOO.util.Event.addListener("yfi_stock_ticker_close_icon", "click", removeStockTicker);

var yDom = YAHOO.util.Dom;

// returns value of scrolling radio buttons as string
var getIsPaused = function() {
	return getRadioValue("isPaused").toString();
};

// returns value of scrolling speed radio buttons as string
var getScrollingSpeed = function() {
        return getRadioValue("scrollingSpeed").toString();
};

// returns value of background color of ticker
var getTickerColor = function() {
        return getRadioValue("tickerColor").toString();
};

// returns value of display for ticker : change or %change
var getTickerChange = function() {
        return getRadioValue("tickerChange").toString();
};

// returns value of checked radio button
var getRadioValue = function(radioName) {
        var input = YAHOO.util.Dom.getElementsBy(function (el) {
                return (el.name === radioName && el.checked);
            }, 'input', 'yfi_stock_ticker_settings', null, null, null, true);

        var value = input.value;
	    // console.log("input radio checked="+input.value);

        return value;
};

// returns value of selected option
var getSelectValue = function() {
	var tickerEl = yDom.get("yfi_stock_ticker_settings");
	var tickerListEl = tickerEl.getElementsByTagName("select")[0];
	var optionList = tickerListEl.getElementsByTagName("option");
        var numOption = optionList.length;
        for (var i = 0; i < numOption; i++) {
        	if (optionList[i].selected) {
			// console.log(i.toString());
			return i.toString();
               	}
     	}
};

var settingsUDBCallback = {
        success:function(o) {
                if(o.status == 200){
                // console.log('Success');
                }
        },
        failure:function(o){
                // console.log('Failure');
        },
        timeout: 5000
};

// Save user preferences to UDB
var saveSettingsUDB = function(e){
  	// console.log('Save settings in UDB');
       	var crumbEl = YAHOO.util.Dom.get(".yficrumb");
       	var crumbValue = (crumbEl != null)? crumbEl.value : "";
        var sUrl = "/webservice/v1/preferences?.yficrumb=" + crumbValue;
        var scroll = getIsPaused();
        var scrollSpeed = getScrollingSpeed();
        var scrollDisplay = getSelectValue();
        // var bgColor = getTickerColor();
       	var change = getTickerChange();
        var postData = "tt_scroll="+scroll+"&tt_speed="+scrollSpeed+"&tt_display="+scrollDisplay+"&tt_change="+change;
	// var postData = "tt_scroll="+scroll+"&tt_speed="+scrollSpeed+"&tt_display="+scrollDisplay+"&tt_color="+bgColor+"&tt_change="+change;
	// console.log("postData = "+postData);
        YAHOO.util.Connect.initHeader("Content-Type", "application/x-www-form-urlencoded");
        var request = YAHOO.util.Connect.asyncRequest('POST', sUrl, settingsUDBCallback, postData);
};

var prev_tt_onoff = -1; // Set initial value to -1, so that the first tt_onoff setting gets saved to UDB
var saveTTSettingsUDB = function(tt_onoff){
        // If the tt_onoff setting has not changed, do not save it to UDB again
        if (prev_tt_onoff == tt_onoff) {
                return false;
        }
        prev_tt_onoff = tt_onoff;
    	// console.log('Save settings in UDB');
       	var crumbEl = YAHOO.util.Dom.get(".yficrumb");
       	var crumbValue = (crumbEl != null)? crumbEl.value : "";
        var sUrl = "/webservice/v1/preferences?.yficrumb=" + crumbValue;
        var postData = "tt_userPref="+tt_onoff;
	// console.log("postData = "+postData);
        YAHOO.util.Connect.initHeader("Content-Type", "application/x-www-form-urlencoded");
        var request = YAHOO.util.Connect.asyncRequest('POST', sUrl, settingsUDBCallback, postData);
};

// Get TT Cookie
var getSubCookie = function(cookieName, subName) {
	var yCookie = YAHOO.Finance.Cookie;
        var cookieValue = yCookie.get(cookieName);
        var nvArray = [];
        var nvPair = [];
        // console.log("getSubCookie: looking up " + cookieName + "." + subName);
        // console.log("cookieValue = " + cookieValue);
        if (cookieValue) {
                nvArray = cookieValue.split('&');
        }
        // console.log("nvArray.length = " + nvArray.length);
        for (var i = 0; i < nvArray.length ; i++) {
                nvPair = nvArray[i].split('=');
                if (nvPair.length == 1) {
                        // console.log("nvPair[0] = " + nvPair[0]);
                        nvPair = nvPair[0].split('=');
                }
                // console.log("i=" + i + ": nvPair.length = " + nvPair.length);
                if (nvPair.length > 1) {
                        // console.log("nvPair[0] = " + nvPair[0] + " nvPair[1] = " + nvPair[1]);
                        if (nvPair[0] === subName) {
                                // console.log("Returning " + nvPair[1]);
                                return nvPair[1];
                        }
                }
        }
        // console.log("getSubCookie: " + cookieName + "." + subName + " not found.  Returning -1");
        return -1;
};

// Set TT Cookie
var setSubCookie = function(cookieName, subName, subValue) {
	var yCookie = YAHOO.Finance.Cookie;
	var days = 3652; // 10 years
	var cookieValue = yCookie.get(cookieName);
        var newValue = "";
        var nvArray = [];
        var nvPair = [];
        var found = false;
        if (cookieValue) {
                nvArray = cookieValue.split('&');
        }
        for (var i = 0; i < nvArray.length ; i++) {
                nvPair = nvArray[i].split('=');
                if (nvPair.length > 1) {
                        if (nvPair[0] === subName) {
                                nvPair[1] = subValue;
                                found = true;
                        }
                }
                nvArray[i] = nvPair.join('=');
        }
        if (!found) {
                nvArray[nvArray.length] = subName + '=' + subValue;
        }
        newValue = nvArray.join('&');
        yCookie.set(cookieName, newValue, days, "", "/");
};


// Submitting ticker panel
var tickerPanelSubmit=function(event) {
	var yDom = YAHOO.util.Dom;

	// cookie
        var ttCookie = "TT"; // User preferences for stock ticker
        var yfiCookie = "PRF"; // Get recent quotes tickers

	// initialize cookie and restore settings
	var setUserPreferences = function() {
	    var yDom = YAHOO.util.Dom;
	    var ttCookie = "TT";
	    var yCookie = YAHOO.Finance.Cookie;
	    var userPreferences = yDom.get("yfi_user_preferences").value;
	    var userSignedIn = yDom.get("yfi_user_signed_in").value;
	    var saveUserSettings;

	    // Get speed/scroll/display/color/change/%change settings from user preferences

	    // console.log(userSignedIn);
	    // console.log(saveUserSettings);

	    if ((getSubCookie(ttCookie, "savettsettings")) === "1") {saveUserSettings = 1;}
                else {saveUserSettings = 0;}

            var scrollValue = getIsPaused();
            var displayValue = getSelectValue();
            var speedValue = getScrollingSpeed();
            // var bgColorValue = getTickerColor();
            var changeValue = getTickerChange();
 
	    // console.log(scrollValue);
	    // console.log(displayValue);
	    // console.log(speedValue);

            // Save values in user cookie
	    setSubCookie(ttCookie,"tt_scroll", scrollValue);
	    setSubCookie(ttCookie,"tt_display", displayValue);
	    setSubCookie(ttCookie,"tt_speed", speedValue);
	    // setSubCookie(ttCookie,"tt_color", bgColorValue);
	    setSubCookie(ttCookie,"tt_change", changeValue);
	    setSubCookie(ttCookie,"savettsettings", "1");

	    if(userPreferences === "0" && saveUserSettings == 0) {
		// console.log('User has pref');
	          saveUserSettings = 1;
	    }
	    else if (!yCookie.get(ttCookie)) {
		// console.log('Get cookie');
	        // Fresh cookie creation
	          saveUserSettings = 1;
	    } else {
	        // Update
	        // console.log("updating");
	          saveUserSettings = 1;
	          scrollValue = getSubCookie(ttCookie, "tt_scroll");
	          displayValue = getSubCookie(ttCookie, "tt_display");
	          speedValue = getSubCookie(ttCookie, "tt_speed");
	          changeValue = getSubCookie(ttCookie, "tt_change");
	    }
		// console.log("user signed in ="+userSignedIn);
		// console.log("save user settings="+saveUserSettings);

	    if (userSignedIn === "0" && saveUserSettings == 1) {
		setSubCookie(ttCookie,"savettsettings", "2");
	        saveSettingsUDB();
	    } 

	    // Set global variables with user selected values     
	    stockTickerSpeed = speedValue;
            stockTickerScroll = scrollValue;
            stockTickerDisplay = displayValue;
            // stockTickerColor = bgColorValue;
            stockTickerChange = changeValue;
	};

	// Set user preferences
	setUserPreferences();

	// Hide the panel
	tickerPanel.hide();

	// Dont submit page
	YAHOO.util.Event.preventDefault(event);
};

// Load ticker panel
YAHOO.Finance.TickerPanel();

var loadScrollValue;
var loadDisplayValue;
var loadSpeedValue;
var loadChangeValue;

var userSignedIn = yDom.get("yfi_user_signed_in").value;
if (userSignedIn === "0") {
        loadScrollValue = getIsPaused();
        loadDisplayValue = getSelectValue();
        loadSpeedValue = getScrollingSpeed();
        // loadBgColorValue = getTickerColor();
        loadChangeValue = getTickerChange();
} else {
	var ttCookie = "TT";
	loadScrollValue = getSubCookie(ttCookie, "tt_scroll");
	loadDisplayValue = getSubCookie(ttCookie, "tt_display");
	loadSpeedValue = getSubCookie(ttCookie, "tt_speed");
	loadChangeValue = getSubCookie(ttCookie, "tt_change");
}


if(loadSpeedValue == 1) { stockTickerSpeed = TICKER_SPEED_MEDIUM; YAHOO.util.Dom.setAttribute("yfi_ticker_speed2", "checked", true);}
else if (loadSpeedValue == 2) { stockTickerSpeed = TICKER_SPEED_FAST; YAHOO.util.Dom.setAttribute("yfi_ticker_speed3", "checked", true);}
else { stockTickerSpeed = TICKER_SPEED_SLOW; YAHOO.util.Dom.setAttribute("yfi_ticker_speed1", "checked", true); // Get the default speed declared above
}

if(loadScrollValue == 1) { stockTickerScroll = TICKER_SCROLL_OFF; YAHOO.util.Dom.setAttribute("yfi_ticker_pause", "checked", true);}
else { stockTickerScroll = TICKER_SCROLL_ON; YAHOO.util.Dom.setAttribute("yfi_ticker_resume", "checked", true); // Get the default scroll declared above
}

if(loadDisplayValue == 1) { stockTickerDisplay = TICKER_DISPLAY_MARKET_SUMMARY; 
	YAHOO.util.Dom.setAttribute("yfi_ticker_ms", "selected", "selected");}
else { stockTickerDisplay = TICKER_DISPLAY_RECENT_QUOTES; 
       YAHOO.util.Dom.setAttribute("yfi_ticker_rq", "selected", "selected"); // Get the default speed declared above
}

// if(loadBgColorValue == 1) { stockTickerColor = TICKER_COLOR_TEAL;}
// else { stockTickerColor = TICKER_COLOR_GREEN; // Get the default speed declared above
// }

if(loadChangeValue == 0) { stockTickerChange = TICKER_DISPLAY_ABSOLUTE_CHANGE; YAHOO.util.Dom.setAttribute("yfi_ticker_change1", "checked", true);}
else { stockTickerChange = TICKER_DISPLAY_PERCENT_CHANGE; YAHOO.util.Dom.setAttribute("yfi_ticker_change2", "checked", true); // Get the default speed declared above
}

// Animate
window.requestAnimFrame = (function(callback){
  return window.requestAnimationFrame ||
  window.webkitRequestAnimationFrame |
  window.mozRequestAnimationFrame ||
  window.oRequestAnimationFrame ||
  window.msRequestAnimationFrame ||
  function(callback){
    window.setTimeout(callback, 40); // Refresh, repaint ticker every 40 milliseconds
  };
})();

var xoffset = 0; // Keeps track of where the tickers should be displayed in canvas
var iteration = 0; // A counter to keep track of the number of times tape is refreshed
var once = 1; // Track one time initializations
var text = ""; // Text to be displayed inside ticker tape
// var quotesArray = new Array();
var ltArray = new Array(); // Last Trade 
var absArray = new Array(); // Absolute Change
var pcArray = new Array(); // percent Change

// Fill a rounded rectangle in the HTML 5 canvas
function fillRoundRect(context,x,y,w,h,r) {
    // Draw the cuved rectangle
    context.beginPath();

    // Draw top line
    context.moveTo(x+r, y);
    context.lineTo(x+w-r, y);
    // Draw top right corner
    context.arcTo(x+w, y, x+w, y+r, r);
    // Draw right line
    context.lineTo(x+w, y+h-r);
    // Draw bottom right corner
    context.arcTo(x+w, y+h, x+w-r, y+h, r);
    // Draw bottom line
    context.lineTo(x+r, y+h);
    // Draw bottom left corner
    context.arcTo(x, y+h, x, y+h-r, r);
    // Draw left line
    context.lineTo(x, y+r);
    // Draw top left corner
    context.arcTo(x, y, x+r, y, r);

    context.closePath();
    context.fill();
}

// Stock ticker
YAHOO.Finance.Ticker=function(){

   var yDom = YAHOO.util.Dom;
   var yEvent = YAHOO.util.Event;

   var tickerEl = yDom.get("yfi_stock_ticker");

   var getRecentQuotes = function() {
        var prfObj = YAHOO.Finance.Cookie.getObj('PRF');
        var tValue = "";
        var tmpArray = [];
        tArray = [];
        var i, j;
	// Display recent quotes
        if (prfObj && (stockTickerDisplay == TICKER_DISPLAY_RECENT_QUOTES)) {
                tValue = prfObj.t;
                if (tValue) {
                        tmpArray = tValue.split('+');
                }
        }
	tmpArray.sort();
        for (i=0; i<tmpArray.length; i++) {
                if ((i==0) || (tmpArray[i-1] != tmpArray[i])) {
                        tArray.push(tmpArray[i]);
                }
        }

        // add market summary indices
        marketSumIndex = tArray.length;
//        if(tArray.length <= 4) {
        if(!YAHOO.Finance.TickerTapeConfig)
            return;

        var mstickers = YAHOO.Finance.TickerTapeConfig.config[0].mstickers;
        var mstickersdn = YAHOO.Finance.TickerTapeConfig.config[0].mstickersdn;

        var mstickersArr = mstickers.split(',');
        var mstickersdnArr = mstickersdn.split(',');

        for (i=0; i<mstickersArr.length; i++) {
            var dupTicker = false;

            for (j=0; j<tArray.length; j++) {
                if (tArray[j] == mstickersArr[i].toUpperCase()) {
                    dupTicker = true;
                }
            }
            if (!dupTicker) {
                tArray.push(mstickersArr[i].toUpperCase());
                marketSumDn[mstickersArr[i].toUpperCase()] = mstickersdnArr[i].replace(/\'/g,'');
            }
        }

	// console.log("tArray = " + tArray.join(',') );

	// Empty initialization/it was undefined (need to revisit)
        if (once) {
            for (i=0; i<tArray.length; i++) {
		// console.log("Setting ltArray[" + tArray[i] + "] to \"\"");
                // quotesArray[tArray[i]] = "";
  		ltArray[tArray[i]] = "";
  		absArray[tArray[i]] = "";
  		pcArray[tArray[i]] = "";  
            }
        }
  };

  // returns formatted ticker list in CSV style as required for dynamic update via streaming
  var formatData = function(data) {
      	var lastTradeRTQ;
       	var absChangeRTQ;
       	var pctChangeRTQ;
      	var lastTrade;
     	var absChange;
       	var pctChange;
       	for (var symbol in data) {
               	// last trade
                lastTradeRTQ = data[symbol]["l84"];
                lastTradeAfterHrRTQ = data[symbol]["l86"];
                lastTrade = data[symbol]["l10"];
		
		// absolute change
             	absChangeRTQ = data[symbol]["c63"];
                absChangeAfterHrRTQ = data[symbol]["c85"];
               	absChange = data[symbol]["c10"];

                // percent change
                pctChangeRTQ = data[symbol]["p43"];
                pctChangeAfterHrRTQ = data[symbol]["c86"];
                pctChange = data[symbol]["p20"];

		// Fill RTQ and legacy values in respective array
                if (lastTradeAfterHrRTQ && absChangeAfterHrRTQ && pctChangeAfterHrRTQ) {
                       	// quotesArray[symbol] = '"' + lastTradeAfterHrRTQ + ', ' + pctChangeAfterHrRTQ + '%"';
                        if (lastTradeAfterHrRTQ != undefined && lastTradeAfterHrRTQ != "") {
  			    ltArray[symbol] = lastTradeAfterHrRTQ;
                        }
                        if (absChangeAfterHrRTQ != undefined) {
                            absArray[symbol] = absChangeAfterHrRTQ;
                        }
                        if (pctChangeAfterHrRTQ != undefined) {
                            pcArray[symbol] = pctChangeAfterHrRTQ + "%";
                        }
              	}
		else if (lastTradeRTQ && absChangeRTQ && pctChangeRTQ) {
                       	// quotesArray[symbol] = '"' + lastTradeRTQ + ', ' + absChangeRTQ + ', ' + pctChangeRTQ + '%"';
                        if (lastTradeRTQ != undefined && lastTradeRTQ != "") {
  			    ltArray[symbol] = lastTradeRTQ;
                        }
                        if (absChangeRTQ != undefined) {
  			    absArray[symbol] = absChangeRTQ;
                        }
                        if (pctChangeRTQ != undefined) {
  			    pcArray[symbol] = pctChangeRTQ + "%";
                        }
              	}
                else if (lastTrade && absChange && pctChange) {
                       	// quotesArray[symbol] = '"' + lastTrade + ', ' + pctChange + '%"';
                        if (lastTrade != undefined && lastTrade != "") {
  			    ltArray[symbol] = lastTrade;
                        }
                        if (absChange != undefined) {
                            absArray[symbol] = absChange;
                        }
                        if (pctChange != undefined) {
                            pcArray[symbol] = pctChange + "%";
                        }
              	} else  {
			if (absChangeRTQ == undefined && absArray[symbol] == undefined) {
                            absChangeRTQ = "0.00";
	                }
			if (pctChangeRTQ == undefined && pcArray[symbol] == undefined) {
			    pctChangeRTQ = "0.00";
			}
                       	// quotesArray[symbol] = '"' + lastTradeRTQ + ', ' + absChangeRTQ + ', ' + pctChangeRTQ + '%"';
                        if (lastTradeRTQ != undefined && lastTradeRTQ != "") {
  			    ltArray[symbol] = lastTradeRTQ;
                        }
                        if (absChangeRTQ != undefined) {
  			    absArray[symbol] = absChangeRTQ;
                        }
                        if (pctChangeRTQ != undefined) {
  			    pcArray[symbol] = pctChangeRTQ + "%";
                        }
		}
      	}
  };
  
  // returns ticker name 
  var getTickerName = function(sym) {
	if (sym == undefined) {
            return sym;
        }

	if (marketSumDn[sym.toUpperCase()] == undefined) {
     		return sym;
	}
    
	return marketSumDn[sym.toUpperCase()];
  };

  // A polling method to check whether streaming is on or off
  if ((iteration % 50) == 0) {
    var yfiCookie = "PRF"; // Get recent quotes tickers
    var sq_cookie_val = YFS.util.cookieMgr.existsInCookie("PRF", "sq=0");
    // console.log("sq_cookie_val = " + sq_cookie_val);
    if (sq_cookie_val) {
	hideTT();
	enableTTSettings(0);
    } else {
        checkAndShowTT();
	enableTTSettings(1);
    }
  }

  if ((iteration % 250) == 0) {
    iteration = 0;
  }
  iteration++;

  // Check if ticker tape is to be displayed
  if (ttDisplayed) {

          if (((iteration % 250) == 0) && (!ttStreamStarted)) {
              var yfiStreaming = YAHOO.Finance.Streaming.vcr;
              if(yfiStreaming.isStreaming()) {
                   	yfiStreaming.shutdownStreaming();
                      	yfiStreaming.startStreaming();
              }
     	  }

	  // Fill ticker array for rendering
	  if ((tArray.length == 0) || ((iteration % 50) == 0)) {
	    getRecentQuotes();
	  }

	  // Get HTML5 canvas object and its 2d context
	  var canvas = document.getElementById("stock_ticker");
	  var context= canvas.getContext("2d");

	  // Erase the previous canvas content
	  context.clearRect(0,0,canvas.width,canvas.height);

	  // Where to display text inside the canvas
	  // var yoffset = (canvas.height - metrics.height)/2;
	  // Margin from top
	  var yoffset = 12;

	  // Define text properties
	  context.font = "bold 10pt sans-serif";
	  // Place content in the top position in canvas 
	  context.textBaseline = "middle";

	  var WHITE_COLOR = "#FFFFFF";
	  var GREEN_COLOR = "#009900";
	  var RED_COLOR   = "#D82025";

	  // Default server message if streaming is not started
	  if(!ttStreamStarted) {
                  var prevAlign = context.textAlign;
                  var x = canvas.width / 2;
		  loadingText = "Loading ...";
                  context.fillStyle = WHITE_COLOR;
		  context.font = "bold 9pt sans-serif";
                  context.textAlign = "center";
                  context.fillText(loadingText, x, yoffset);
                  context.textAlign = prevAlign;
          }

	  // Now display the text
	  // Positioning text in the left
	  var x = xoffset;
	  var tickerwidth = 0;
	  var symStartIndex = firstTickerIndex;

	  tickerX = [];
	  tickerSymIndex = [];

	  // Repeat the tape
	  var repeat;
	  // Repeat minimum of 10, width of the ticker tape
	  for (repeat=0; repeat<10; repeat++) {
            var numTickersDisplayed = 0;

	    // Break if we are going beyond canvas width
	    if (x > canvas.width) {
	      break;
	    }

	    // sym is an index into ticker symbol array
	    for (var sym=0; sym<symStartIndex; sym++) {
	      text = getTickerName(tArray[sym]);
	      if ((text == undefined)
		  || (ltArray[tArray[sym]] == undefined) || (ltArray[tArray[sym]] === "")) {
                continue;
              }
              numTickersDisplayed++;
            }

	    for (var sym=symStartIndex; sym<tArray.length; sym++) {
	      // Display symbol
	      text = getTickerName(tArray[sym]);

	      if ((text == undefined)
		  || (ltArray[tArray[sym]] == undefined) || (ltArray[tArray[sym]] === "")
	//          || (absArray[tArray[sym]] == undefined) || (absArray[tArray[sym]] === "")
	//          || (pcArray[tArray[sym]] == undefined) || (pcArray[tArray[sym]] === "")
		 )
	      {
                if ( (sym == symStartIndex) && (symStartIndex == firstTickerIndex) ) {
		  firstTickerIndex = (firstTickerIndex + 1) % tArray.length;
                  // console.log("1: firstTickerIndex = " + firstTickerIndex + ", xoffset = " + xoffset + ", tickerwidth = " + tickerwidth);
                }
		continue;
	      }

	      // Define width of the text to be displayed
	      var metrics = context.measureText(text);
	      var textwidth = metrics.width;

	      // Display text in white color
	      if (textwidth > 0) {
                numTickersDisplayed++;

                if (numTickersDisplayed > 10) {
                  break;
                }

		context.fillStyle = WHITE_COLOR;
		context.fillText(text, x, yoffset, textwidth);

		// Save the x-offset of the ticker
		var xIndex = tickerX.length;
		tickerX[xIndex] = x;
		tickerSymIndex[xIndex] = sym;

		 // For debugging ticker offsets
		// context.strokeStyle = "#FFaa00";
		// context.moveTo(x,0);
		// context.lineTo(x,canvas.height);
		// context.stroke();

		// Intra-ticker spacing
		x = x + textwidth + 10;
	      } else {
		continue;
	      }
              
	      if (x > canvas.width) {
		break;
	      }

	      // Display last trade value
	      text = ltArray[tArray[sym]];

	      if (text == undefined) {
		x = x + 30;
		if (tickerwidth == 0) {
		  tickerwidth = x - xoffset;
		}
		continue;
	      }

	      // Define width of the text to be displayed
	      metrics = context.measureText(text);
	      textwidth = metrics.width;
		
	      // Display text in white color
	      if (textwidth > 0) {
		context.fillStyle = WHITE_COLOR;
		context.fillText(text, x, yoffset, textwidth);
		// Intra-ticker spacing
		x = x + textwidth + 10;
	      }

	      if (x > canvas.width) {
		break;
	      }

	      // Display absolute or percent change
	      if (stockTickerChange == TICKER_DISPLAY_ABSOLUTE_CHANGE) {
		text = absArray[tArray[sym]];
	      } else {
		text = pcArray[tArray[sym]];
	      }

	      if (text == undefined) {
		x = x + 30;
		if (tickerwidth == 0) {
		  tickerwidth = x - xoffset;
		}
		continue;
	      }

	      if (text == "0.00") {
		text = "+" + text;
	      }

	      // Define height and width of the text to be displayed
	      metrics = context.measureText(text);
	      textwidth = metrics.width;

	      // Choose background color for change/%change
	      if (text.indexOf("-") == -1) {
		context.fillStyle = GREEN_COLOR;
	      } else {
		context.fillStyle = RED_COLOR;
	      }

	      if (textwidth > 0) {
		// Set the background
		fillRoundRect(context, x, 3, textwidth + 10, 16, 2); // 16 is height of rect
		// Display text in white color
		context.fillStyle = WHITE_COLOR;
		context.fillText(text, x + 5, yoffset, textwidth);
		x = x + textwidth + 20;
	      }

	      if (x > canvas.width) {
		break;
	      }

	      // Additional inter-ticker spacing
	      x = x + 30;
	      if (tickerwidth == 0) {
		tickerwidth = x - xoffset;
	      }
	    }
	    symStartIndex = 0;
	  }

	  // If the text scrolls out of the left side of the canvas, start it again from the right
	  if ((xoffset + tickerwidth) <= 0) {
		if (firstTickerIndex < 10) {
		        xoffset = xoffset + tickerwidth;
                }
		firstTickerIndex = (firstTickerIndex + 1) % tArray.length;
                // console.log("2: firstTickerIndex = " + firstTickerIndex + ", xoffset = " + xoffset + ", tickerwidth = " + tickerwidth);
	  }
	  if (stockTickerScroll == TICKER_SCROLL_OFF) {
		// xoffset = 0 + (canvas.width - x + xoffset) / 2;
		xoffset = 0;
	  } else if (stockTickerSpeed == TICKER_SPEED_SLOW) {
		xoffset = xoffset - 1;
	  } else if (stockTickerSpeed == TICKER_SPEED_MEDIUM) {
		xoffset = xoffset - 2;
	  } else {
		xoffset = xoffset - 3; // every 40 millisec 4 px to the left
	  }

  }

  // Schedule animation
  requestAnimFrame(function(){
     YAHOO.Finance.Ticker();
  });

  // Define callback to receive stream data
  // Streaming Quotes Callback :: fired when ticker data is updated
  // @param {Object} ticker JSON data

   // Set the stream; refresh it every 1000 milli-seconds
   var yfiStreaming = YAHOO.Finance.Streaming.vcr;

   var streamingTickerCallback = function(data) {
        // console.log("streamingTickerCallback");
        if (!ttStreamStarted) {
                ttStreamStarted = true;
                if(yfiStreaming.isStreaming()) {
                        yfiStreaming.shutdownStreaming();
                        yfiStreaming.startStreaming();
                }
        }
        formatData(data);
   }

   if (once) {
       // console.log("once=1; addStreamigDataListener");
       setTimeout(function(){
      		yfiStreaming.addStreamingDataListener(function(data){ streamingTickerCallback(data); });
       }, 1000);
       once = 0;
   } 
}

var ua = YAHOO.env.ua;
  
if ((/webkit\W(?!.*chrome).*safari\W/i).test(navigator.userAgent)) {
    ua.safari = 1;
    var appleDevicePattern = new RegExp("(iPad|iPhone|iPod)");
    if ( navigator.userAgent.match( appleDevicePattern ) ) {
      ua.safari = 0;
    }
}

// Check if streaming is enabled before loading ticker panel
if ((ua.gecko > 0) || (ua.ie >= 9) || (ua.safari > 0)) {
	var yDom = YAHOO.util.Dom;
  var streaming_setting = yDom.get("ustreaming").value;
	var userSignedIn = yDom.get("yfi_user_signed_in").value;
	if(userSignedIn == 1) {streaming_setting = 1};
	if (streaming_setting === "0") {
		// Dont show tape
    var yfiCookie = "PRF"; // Get recent quotes tickers
    setSubCookie(yfiCookie, "sq", 0);
    hideTT();
		YAHOO.Finance.Ticker();
	} else {
		checkAndShowTT();
		// First time calling ticker
		YAHOO.Finance.Ticker();
		// Hack for view level ULT
    var sec = "tt-view";
    var pg_ssk = YAHOO.util.Dom.get("spaceid");
    var ttUltViewObj = {
       "sec": sec
    };
    if (pg_ssk) {
       ttUltViewObj[YAHOO.ULT.SRC_SPACEID_KEY] = pg_ssk.innerHTML;
    }

    YAHOO.ULT.beacon_click(ttUltViewObj)
	}
}

/*yui2.8 is not setting ua.chrome*/
if( /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor) ){
  ua.chrome=1;
}

//hack for chrome streaming
if( ua.chrome > 0  && document.getElementById('yfs_enable_chrome') == null ){
  ua.chrome = 0;
}

// Show settings icon only in streaming enabled browsers
if ((ua.gecko > 0) || (ua.ie > 0) || (ua.safari > 0) || ( ua.chrome > 0 ) ) {
	document.getElementById('yfi_pg_settings_icon').style.display = "block";
  
  /**FIXME HACK: disable TT for Chrome: this require for displaying panel**/
  if( ua.chrome > 0 ){
    document.getElementById('ticker_onoff').style.display = "block";
    document.getElementById('ticker_onoff').style.visibility = "hidden";
    document.getElementById('ticker_onoff').style.marginTop = "24px";
  }

	if ((ua.gecko > 0) || (ua.ie >= 9) || (ua.safari > 0)) {
		document.getElementById('ticker_onoff').style.display = "block";
		// Load Toggle Settings
		initToggle();
	}
}

