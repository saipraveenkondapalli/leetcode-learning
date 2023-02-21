
var query = document.getElementById('query');

document.getElementById('query').addEventListener('input', function(event) {
    if (query.value.length === 0) {
        //window.location.href = '/problems';
        sendRequest();
    }
});


document.getElementById('search-button').addEventListener('click', function() {
  event.preventDefault();
  //alert('You searched for: ' + document.getElementById('query').value);

  var query = document.getElementById('query').value;
  if (query.length < 3) {
    return
  }

  document.getElementById('filter').innerHTML = '<img src="https://gifimage.net/wp-content/uploads/2017/09/blue-loading-gif-transparent-6.gif" style="display: block; margin-top: 60px; margin-bottom:100px; margin-left: auto; margin-right: auto; height: 25px; width: 25px;">';
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/search?search=' + query);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    if (xhr.status === 200) {
      // Success: parse the JSON response and display the results
      document.getElementById('filter').innerHTML = xhr.responseText;
    } else {
      // Error: display an error message
      console.error('Error: ' + xhr.status);
    }
  };
  xhr.send();
});

/*function displayResults(results) {
  // Clear the existing results
  document.getElementById('results').innerHTML = '';
  // Iterate through the results and display them
  for (var i = 0; i < results.length; i++) {
    var result = results[i];
    var name = result.name;
    // Create a new list item for the result
    var li = document.createElement('li');
    li.textContent = name;
    // Add the result to the list
    document.getElementById('results').appendChild(li);
  }
} */

    // Get the "previous" and "next" buttons
var prevButton = document.querySelector('.page-item .page-link[aria-label="Previous"]');
var nextButton = document.querySelector('.page-item .page-link[aria-label="Next"]');

// Get the page number element
var pageNumber = document.querySelector('#page-number');

// Listen for clicks on the "previous" button
prevButton.addEventListener('click', function(event) {
  event.preventDefault();

  // Decrement the page number and update the page number element
  var currentPage = parseInt(pageNumber.textContent);
  pageNumber.textContent = currentPage - 1;
  sendRequest();
});

// Listen for clicks on the "next" button
nextButton.addEventListener('click', function(event) {
  event.preventDefault();

  // Increment the page number and update the page number element
  var currentPage = parseInt(pageNumber.textContent);
  pageNumber.textContent = currentPage + 1;
  sendRequest();
});



    function sendRequest() {
    // replace filter with loading image
    document.getElementById("filter").innerHTML = '<img src="https://gifimage.net/wp-content/uploads/2017/09/blue-loading-gif-transparent-6.gif" style="display: block; margin-top: 60px; margin-bottom:100px; margin-left: auto; margin-right: auto; height: 25px; width: 25px;">';
    // Get the selected level, category, and page number
    var level = levelSelect.value;
    var category = categorySelect.value;
    var page = document.getElementById("page-number").innerText;
    page = parseInt(page);
    // Send an HTTP request to the /filter URL with the selected filters as query parameters
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/filter?level=' + level + '&category=' + category + '&page=' + page);
    xhr.onload = function() {
        if (xhr.status === 200) {
            // If the request was successful, replace the table body with the response
            document.getElementById('filter').innerHTML = xhr.responseText;
            // enable the next link
            document.querySelector('.page-item .page-link[aria-label="Next"]').style.pointerEvents = 'auto';
            window.history.pushState({}, '', '/problems?level=' + level + '&category=' + category + '&page=' + page);

        }
        else {

            //disable the next link and set the page number to 1
            document.getElementById("page-number").innerText = page - 1;
            document.querySelector('.page-item .page-link[aria-label="Next"]').style.pointerEvents = 'none';
        }
    };
    xhr.send();
}


    // Get the form element
    var form = document.querySelector('form');

    // Listen for the submit event on the form


    // Get the select elements
    var levelSelect = document.querySelector('#levelFilter');
    var categorySelect = document.querySelector('#categoryFilter');
    var PageNumber = document.querySelector('#page-number');
    // Listen for the change event on the select elements and set the page number to 1
    levelSelect.addEventListener('input', function(event) {
      PageNumber.innerText = 1;
      sendRequest();
    });
    categorySelect.addEventListener('input', function(event) {
      PageNumber.innerText = 1;
      sendRequest();
    });


    // Get the level and category filters
var levelFilter = document.querySelector('#levelFilter');
var categoryFilter = document.querySelector('#categoryFilter');

// Get the URL parameters
var urlParams = new URLSearchParams(window.location.search);

// Get the level and category parameters from the URL
var level = urlParams.get('level');
var category = urlParams.get('category');

// If the level parameter is present, select the corresponding option in the level filter
if (level) {
  levelFilter.value = level;
  levelFilter.click();
}

// If the category parameter is present, select the corresponding option in the category filter
if (category) {
  categoryFilter.value = category;
  categoryFilter.click();
}
window.onpopstate = function(event) {
    // Get the current URL
    var currentUrl = new URL(window.location.href);
}