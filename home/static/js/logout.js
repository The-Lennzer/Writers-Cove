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

  
  fetch("/auth/logout/", {
    method: "POST",
    credentials: "same-origin",  //cookie-set
    headers: {
      "X-CSRFToken": csrfToken,  
    }
  })
  .then(response => {
    if (response.redirected) {
      console.log(response.status);
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
