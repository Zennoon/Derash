$(document).ready(() => {
    const contentDiv = $('div.content');
    const toggleActiveDiv = $('div.toggle-active');
    const toggleActivePara = $(toggleActiveDiv).find('p');
    const toggleActiveButton = $(toggleActiveDiv).find('button');

    const driverActivate = () => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/driver/activate`,
            method: "PUT",
            success: () => {
                $(toggleActiveButton).removeClass('activate');
                $(toggleActiveButton).html('Deactivate');
                $(toggleActiveButton).addClass('deactivate');            
                $(toggleActivePara).html('You are currently <span class="active">active</span> and accepting requests');
                $($(contentDiv).find('.error-text')).remove();
            }
        });
    };
    
    const driverDeactivate = () => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/driver/deactivate`,
            method: "PUT",
            success: () => {
                $(toggleActiveButton).removeClass('deactivate');
                $(toggleActiveButton).html('Activate')
                $(toggleActiveButton).addClass('activate');            
                $(toggleActivePara).html('You are currently <span class="dormant">dormant</span> and not accepting requests');   
            }
        });
    };

    const driverGetCurrentDelivery = () => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/driver/current_delivery`,
            method: "GET",
            success: (data, textStatus) => {
                fillContentPendingDelivery(contentDiv, data, "Pending Delivery");
                $('.confirm-delivered').on('click', (event) => {
                    const orderId = $($(event.currentTarget).parent().parent()).attr('data-id');

                    driverConfirmDelivery(orderId);
                })
            }
        });
    };

    const driverConfirmDelivery = (orderId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/driver/${orderId}/delivered`,
            method: "PUT",
            success: () => {
                $(contentDiv).empty();
                $(contentDiv).append('<div class="loader"></div>');
                driverGetCurrentDelivery();
            }
        });
    };

    const driverGetPossibleDeliveries = () => {
        navigator.geolocation.getCurrentPosition((position) => {
            const driverCoords = [position.coords.latitude, position.coords.longitude];
            $.ajax({
                url: `http://127.0.0.1:5000/api/driver/possible_deliveries`,
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                data: JSON.stringify({
                    "coords": driverCoords
                }),
                success: (data, textStatus) => {
                    fillContentPossibleDeliveries(contentDiv, data, "Possible Deliveries");
                    $('.accept-delivery').on('click', (event) => {
                        const orderId = $($(event.currentTarget).parent().parent()).attr('data-id');
                        driverAcceptDelivery(orderId, $(event.currentTarget))
                    })
                }
            });
        });   

        const driverAcceptDelivery = (orderId, button) => {
            $.ajax({
                url: `http://127.0.0.1:5000/api/driver/${orderId}/accept`,
                method: "PUT",
                success: (data, textStatus) => {
                    $(contentDiv).empty();
                    $(contentDiv).append('<div class="loader"></div>');
                    driverGetPossibleDeliveries();
                },
                error: (error) => {
                    $($(button).parent().children('.order-text').find('.error-text')).remove()
                    $($(button).parent().children('.order-text')).append(`<p class="error-text">${error.responseText}</p>`);
                }
            });
        };
    };

    const driverGetPastDeliveries = () => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/driver/past_deliveries`,
            method: "GET",
            success: (data, textStatus) => {
                fillContentPastDeliveries(contentDiv, data, "Past Deliveries")
            }
        });
    };

    const driverGetPastMonthReceipt = () => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/driver/past_month`,
            method: "GET",
            success: (data, textStatus) => {
                fillContentPastMonthDeliveries(contentDiv, data, "Past Month's Deliveries");
            },
            error: (error) => {
                fillContentPastMonthDeliveries(contentDiv, null, "Past Month's Deliveries");
            }
        });
    };

    driverGetCurrentDelivery();
    $(toggleActiveButton).on('click', () => {
        if ($(toggleActiveButton).hasClass('activate')) {
            driverActivate();
        } else if ($(toggleActiveButton).hasClass('deactivate')) {
            driverDeactivate();
        }
    })

    $('.nav-item').on('click', (event) => {
        for (const link of $('.nav-item')) {
            $(link).removeClass('clicked');
        }
        $(event.currentTarget).addClass('clicked');
        $(contentDiv).empty();
        $(contentDiv).append('<div class="loader"></div>');
    });

    $('.pending-delivery').on('click', () => {
        driverGetCurrentDelivery();
    });

    $('.possible-deliveries').on('click', () => {
        driverGetPossibleDeliveries();
    });

    $('.past-deliveries').on('click', () => {
        driverGetPastDeliveries();
    });

    $('.deliveries-past-month').on('click', () => {
        driverGetPastMonthReceipt();
    });
});

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

const calcDistance = (restaurantCoord, customerCoord) => {
    const lat1 = restaurantCoord[0] * (Math.PI / 180);
    const lat2 = customerCoord[0] * (Math.PI / 180);
    const lon1 = restaurantCoord[1] * (Math.PI / 180)
    const lon2 = customerCoord[1] * (Math.PI / 180)
    radius = 6371

    const dist = Math.acos(Math.sin(lat1)*Math.sin(lat2)+Math.cos(lat1)*Math.cos(lat2)*Math.cos(lon2-lon1))*radius;
    return (dist);

}

const fillContentPendingDelivery = (element, data, title) => {
    $(element).empty();
    $(element).append(`<h1 class='section-title'>${title}</h1>`);
    const orders = $('<div class="orders"></div>');

    if (data.length === 0) {
        $(orders).append(`<p class="empty-list">You don't have any pending deliveries</p>`)
    }

    for (const order of data) {
        const dateTime = getDateTime(order.created_at);
        const restaurantLocation = `Restaurant location: Lat: <span>${order.restaurant.latitude}</span>, Lng: <span>${order.restaurant.longitude}</span>`;
        const customerLocation = `Destination: Lat: <span>${order.destination_latitude}</span>, Lng: <span>${order.destination_longitude}</span>`;
        const distance = calcDistance([order.restaurant.latitude, order.restaurant.longitude], [order.destination_latitude, order.destination_longitude]);

        let confirmDeliveredButton = `<button class="confirm-delivered">Confirm Delivery</button>`;
        if (order.driver_confirm) {
            confirmDeliveredButton = '<p class="awaiting-customer">Waiting for customer confirmation</p>';
        }

        const orderDiv = `<div class="order" data-id=${order.id}>
            <div class="order-headline">
                <h3 class="order-customer-name">Ordered by ${order.customer.first_name + ' ' + order.customer.last_name} from ${order.restaurant.name}</h3>
                <p class="order-time">${dateTime[0]} at ${dateTime[1]}</p>
            </div>
            <div class="order-body">
                <div class="order-text">
                    <p class="order-restaurant-location">${restaurantLocation}</p>
                    <p class="order-destination">${customerLocation}</p>
                    <p class="order-distance">Distance: <span>${distance} Km</span></p>
                    <p class="customer-phone"><span>${order.customer.first_name}</span>'s phone number: <span>${order.customer.phone_num}</span></p>
                    <p class="order-dishes">${mergeDishNames(order.dish_names)}</p>
                    <p class="order-price">Order Price: <span>${order.price} ETB</span></p>
                    <p class="delivery-fee">Delivery Fee: <span>${order.delivery_fee} ETB</span></p>
                    <p class="total-price">Total: <span>${order.price + order.delivery_fee} ETB</span></p>
                </div>
                ${confirmDeliveredButton}
            </div>
        </div>`
        $(orders).append(orderDiv);
    }
    $(element).append(orders);
};

const fillContentPossibleDeliveries = (element, data, title) => {
    $(element).empty();
    $(element).append(`<h1 class='section-title'>${title}</h1>`);
    const orders = $('<div class="orders"></div>');
    const acceptDeliveryButton = `<button class="accept-delivery">Accept Delivery</button>`;

    if (data.length === 0) {
        $(orders).append(`<p class="empty-list">You don't have any possible deliveries</p>`)
    }

    for (const order of data) {
        const dateTime = getDateTime(order.created_at);
        const restaurantLocation = `Restaurant location: Lat: <span>${order.restaurant.latitude}</span>, Lng: <span>${order.restaurant.longitude}</span>`;
        const customerLocation = `Destination: Lat: <span>${order.destination_latitude}</span>, Lng: <span>${order.destination_longitude}</span>`;
        const distance = calcDistance([order.restaurant.latitude, order.restaurant.longitude], [order.destination_latitude, order.destination_longitude]);

        const orderDiv = `<div class="order" data-id=${order.id}>
            <div class="order-headline">
                <h3 class="order-customer-name">Ordered by ${order.customer.first_name + ' ' + order.customer.last_name} from ${order.restaurant.name}</h3>
                <p class="order-time">${dateTime[0]} at ${dateTime[1]}</p>
            </div>
            <div class="order-body">
                <div class="order-text">
                    <p class="order-restaurant-location">${restaurantLocation}</p>
                    <p class="order-destination">${customerLocation}</p>
                    <p class="order-distance">Distance: <span>${distance} Km</span></p>
                    <p class="order-price">Order Price: <span>${order.price} ETB</span></p>
                    <p class="delivery-fee">Delivery Fee: <span>${order.delivery_fee} ETB</span></p>
                    <p class="total-price">Total: <span>${order.price + order.delivery_fee} ETB</span></p>
                </div>
                ${acceptDeliveryButton}
            </div>
        </div>`
        $(orders).append(orderDiv);
    }
    $(element).append(orders);
};

const fillContentPastDeliveries = (element, data, title) => {
    $(element).empty();
    $(element).append(`<h1 class='section-title'>${title}</h1>`);
    const orders = $('<div class="orders"></div>');

    if (data.length === 0) {
        $(orders).append(`<p class="empty-list">You don't have any past deliveries</p>`)
    }

    for (const order of data) {
        const dateTime = getDateTime(order.created_at);
        const restaurantLocation = `Restaurant location: Lat: <span>${order.restaurant.latitude}</span>, Lng: <span>${order.restaurant.longitude}</span>`;
        const customerLocation = `Destination: Lat: <span>${order.destination_latitude}</span>, Lng: <span>${order.destination_longitude}</span>`;
        const distance = calcDistance([order.restaurant.latitude, order.restaurant.longitude], [order.destination_latitude, order.destination_longitude]);

        const orderDiv = `<div class="order" data-id=${order.id}>
            <div class="order-headline">
                <h3 class="order-customer-name">Ordered by ${order.customer.first_name + ' ' + order.customer.last_name} from ${order.restaurant.name}</h3>
                <p class="order-time">${dateTime[0]} at ${dateTime[1]}</p>
            </div>
            <div class="order-body">
                <div class="order-text">
                    <p class="order-restaurant-location">${restaurantLocation}</p>
                    <p class="order-destination">${customerLocation}</p>
                    <p class="order-distance">Distance: <span>${distance} Km</span></p>
                    <p class="customer-phone"><span>${order.customer.first_name}</span>'s phone number: <span>${order.customer.phone_num}</span></p>
                    <p class="order-dishes">${mergeDishNames(order.dish_names)}</p>
                    <p class="order-price">Order Price: <span>${order.price} ETB</span></p>
                    <p class="delivery-fee">Delivery Fee: <span>${order.delivery_fee} ETB</span></p>
                    <p class="total-price">Total: <span>${order.price + order.delivery_fee} ETB</span></p>
                </div>
            </div>
        </div>`
        $(orders).append(orderDiv);
    }
    $(element).append(orders);
};

const fillContentPastMonthDeliveries = (element, data, title) => {
    $(element).empty();
    $(element).append(`<h1 class='section-title'>${title}</h1>`);
    const orders = $('<div class="orders"></div>');
    let totalPrice = 0;
    let totalDeliveryFees = 0;

    if (data === null) {
        $(element).append('<p class="empty-list">Your account was created less than a month ago</p>');
    } else {
        for (const order of data) {
            const dateTime = getDateTime(order.created_at);
            const restaurantLocation = `Restaurant location: Lat: <span>${order.restaurant.latitude}</span>, Lng: <span>${order.restaurant.longitude}</span>`;
            const customerLocation = `Destination: Lat: <span>${order.destination_latitude}</span>, Lng: <span>${order.destination_longitude}</span>`;
            const distance = calcDistance([order.restaurant.latitude, order.restaurant.longitude], [order.destination_latitude, order.destination_longitude]);
            const orderDiv = `<div class="order" data-id=${order.id}>
                <div class="order-headline">
                    <h3 class="order-customer-name">Ordered by ${order.customer.first_name + ' ' + order.customer.last_name} from ${order.restaurant.name}</h3>
                    <p class="order-time">${dateTime[0]} at ${dateTime[1]}</p>
                </div>
                <div class="order-body">
                    <div class="order-text">
                        <p class="order-restaurant-location">${restaurantLocation}</p>
                        <p class="order-destination">${customerLocation}</p>
                        <p class="order-distance">Distance: <span>${distance} Km</span></p>
                        <p class="customer-phone"><span>${order.customer.first_name}</span>'s phone number: <span>${order.customer.phone_num}</span></p>
                        <p class="order-dishes">${mergeDishNames(order.dish_names)}</p>
                        <p class="order-price">Order Price: <span>${order.price} ETB</span></p>
                        <p class="delivery-fee">Delivery Fee: <span>${order.delivery_fee} ETB</span></p>
                        <p class="total-price">Total: <span>${order.price + order.delivery_fee} ETB</span></p>
                    </div>
                </div>
            </div>`
            $(orders).append(orderDiv);
            totalPrice += order.price;
            totalDeliveryFees += order.delivery_fee;
        }
        $(element).append(`<p class="receipt-summary">In the past month, you have completed <span>${data.length} deliveries</span>, and collected <span>${totalPrice} ETB in orders</span>, and <span>${totalDeliveryFees} in delivery fees</span>. In summary you have earned <span>${totalDeliveryFees * 0.75} ETB</span> (75% of the total delivery fees), and you are expected to <span>submit ${totalPrice + (totalDeliveryFees * 0.25)} ETB</span> to the nearest Derash center by the end of this month</p>`);
        $(element).append(orders);
    }
};
