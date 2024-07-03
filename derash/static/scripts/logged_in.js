$(document).ready(() => {
    const navLinks = $('.nav-link');
    const appDomain = "https://derash.zennoon.tech"

    for (const link of navLinks) {
        if (appDomain + $(link).attr("href") === location.href) {
            $(link).css("border-bottom", "2px solid rgb(225,28,64)");
        }
    }
})