function getCSRFToken() {
    const csrfToken = document.cookie.split(';')
      .find(cookie => cookie.trim().startsWith('csrftoken='))
      ?.split('=')[1];
    return csrfToken;
  }
  
  document.getElementById("submit-btn").addEventListener("click", function() {
    // Get the CSRF token from the cookie
    const csrfToken = getCSRFToken();
    
    if (!csrfToken) {
      alert("CSRF token not found!");
      return;
    }
  
    // Get the story content from the TinyMCE editor
    const storyTitle = document.getElementById("storyTitle").value;  // Assuming you have an input field for the title
    const storyContent = tinymce.get('storyEditor').getContent();  // Get the content from the TinyMCE editor
  
    if (!storyTitle || !storyContent) {
      alert("Please fill in both the title and the content!");
      return;
    }
  
    // Prepare the data to send in the request
    const data = {
      storyTitle: storyTitle,
      content: storyContent
    };
  
    // Send the POST request to submit the story
    fetch("/story/editor/", {
      method: "POST",
      credentials: "same-origin",  // Ensures cookies are sent with the request
      headers: {
        "Content-Type": "application/json",  // Specify that we are sending JSON
        "X-CSRFToken": csrfToken,  // Include the CSRF token in the request header
      },
      body: JSON.stringify(data)  // Send the story data as JSON
    })
    .then(response => {
      if (response.ok) {
        // Success: Handle response (e.g., show a success message or redirect)
        alert("Story submitted successfully!");
        window.location.href = '/stories';  // Redirect to the page where the stories are displayed
      } else {
        // If response is not OK (e.g., server error, validation issue), show an alert
        alert("Failed to submit the story.");
      }
    })
    .catch(error => {
      console.error("Error:", error);
      alert("An error occurred while submitting the story.");
    });
  });
  