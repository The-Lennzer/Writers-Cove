function getCSRFToken() {
    const csrfToken = document.cookie.split(';')
      .find(cookie => cookie.trim().startsWith('csrftoken='))
      ?.split('=')[1];
    return csrfToken;
  }
  
  document.getElementById("submit-btn").addEventListener("click", function() {
    const csrfToken = getCSRFToken();
    
    if (!csrfToken) {
      alert("CSRF token not found!");
      return;
    }
  
  
    const storyTitle = document.getElementById("storyTitle").value; 
    const storyContent = tinymce.get('storyEditor').getContent(); 
  
    if (!storyTitle || !storyContent) {
      alert("Please fill in both the title and the content!");
      return;
    }
  
    
    const data = {
      storyTitle: storyTitle,
      content: storyContent
    };
  
    
    fetch("/story/editor/", {
      method: "POST",
      credentials: "same-origin", 
      headers: {
        "Content-Type": "application/json",  
        "X-CSRFToken": csrfToken,  
      },
      body: JSON.stringify(data)  
    })
    .then(response => {
      if (response.ok) {
        alert("Story submitted successfully!");
        window.location.href = '/stories';  
      } else {
       
        alert("Failed to submit the story.");
      }
    })
    .catch(error => {
      console.error("Error:", error);
      alert("An error occurred while submitting the story.");
    });
  });
  