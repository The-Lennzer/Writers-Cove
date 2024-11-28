function getCSRFToken() {
  const csrfToken = document.cookie.split(';')
    .find(cookie => cookie.trim().startsWith('csrftoken='))
    ?.split('=')[1];
  return csrfToken;
}

document.getElementById("logoutButton").addEventListener("click", function() {
  // Get the CSRF token from the cookie
  const csrfToken = getCSRFToken();
  
  if (!csrfToken) {
    alert("CSRF token not found!");
    return;
  }

  // Send the POST request to logout
  fetch("/auth/logout/", {
    method: "POST",
    credentials: "same-origin",  // Ensures cookies are sent with the request
    headers: {
      "X-CSRFToken": csrfToken,  // Include the CSRF token in the request header
    }
  })
  .then(response => {
    if (response.redirected) {
      console.log(response.status);
      // Redirect to login page after successful logout
      window.location.href = response.url;
    } else {
      alert("Failed to log out");
    }
  })
  .catch(error => {
    console.error("Error:", error);
    alert("An error occurred while logging out.");
  });
});
