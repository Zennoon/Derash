$(document).ready(() => {
    $('.open-restaurants').addClass('clicked');

    const contentDiv = $('div.content');
    $(contentDiv).append('<div class="loader"></div>');
    custGetOpenRestaurants(contentDiv);

    $('.nav-item').on('click', (event) => {
        for (const link of $('.nav-item')) {
            $(link).removeClass('clicked');
        }

        $(event.currentTarget).addClass('clicked');
    });

    $('.open-restaurants').on('click', () => {
        $(contentDiv).empty()
        $(contentDiv).append('<div class="loader"></div>');
        custGetOpenRestaurants(contentDiv);
    });

    $('.nearby-restaurants').on('click', () => {
        $(contentDiv).empty();
        $(contentDiv).append(`<div class="nearby-select"><div class="coord-form">
            <label for="latitude">Latitude:</label>
            <input id="latitude" class="coord-input" required>
            <label for="longitude">Longitude:</label>
            <input id="longitude" class="coord-input" required>
            <button class="coord-submit"><i class="fa-solid fa-magnifying-glass"></i></button>
        </div><h3>or</h3><div class="other-options"><button class="show-map">Select on map</button><button class="current-location">Use my location</button></div></div>`);
        $('.coord-submit').on('click', () => {
            let lat = Number($('input#latitude').val()), lng = Number($('input#longitude').val());
            if (isNaN(lat)) {
                lat = 0;
            }
            if (isNaN(lng)) {
                lng = 0;
            }
            const coords = {
                "coords": [lat, lng]
            };
            $(contentDiv).empty();
            $(contentDiv).append('<div class="loader"></div>');
            custGetRestaurantsNear(coords, contentDiv);
        });

        $('.current-location').on('click', () => {
            navigator.geolocation.getCurrentPosition((position) => {
                const coords = {"coords": [position.coords.latitude, position.coords.longitude]};
                console.log(coords);

                $(contentDiv).empty();
                $(contentDiv).append('<div class="loader"></div>');
                custGetRestaurantsNear(coords, contentDiv);
            });
        });
    });

    $('.pending-orders').on('click', () => {
        $(contentDiv).empty()
        $(contentDiv).append('<div class="loader"></div>');
        custGetPendingOrders(contentDiv);
    })
})

const fillContentRestaurants = (element, data, title) => {
    $(element).empty();
    $(element).append(`<h1 class='section-title'>${title}</h1>`);
    const restaurants = $('<div class="restaurants"></div>');
    if (data.length === 0) {
        $(restaurants).append('<p class="empty-list">No result has been found. Try another query</p>')
    }
    for (const restaurant of data) {
        if (!restaurant.description) {
            restaurant.description = "";
        }
        const restaurantDiv = `<a href="#"><div class="restaurant" data-id=${restaurant.id}>
            <h3 class="restaurant-name">${restaurant.name}</h3>
            <img src="/static/images/restaurant-pics/${restaurant.image_file}.png" class="restaurant-img">
            <div class="restaurant-text">
                <p>${restaurant.description}</p>
                <p class="restaurant-location"><i class="fa-solid fa-location-dot"></i>lat: ${restaurant.latitude} lng: ${restaurant.longitude}</p>
            </div>
        </div></a>`
        $(restaurants).append(restaurantDiv);
    }
    $(element).append(restaurants);
}

const fillContentOrders = (element, data, title) => {
    $(element).empty();
    $(element).append(`<h1 class='section-title'>${title}</h1>`);
    const orders = $('<div class="orders"></div>');
    if (data.length === 0) {
        $(orders).append('<p class="empty-list">No result has been found. Try another query</p>')
    }
    for (const order of data) {
        const orderDiv = `<a href="#"><div class="order" data-id=${restaurant.id}>
            <h3 class="order-name">${restaurant.name}</h3>
            <img src="/static/images/restaurant-pics/${restaurant.image_file}.png" class="restaurant-img">
            <div class="restaurant-text">
                <p>${restaurant.description}</p>
                <p class="restaurant-location"><i class="fa-solid fa-location-dot"></i>lat: ${restaurant.latitude} lng: ${restaurant.longitude}</p>
            </div>
        </div></a>`
        $(orders).append(restaurantDiv);
    }
    $(element).append(orders);
}

const custGetOpenRestaurants = (element) => {
    $.ajax({
        url: 'http://127.0.0.1:5000/api/customer/open_restaurants',
        success: (data, textStatus) => {
            fillContentRestaurants(element, data, "Open Restaurants");
        }
    }); 
};

const custGetRestaurantsNear = (coords, element) => {
    $.ajax({
        url: 'http://127.0.0.1:5000/api/customer/restaurants_near',
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        data: JSON.stringify(coords),
        success: (data, textStatus) => {
            fillContentRestaurants(element, data, "Nearby Restaurants");
        }
    });
};

const custGetPendingOrders = () => {
    $.ajax({
        url: `http://127.0.0.1:5000/api/customer/pending_orders`,
        success: (data, textStatus) => {
            console.log(data);
        }
    });
};