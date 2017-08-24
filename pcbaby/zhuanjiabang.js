var webPage = require('webpage');

var page = webPage.create();
page.settings.userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36';

page.open('http://kuaiwen.pcbaby.com.cn/zhuanjiabang/', function(status) {
	if (status !== 'success') {
		phantom.exit();
	}

  	// Do other things here...
  	var links = [];
  	var items = document.getElementsByClassName("aList-title");
  	for (var i=0; i<items.length; i++) {
  		console.log(items[i]);
  		links.push(items[i].children[1].href);
  	}

  	phantom.exit();
});
