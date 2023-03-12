// Get the problem name from the URL
const problemName = window.location.pathname.split("/")[2]
alert(problemName);
// Make a request to the Flask API
fetch(`https://www.leetcodeproblems.tech/api/problems/${problemName}`)
  .then(response => response.text())
  .then(data => {
    // Insert the data into the page
      //convert the response to json
        data = JSON.parse(data);
        console.log(data);

    //problemDescription.innerHTML += data;
  });
