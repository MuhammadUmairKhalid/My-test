async function signupUser() {
    event.preventDefault();
    // Get values from input fields
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
      let response = await fetch("http://127.0.0.1:8000/api/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          email: email,
          password: password,
        }),
      });

      let data = await response.json();
      console.log(data)

      if (data.status === 200) {
        alert(data["message"]);
        let user_id = data["user_id"]
        // Optionally redirect to OTP page
       window.location.href = `http://127.0.0.1:8000/views/otp_page/?user_id=${user_id}`;
      } else {
        alert("❌ Signup failed: " + data["message"]);
      }
    } catch (error) {
      console.error("Error during signup:", error);
      alert("⚠️ Something went wrong, please try again.",error);
    }
  }
