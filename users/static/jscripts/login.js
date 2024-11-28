// document.addEventListener("DOMContentLoaded", () => {
//     const loginForm = document.getElementById("loginForm");
//     const errorMessage = document.getElementById("error-message");

//     loginForm.addEventListener("submit", async (event) => {
//         event.preventDefault(); // Prevent form from submitting traditionally

//         const formData = new FormData(loginForm);

//         const payload = {
//             email: formData.get("email"),
//             password: formData.get("password"),
//         };

//         try {
//             const response = await fetch("/api/login/", {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json",
//                     "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
//                 },
//                 body: JSON.stringify(payload),
//             });

//             if (response.ok) {
//                 const data = await response.json();
//                 alert("Login successful!");
//                 localStorage.setItem("authToken", data.token); // Store token in localStorage
//                 window.location.href = "/home/feed"; // Redirect to home page
//             } else {
//                 const errorData = await response.json();
//                 errorMessage.textContent = errorData.error || "Invalid credentials.";
//                 errorMessage.style.display = "block";
//             }
//         } catch (error) {
//             errorMessage.textContent = "An error occurred. Please try again.";
//             errorMessage.style.display = "block";
//         }
//     });
// });
