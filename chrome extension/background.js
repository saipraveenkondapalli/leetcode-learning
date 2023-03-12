


chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.type === "showLoading") {
    chrome.browserAction.setPopup({ popup: "popup.html" });
  } else if (request.type === "hideLoading") {
    chrome.browserAction.setPopup({ popup: "" });
  }
});
