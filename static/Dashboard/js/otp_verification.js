// Timer
let timeLeft = 30; 
let timerDisplay = document.getElementById("timerText");
let resendBtn = document.getElementById("resendBtn");

function startTimer() {
  resendBtn.disabled = true;
  timeLeft = 30;
  timerDisplay.textContent = `Resend available in ${timeLeft}s`;

  let countdown = setInterval(() => {
    timeLeft--;
    timerDisplay.textContent = `Resend available in ${timeLeft}s`;

    if (timeLeft <= 0) {
      clearInterval(countdown);
      timerDisplay.textContent = "You can now resend the code.";
      resendBtn.disabled = false;
    }
  }, 1000);
}

// Start timer on page load
startTimer();

// Restart timer when "Resend" is clicked
resendBtn.addEventListener("click", () => {
  alert("OTP resent! (call backend API here)");
  startTimer();
});

// Auto move to next OTP input
let otpInputs = document.querySelectorAll(".otp-input");
otpInputs.forEach((input, index) => {
  input.addEventListener("input", () => {
    if (input.value.length === 1 && index < otpInputs.length - 1) {
      otpInputs[index + 1].focus();
    }
  });
});

// Verify OTP
document.getElementById("verifyBtn").addEventListener("click", () => {
  let otp = "";
  otpInputs.forEach(input => otp += input.value);

  if (otp.length < 4) {
    alert("⚠️ Please enter the full 4-digit OTP.");
    return;
  }

  // Example user_id (replace with actual from signup/login flow)
  // let userId = 10;
  const urlParams = new URLSearchParams(window.location.search);
  const userId = urlParams.get("user_id");

  fetch("http://127.0.0.1:8000/api/verify_otp/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: userId,
      otp: otp
    }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert("✅ OTP Verified! Redirecting...");
        window.location.href = "http://127.0.0.1:8000/views/loginn/";
      } else {
        alert("❌ " + data.error);
      }
    })
    .catch(err => console.error("Error:", err));
});
