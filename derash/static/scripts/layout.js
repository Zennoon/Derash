$(document).ready(() => {
    const appDomain = "http://127.0.0.1:5000"
    const headerLinks = $('.header-link');

    for (const link of headerLinks) {
        console.log(appDomain + $(link).attr('href'));
        console.log(location.href);
        if (appDomain + $(link).attr('href') === location.href) {
            $(link).css("color", "rgb(185,22,53)");
        }
    }
})