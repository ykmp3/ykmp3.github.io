    function createXMLHttpRequest() {  
        var xmlHttp;  
        if (window.XMLHttpRequest) {  
            xmlHttp = new XMLHttpRequest();  
            if (xmlHttp.overrideMimeType)  
                xmlHttp.overrideMimeType('text/xml');  
        } else if (window.ActiveXObject) {  
            try {  
                xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");  
            } catch (e) {  
                try {  
                    xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");  
                } catch (e) {  
                }  
            }  
        }  
        return xmlHttp;  
    }  

function recv_callback()
{
if (xmlHttp.readyState==4)
  {// 4 = "loaded"
  if (xmlHttp.status==200)
    {// 200 = "OK"
    console.log(xmlHttp);
    console.log(xmlHttp.reponseText);
    }
  else
    {
    console.log(xmlHttp);
    alert("Problem retrieving XML data:" + xmlHttp.statusText);
    }
  }
}
function clickConvert(){
	var url = document.getElementById('input').value;
	var videoId = url.match('id_(.*==)')[1];
	var mmu = (new Date()).getTime();
    var client_ts = (mmu - mmu%100)/100;
	var ups_url = "https://ups.youku.com/ups/get.json?vid="+videoId+"&ccode=0401&client_ip=192.168.1.1&utid=rjVrETO4v0oCAXVJkKWLTkoS&client_ts="+client_ts;
	console.log(ups_url);
	var request = require('request');

	var options = {
    	url: 'https://api.github.com/repos/mikeal/request',
    	headers: {
        	'User-Agent': 'request'
    	}
	};

	function callback(error, response, body) {
    	if (!error && response.statusCode == 200) {
        	var info = JSON.parse(body);
        	console.log(info.stargazers_count + " Stars");
        	console.log(info.forks_count + " Forks");
    	}
	}
	request(options, callback); 
}
