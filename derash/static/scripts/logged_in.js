$(document).ready(() => {
    const navLinks = $('.nav-link');
    const appDomain = "http://127.0.0.1:5000"

    for (const link of navLinks) {
        if (appDomain + $(link).attr("href") === location.href) {
            $(link).css("border-bottom", "2px solid rgb(225,28,64)");
        }
    }
})