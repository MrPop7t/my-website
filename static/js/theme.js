var main = document.getElementById("page")
var switcher = document.getElementById("themeButton")

var storedTheme = localStorage.theme;

switcher.addEventListener("click", themeEvent);
document.addEventListener('DOMContentLoaded', function() {
    if (storedTheme != null || storedTheme != undefined) {
        changeTheme(storedTheme);
    };
}, false);

function themeEvent() {

    if (main.classList.value.includes("dark")) {
        changeTheme("light")
        storeTheme("light")
        switcher._tippy.setContent(`Dark theme`);
    } else {
        changeTheme("dark")
        storeTheme("dark")
        switcher._tippy.setContent(`Light theme`);
    }

    if (storedTheme == null || storedTheme == undefined) {
        storeTheme("dark")
    }
}

function storeTheme(theme) {
    try {
        localStorage.theme = theme;
        return true
    } catch (e) {
        return false
    } 
}

function changeTheme(theme) {

    if (theme == "dark") {
        document.getElementById("page").classList.add("dark")
    }

    if (theme == "light") {
        document.getElementById("page").classList.remove("dark")
    }
}