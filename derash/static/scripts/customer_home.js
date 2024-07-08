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
            <div class="latitude-div">
                <label for="latitude">Latitude:</label>
                <input id="latitude" class="coord-input" required>
            </div>
            <div>
                <label for="longitude">Longitude:</label>
                <input id="longitude" class="coord-input" required>
            </div>
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

    $('.past-orders').on('click', () => {
        $(contentDiv).empty()
        $(contentDiv).append('<div class="loader"></div>');
        custGetPastOrders(contentDiv);
    })
})

const mergeDishNames = (dishNames) => {
    let dishesArray = [];

    for (const dishName in dishNames) {
        dishesArray.push(`${dishNames[dishName]}&times; ${dishName}`);
    }
    return (dishesArray.join(', '));
};

const getDateTime = (date) => {
    const dateTime = date.split('T');

    return (dateTime);
};

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
        const restaurantDiv = `<a href="https://derash.zennoon.tech/c/restaurants/${restaurant.id}"><div class="restaurant" data-id=${restaurant.id}>
            <h3 class="restaurant-name">${restaurant.name}</h3>
            <img src="/static/images/restaurant-pics/${restaurant.image_file}" class="restaurant-img">
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
        let confirmDelivered = '<button class="order-delivered">Confirm Delivery</button>';
        if (title === "Pending Orders" && order.customer_confirm) {
            confirmDelivered = '<p class="awaiting-driver">Waiting for driver confirmation</p>';
        }
        if (title === "Past Orders") {
            confirmDelivered = '';
        }
        let driver =  '';
        if (order.driver.id === "0") {
            driver = 'Waiting for a driver to accept delivery'
        } else {
            driver = `Delivered by ${order.driver.first_name + ' ' + order.driver.last_name} , License Plate number: <span class="order-license-num">${order.driver.license_num}</span>, Phone number: <span>${order.driver.phone_num}</span>`;
        }
        const dateTime = getDateTime(order.created_at);
        const orderDiv = `<div class="order" data-id=${order.id}>
        <div class="order-headline">
            <h3 class="order-restaurant-name">Ordered from ${order.restaurant.name}</h3>
            <p class="order-time">${dateTime[0]} at ${dateTime[1]}</p>
        </div>
        <div class="order-body">
            <div class="order-text">
                <p class="order-driver-name">${driver}</p>
                <p class="order-dishes">${mergeDishNames(order.dish_names)}</p>
                <p class="order-price">Order Price: <span>${order.price} ETB</span></p>
                <p class="delivery-fee">Delivery Fee: <span>${order.delivery_fee} ETB</span></p>
                <p class="total-price">Total: <span>${order.price + order.delivery_fee} ETB</span></p>
            </div>
            ${confirmDelivered}
        </div>
    </div>`
        $(orders).append(orderDiv);
    }
    $(element).append(orders);
}

const custGetOpenRestaurants = (element) => {
    $.ajax({
        url: 'https://derash.zennoon.tech/api/customer/open_restaurants',
        success: (data, textStatus) => {
            fillContentRestaurants(element, data, "Open Restaurants");
        }
    }); 
};

const custGetRestaurantsNear = (coords, element) => {
    $.ajax({
        url: 'https://derash.zennoon.tech/api/customer/restaurants_near',
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

const custGetPendingOrders = (element) => {
    $.ajax({
        url: `https://derash.zennoon.tech/api/customer/pending_orders`,
        success: (data, textStatus) => {
            fillContentOrders(element, data, "Pending Orders");
            $('.order-delivered').on('click', (event) => {
                custConfirmOrderDelivered(element, $(event.currentTarget).parent().parent().attr("data-id"));
            })
        }
    });
};

const custConfirmOrderDelivered = (element, orderId) => {
    $(element).empty();
    $(element).append('<div class="loader"></div>');
    $.ajax({
        url: `https://derash.zennoon.tech/api/customer/confirm_delivered/${orderId}`,
        method: "PUT",
        success: (data, textStatus) => {
            custGetPendingOrders(element);
        }
    });
};

const addCustomEventListener = (element, eventName, callback) => {
    $(element).on(eventName, callback);
}

const custGetPastOrders = (element) => {
    $.ajax({
        url: `https://derash.zennoon.tech/api/customer/past_orders`,
        success: (data, textStatus) => {
            fillContentOrders(element, data, 'Past Orders');
            $('.repeat-order').on('click', (event) => {
                $(event.currentTarget).parent().parent().append(`<div class="nearby-select"><div class="coord-form">
                <label for="latitude">Latitude:</label>
                <input id="latitude" class="coord-input" required>
                <label for="longitude">Longitude:</label>
                <input id="longitude" class="coord-input" required>
                <button class="coord-submit">Submit</button>
            </div><h3>or</h3><div class="other-options"><button class="current-location">Use my location</button></div><button class="cancel-repeat">Cancel</button></div>`);
                $(event.currentTarget).remove()
                $('.cancel-repeat').on('click', (event) => {
                    $(element).empty();
                    $(element).append('<div class="loader"></div>');
                    custGetPastOrders(element);
                })
            })
        }
    });
};