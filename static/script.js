// ================================
// DARK MODE
// ================================

const themeButton = document.getElementById("theme-btn");

themeButton.addEventListener("click", function () {

    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {
        themeButton.textContent = "☀️";
        localStorage.setItem("theme", "dark");
    } else {
        themeButton.textContent = "🌙";
        localStorage.setItem("theme", "light");
    }

});


// ================================
// LOAD SAVED THEME
// ================================

const savedTheme = localStorage.getItem("theme");

if (savedTheme === "dark") {

    document.body.classList.add("dark-mode");

    if (themeButton) {
        themeButton.textContent = "☀️";
    }
}


// ================================
// REFRESH CHAT
// ================================

const refreshButton = document.getElementById("refresh-btn");

refreshButton.addEventListener("click", function () {

    location.reload();

});