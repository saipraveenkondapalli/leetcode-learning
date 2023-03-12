function showLoading() {
  // Create the banner element
  const banner = document.createElement("div");
  banner.setAttribute("id", "loading-banner");
  banner.style.backgroundColor = "#337ab7";
  banner.style.color = "white";
  banner.style.padding = "10px";
  banner.style.textAlign = "center";
  banner.style.fontWeight = "bold";
  banner.innerHTML = "Loading LeetCode insights from LeetCode Extension...";

  // Find the navigation bar element
  // get body element
    const body =  document.body


  // Insert the banner before the navigation bar
  body.insertBefore(banner, body.firstChild);
}




// Get the problem name from the URL

const problemName = window.location.pathname.split("/")[2]
// Add  a banner to show that the extension is loading
 showLoading();

setTimeout(function() {
    fetch(`https://www.leetcodeproblems.tech/api/problems/${problemName}`)
        .then(response => response.text())
        .then(data => {
            data = JSON.parse(data);
            // get element by xpath
            xpath = "/html/body/div[2]/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div[3]/div"
            problemDescription = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            spanSuccess = 'bg-olive dark:bg-dark-olive text-olive dark:text-dark-olive inline-block rounded-[21px] bg-opacity-[.15] px-2.5 py-1 text-xs font-medium capitalize dark:bg-opacity-[.15]'
            spanDanger = "bg-pink dark:bg-dark-pink text-pink dark:text-dark-pink inline-block rounded-[21px] bg-opacity-[.15] px-2.5 py-1 text-xs font-medium capitalize dark:bg-opacity-[.15]\" style=\"margin:3px"
            // get message from json and if message equals to "Problems found"
            message = data["message"];
            if (message == "Problem found") {
                p = document.createElement("p");
                // use for loop on data['problem']['company']
                for (var i = 0; i < data['problem']['company'].length; i++) {
                    name = data['problem']['company'][i]['name'];
                    frequency = data['problem']['company'][i]['freq'];
                    p.innerHTML += `<a href="https://www.leetcodeproblems.tech/company/${name}" target="_blank"><span class = "${spanSuccess}" style="margin: 3px">${name} (${frequency})</span></a>`;
                }

                problemDescription.innerHTML = p.innerHTML + problemDescription.innerHTML;

            }
            else{
                p = document.createElement("p");
                p.innerHTML = `<span class="${spanDanger}">No company found</span>`;
                problemDescription.innerHTML = p.innerHTML + problemDescription.innerHTML;
            }
            // hide the loading image
             document.getElementById("loading-banner").remove();

        });
}, 1000);
