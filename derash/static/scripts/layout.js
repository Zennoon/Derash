$(document).ready(() => {
    const appDomain = "https://derash.zennoon.tech"
    const headerLinks = $('.header-link');

    for (const link of headerLinks) {
        if (appDomain + $(link).attr('href') === location.href) {
	    $(link).css("color", "rgb(185,22,53)");
        }
    }
});
