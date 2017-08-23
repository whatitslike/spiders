var webPage = require('webpage');
var page = webPage.create();

page.open('http://www.baidu.com/', function(status) {
  console.log('Status: ' + status);
  // Do other things here...
  phantom.exit();
});