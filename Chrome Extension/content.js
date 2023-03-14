

function addScript() {
   script = document.createElement('script');
   script.src = chrome.runtime.getURL('leetcode.js');
   document.body.appendChild(script);
}


addScript();

