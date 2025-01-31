function togglePassword() {
    const passwordInput = document.getElementById("password");
    const toggleIcon = document.getElementById("toggle-password");
    
    if (passwordInput.type === "password") {
      // Change to text to show password
      passwordInput.type = "text";
      toggleIcon.classList.remove("fa-lock");
      toggleIcon.classList.add("fa-unlock");
    } else {
      // Change back to password to hide
      passwordInput.type = "password";
      toggleIcon.classList.remove("fa-unlock");
      toggleIcon.classList.add("fa-lock");
    }
  }