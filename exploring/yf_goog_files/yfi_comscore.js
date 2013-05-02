if(typeof(YAHOO.Finance) == "undefined" || typeof(YAHOO.Finance.Comscore) == "undefined") {
    // Comscore
    YAHOO.namespace("YAHOO.Finance.Comscore");
}

if(YAHOO.Finance.ComscoreConfig) {

    var spaceid = YAHOO.Finance.ComscoreConfig.config[0].c5;
    var currUrl = YAHOO.Finance.ComscoreConfig.config[0].c7;

    <!-- Begin comScore Tag -->
    var _comscore = _comscore || [];
    _comscore.push({
       c1: "2",
       c2: "7241469",
       c5: spaceid,
       c7: currUrl
    });

    (function() {
       var s = document.createElement("script"), el = document.getElementsByTagName("script")[0]; s.async = true;
       s.src = (document.location.protocol == "https:" ? "https://s.yimg.com/lq" : "http://l.yimg.com/d") + "/lib/3pm/cs_0.2.js";
       el.parentNode.insertBefore(s, el);
    })();
}

