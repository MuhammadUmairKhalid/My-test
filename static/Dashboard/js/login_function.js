// async function loginUser(event) {
//   event.preventDefault();

//   const email = document.getElementById("email").value;
//   const password = document.getElementById("password").value;
//   console.log(email, password);

//   try {
//     let response = await fetch("http://127.0.0.1:8000/api/loginn/", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({
//         email: email,
//         password: password,
//       }),
//     });

//     let data = await response.json();

//     if (response.status === 200) {
//       alert("✅ Login successful!");
//       console.log("Received token:", data);

//       // Store token in localStorage
//       localStorage.setItem("token", data.token);

//       // Redirect to dashboard
//       window.location.href = "dashboard.html";
//     } else {
//       alert("❌ Login failed: " + (data.message || "Invalid credentials"));
//     }
//   } catch (error) {
//     console.error("Error during login:", error);
//     alert("⚠️ Something went wrong, please try again.",error);
//   }
// }

// login.js
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("loginForm");

  form.addEventListener("submit", async function (event) {
    event.preventDefault(); // stop page reload

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    console.log("Submitting:", email, password);

    try {
      let response = await fetch("http://127.0.0.1:8000/api/check_login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      let data = await response.json();

      if (response.status === 200) {
        alert("✅ Login successful!");
        console.log("Received token:", data);

        // Store token in localStorage
        localStorage.setItem("token", data.token);

        // Redirect to dashboard
        window.location.href = "http://127.0.0.1:8000/product/";
      } else {
        alert("❌ Login failed: " + (data.message || "Invalid credentials"));
      }
    } catch (error) {
      console.error("Error during login:", error);
      alert("⚠️ Something went wrong, please try again.");
    }
  });
});

