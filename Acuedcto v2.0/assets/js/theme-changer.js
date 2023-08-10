const darkModeToggle = document.getElementById("darkModeToggle");
const body = document.body;

darkModeToggle.addEventListener("change", function () {
  if (darkModeToggle.checked) {
    body.classList.add("dark-theme");
  } else {
    body.classList.remove("dark-theme");
  }
});
