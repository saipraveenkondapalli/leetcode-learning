// Get the problem name from the URL
const problemName = window.location.pathname.split("/")[2]
//alert(problemName);
// Make a request to the Flask API
fetch(`https://www.leetcodeproblems.tech/api/problems/${problemName}`)
  .then(response => response.text())
  .then(data => {
    // Insert the data into the page
      //convert the response to json
        data = JSON.parse(data);
        console.log(data);
        // get description element from the page with class = _1l1MA
        problemDescription = document.getElementsByClassName("_1l1MA")[0];
        // get message from json and if message equals to "Problems found"
      message = data["message"];
        if(message == "Problem found"){
            alert(data['problem']['total_companies']);

        }

    //problemDescription.innerHTML += data;
  });
