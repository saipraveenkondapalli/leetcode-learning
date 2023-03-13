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

    // get body element and Insert the banner before the navigation bar
    const body = document.body
    body.insertBefore(banner, body.firstChild);
}


// Get the problem name from the URL and call the showLoading function to display the banner
const problemName = window.location.pathname.split("/")[2];
showLoading();


// setTimeout is used to wait for the banner to be displayed and giving sufficient time to execute native JS code of the Leetcode website

setTimeout(function() {
    fetch(`https://www.leetcodeproblems.tech/api/problems/${problemName}`)
        .then(response => response.text())
        .then(data => {

            // convert the response to json
            data = JSON.parse(data);

            // get element by xpath to the Description div of the problem
            const xpath = "/html/body/div[2]/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div[3]/div"
            let problemDescription = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

            // using classes from the Leetcode website to display the data

            let spanSuccess = 'bg-olive dark:bg-dark-olive text-olive dark:text-dark-olive inline-block rounded-[21px] bg-opacity-[.15] px-2.5 py-1 text-xs font-medium capitalize dark:bg-opacity-[.15]';
            let spanDanger = 'bg-pink dark:bg-dark-pink text-pink dark:text-dark-pink inline-block rounded-[21px] bg-opacity-[.15] px-2.5 py-1 text-xs font-medium capitalize dark:bg-opacity-[.15]\"';
            let spanInfo = 'inline-flex items-center whitespace-nowrap text-xs rounded-full bg-blue-0 dark:bg-dark-blue-0 text-blue-s dark:text-dark-blue-s px-3 py-1 font-medium leading-4';

            // get message from json data and if message equals to "Problems found"
            const message = data["message"];

            let para;
            if (message === "Problem found") {
                let para = document.createElement("p");
                para.innerHTML = `<span class="${spanInfo}" style="margin: 5px;">Company Name : Frequency : Percentage appearance based on total questions by company</span><br>`;
                // use for loop on data['problem']['company']
                for (let i = 0; i < data['problem']['company'].length; i++) {

                    const name = data['problem']['company'][i]['name'];
                    const frequency = data['problem']['company'][i]['freq'];
                    let percentage = data['problem']['company'][i]['percentage']

                    if (percentage) {
                        percentage = percentage.toString().split(".");
                        if (percentage.length > 1) {
                            percentage = percentage[0] + "%";
                        } else {
                            // check up to the last character in percentage[0]
                            if (percentage[0][percentage[0].length - 1] === ";") {
                                percentage = percentage[0].slice(0, -1);
                            }
                        }
                        // if percentage == 0%
                        if (percentage === "0%") {
                            percentage = undefined;
                        }
                    }

                    // if both frequency and percentage are present
                    if (frequency && percentage) {
                        para.innerHTML += `<a href="https://www.leetcodeproblems.tech/company/${name}" target="_blank"><span class = "${spanSuccess}" style="margin: 3px">${name} (${frequency}) (${percentage})</span></a>`;
                    }
                    // if only frequency is present
                    else if (frequency) {
                        para.innerHTML += `<a href="https://www.leetcodeproblems.tech/company/${name}" target="_blank"><span class = "${spanSuccess}" style="margin: 3px">${name} (${frequency})</span></a>`;
                    }
                    // if only percentage is present
                    else if (percentage) {
                        para.innerHTML += `<a href="https://www.leetcodeproblems.tech/company/${name}" target="_blank"><span class = "${spanSuccess}" style="margin: 3px">${name} (${percentage})</span></a>`;
                    }
                    // if none of them are present
                    else {
                        para.innerHTML += `<a href="https://www.leetcodeproblems.tech/company/${name}" target="_blank"><span class = "${spanSuccess}" style="margin: 3px">${name}</span></a>`;
                    }
                }

                problemDescription.innerHTML = para.innerHTML + problemDescription.innerHTML;

            } else {
                let para = document.createElement("p");
                para.innerHTML = `<span class="${spanDanger}">No company found</span>`;
                problemDescription.innerHTML = para.innerHTML + problemDescription.innerHTML;
            }
            // hide the loading image
            document.getElementById("loading-banner").remove();

        });
}, 1000);

