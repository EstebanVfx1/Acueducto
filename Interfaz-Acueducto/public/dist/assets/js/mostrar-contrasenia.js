const passwordInput = document.getElementById("user_contrasenia");
const showPasswordCheckbox = document.getElementById("showPassword");

showPasswordCheckbox.addEventListener("change", function() {
    if (showPasswordCheckbox.checked) {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
});