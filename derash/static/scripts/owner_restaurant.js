$(document).ready(() => {
    $('.restaurant-details').addClass('clicked');

    const contentDiv = $('div.content');
    const restaurantId = $(contentDiv).attr('data-id');

    ownerGetRestaurantDetails(contentDiv, restaurantId);

    $('.nav-item').on('click', (event) => {
        for (const link of $('.nav-item')) {
            $(link).removeClass('clicked');
        }
        $(event.currentTarget).addClass('clicked');
        $(contentDiv).empty();
        $(contentDiv).append('<div class="loader"></div>');
    });

    $('.restaurant-details').on('click', () => {
        ownerGetRestaurantDetails(contentDiv, restaurantId);
    });

    $('.pending-orders').on('click', () => {
        ownerGetPendingRestaurantOrders(contentDiv, restaurantId);
    });

    $('.past-orders').on('click', () => {
        ownerGetPastRestaurantOrders(contentDiv, restaurantId);
    });

    $('.orders-past-month').on('click', () => {
        ownerGetPastMonthReceipt(contentDiv, restaurantId);
    })
});

const getDateTime = (date) => {
    const dateTime = date.split('T');

    return (dateTime);
};

const mergeDishNames = (dishNames) => {
    let dishesArray = [];

    for (const dishName in dishNames) {
        dishesArray.push(`${dishNames[dishName]}&times; ${dishName}`);
    }
    return (dishesArray.join(', '));
};

const fillContentOrders = (element, data, title) => {
    $(element).empty();
    $(element).append(`<h1 class='section-title'>${title}</h1>`);
    const orders = $('<div class="orders"></div>');
    let totalPrice = 0;
    let preparedButton = '<button class="order-prepared">Confirm Done</button>';

    if (data === null) {
        $(element).append('<p>This restaurant was created less than a month ago</p>');
    } 
    if (data.length === 0 && title != "Past Month's Orders") {
        $(orders).append('<p class="empty-list">No result has been found. Try another query</p>')
    }
    if (title != "Pending Orders") {
        preparedButton = '';
    }

    for (const order of data) {
        const dateTime = getDateTime(order.created_at);
        let driver = '';
        if (order.driver.id === "0") {
            driver = 'Waiting for a driver to accept delivery'
        } else {
            driver = `Delivered by ${order.driver.first_name + ' ' + order.driver.last_name} , License Plate number: <span class="order-license-num">${order.driver.license_num}</span>, Phone number: <span>${order.driver.phone_num}</span>`;
        }
        const orderDiv = `<div class="order" data-id=${order.id}>
            <div class="order-headline">
                <a><h3 class="order-customer-name">Ordered by ${order.customer.first_name + ' ' + order.customer.last_name}</h3></a>
                <p class="order-time">${dateTime[0]} at ${dateTime[1]}</p>
            </div>
            <div class="order-body">
                <div class="order-text">
                    <p class="order-driver-name">${driver}</p>
                    <p class="order-dishes">${mergeDishNames(order.dish_names)}</p>
                    <p class="order-price">Order price: <span>${order.price} ETB</span></p>
                </div>
                ${preparedButton}
            </div>
        </div>`
        $(orders).append(orderDiv);
        totalPrice += order.price;
    }
    if (title === "Past Month's Orders") {
        $(element).append(`<p class="receipt-summary">This restaurant has served ${data.length} orders last month, and has earned a total of ${totalPrice} ETB</p>`)
    }
    $(element).append(orders);
};

const ownerGetRestaurantDetails = (element, restaurantId, popUp) => {
    $.ajax({
        url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}`,
        success: (data, textStatus) => {
            $(element).empty();
            const restaurantIntro = `<div class="intro">
                <h1>${data.name}</h1>
                <a class="edit-restaurant" href="http://127.0.0.1:5000/o/restaurants/${restaurantId}/update"><i class="fa-solid fa-pen"></i> Edit</a>
            </div>`;
            const restaurantDesc = `<div class="description">
                <img src="/static/images/restaurant-pics/${data.image_file}" class="restaurant-img">
                <p>${data.description || ''}</p>
                <p><i class="fa-solid fa-location-dot"></i> Lat: ${data.latitude} Lng: ${data.longitude}</p>
            </div>`;
            const restaurantDishes = $(`<div class="dishes-section">
                <div class="dishes-intro">
                    <h2>Dishes</h2>
                    <a class="new-dish" href="http://127.0.0.1:5000/o/restaurants/${restaurantId}/add-dish"><i class="fa-solid fa-plus"></i> New</a>
                </div>
            </div>`);
            const dishes = $(`<div class="dishes"></div>`);
            for (const dish of data.dishes) {
                $(dishes).append(`<div class="dish" data-id=${dish.id}>
                    <div class="dish-main">
                        <div class="dish-intro">
                            <img src="/static/images/dish-pics/${dish.image_file}" class="dish-img">
                            <h2>${dish.name}</h2>
                        </div>
                        <span class="dish-price">${dish.price} ETB</span>
                        <a class="edit-dish" href="http://127.0.0.1:5000/o/dish/${dish.id}/edit"><i class="fa-solid fa-pen"></i> Edit</a>
                    </div>
                    <div class="dish-desc">
                        <p>Description: ${dish.description || ''}</p>
                        <p>Ingredients: ${dish.ingredients}</p>
                    </div>
                </div>`);
            }

            const restaurantReviews = `<div class="reviews-section">
            <div class="reviews-intro">
                <h2>Reviews</h2>
                <button class="reviews-toggle show">Show</button>
            </div>
            <div class="reviews"></div>
            </div>`
            $(restaurantDishes).append($(dishes));
            $(element).append(restaurantIntro);
            $(element).append(restaurantDesc);
            $(element).append(restaurantDishes);
            $(element).append(restaurantReviews);

            $('.reviews-toggle').on('click', (event) => {
                if ($(event.currentTarget).hasClass('show')) {
                    $(event.currentTarget).html('Hide');
                    $(event.currentTarget).removeClass('show');
                    $('.reviews').append('<div class="loader"></div>');
                    ownerGetRestaurantReviews(restaurantId);
                } else {
                    $(event.currentTarget).html('Show');
                    $(event.currentTarget).addClass('show');
                    $('.reviews').empty();
                }
            })
        }
    });
};

const ownerGetRestaurantReviews = (restaurantId) => {
    $.ajax({
        url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}/reviews`,
        success: (data, textStatus) => {
            const reviews = $('.reviews');

            $(reviews).empty();
            if (data.length === 0) {
                $(reviews).append('<p>No reviews made yet</p>')
            }
            for (const review of data) {
                const dateTime = getDateTime(review.created_at);
                const reviewData = $(`<div class="review">
                    <div class="review-headline">
                        <div class="reviewer">
                            <img src="/static/images/profile-pics/${review.customer.image_file}" class="reviewer-img">
                            <h3>${review.customer.first_name + ' ' + review.customer.last_name}</h3>
                        </div>
                        <span>${dateTime[0]} at ${dateTime[1]}</span>
                    </div>
                    <p class="review-text">${review.text}</p>    
                </div>`);

                $(reviews).append(reviewData);
            }
        }
    });    
};

const ownerGetPendingRestaurantOrders = (element, restaurantId) => {
    $.ajax({
        url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}/pending_orders`,
        method: "GET",
        success: (data, textStatus) => {
            fillContentOrders(element, data, "Pending Orders");

            $('.order-prepared').on('click', (event) => {
                $(element).empty();
                $(element).append('<div class="loader"></div>');
                ownerConfirmOrderMade($($(event.currentTarget).parent().parent()).attr('data-id'), element, restaurantId);
            });
        }
    });  
};

const ownerConfirmOrderMade = (orderId, element, restaurantId) => {
    $.ajax({
        url: `http://127.0.0.1:5000/api/owner/my_orders/${orderId}/done`,
        method: "PUT",
        success: () => {
            ownerGetPendingRestaurantOrders(element, restaurantId);
        }
    }); 
};

const ownerGetPastRestaurantOrders = (element, restaurantId) => {
    $.ajax({
        url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}/past_orders`,
        method: "GET",
        success: (data, textStatus) => {
            fillContentOrders(element, data, "Past Orders");
        }
    });  
};

const ownerGetPastMonthReceipt = (element, restaurantId) => {
    $.ajax({
        url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}/past_month`,
        method: "GET",
        success: (data, textStatus) => {
            fillContentOrders(element, data, "Past Month's Orders")
        },
        error: (error) => {
            fillContentOrders(element, null, "Past Month's Orders")
        }
    });
};