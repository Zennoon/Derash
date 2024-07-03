$(document).ready(() => {
    const restaurantId = $('.main-content').attr('data-id');
    const restaurantLat = Number($('.restaurant-lat').html());
    const restaurantLng = Number($('.restaurant-lng').html());
    const orderDishes = {};
    const orderDishNames = {};
    let totalPrice = 0;
    const footer = $('footer.restaurant-footer');
    const popup = $('div.popup-order-confirm');
    const reviewsDiv = $('.reviews');
    const toggleReviews = $('.reviews-toggle');
    const reviewText = $('#make-new-review');
    const newReview = $('.new-review');

    $('.add-to-order').on('click', (event) => {
        const dishId = $(event.currentTarget).closest('.restaurant-dish').attr('data-id');
        const dishName = $(event.currentTarget).parent().parent().siblings('.dish-info').find('h2').html();
        const dishAmt = $(event.currentTarget).siblings('span.dish-amt');
        const dishPrice = Number($(event.currentTarget).parent().siblings('h2.dish-price').html().split(' ')[0]);

        if (dishId in orderDishes) {
            orderDishes[dishId] += 1;
        } else {
            orderDishes[dishId] = 1;
        }
        if (dishName in orderDishNames) {
            orderDishNames[dishName] += 1;
        } else {
            orderDishNames[dishName] = 1;
        }
        totalPrice += dishPrice;
        $(dishAmt).html(orderDishes[dishId]);
        $(dishAmt).css("color", "rgb(9, 151, 73)")
    })

    $('.decrease-from-order').on('click', (event) => {
        const dishId = $(event.currentTarget).closest('.restaurant-dish').attr('data-id');
        const dishName = $(event.currentTarget).parent().parent().siblings('.dish-info').find('h2').html();
        const dishAmt = $(event.currentTarget).siblings('span.dish-amt');
        const dishPrice = Number($(event.currentTarget).parent().siblings('h2.dish-price').html().split(' ')[0]);

        if (dishId in orderDishes && (orderDishes[dishId] >= 1)) {
            orderDishes[dishId] -= 1;
            orderDishNames[dishName] -= 1
            totalPrice -= dishPrice;

            if (orderDishes[dishId] === 0) {
                delete orderDishes[dishId];
                $(dishAmt).empty();
            } else {
                $(dishAmt).html(orderDishes[dishId]);
                $(dishAmt).css("color", "rgb(163, 148, 10)")
            }
            if (orderDishNames[dishName] === 0) {
                delete orderDishNames[dishName];
            }
        }
    });

    $('.dish-order-button').on('click', () => {
        $(footer).empty();
        if (totalPrice > 0) {
            $(footer).css("display", "flex");
            $(footer).append(`<h3>Total price (without delivery fee): ${Math.round((totalPrice + Number.EPSILON) * 100) / 100}</h3>
            <button class="restaurant-checkout">Checkout</button>`);
        } else {
            $(footer).css("display", "none");
        }
        $('button.restaurant-checkout').on('click', () => {
            $(popup).empty();
            $(popup).append(`<h1>Your order</h1><i class="fa-solid fa-xmark cancel-mark"></i>`)
            const table = $(`<table class>
                <tr class="headers">
                    <th>Dish</th>
                    <th>Amount</th>
                </tr>    
            </table>`)
            for (let dish in orderDishNames) {
                $(table).append(`<tr>
                    <td>${dish}</td>
                    <td>${orderDishNames[dish]}</td>
                </tr>`);
            }
            $(table).append(`<tr class="order-price">
                    <td>Order price</td>
                    <td>${totalPrice}</td>
                </tr>`);
            $(popup).append(table);

            const locationForm = `<div class="location-submit"><div class="coord-form">
                <label for="latitude">Latitude:</label>
                <input id="latitude" class="coord-input" required>
                <label for="longitude">Longitude:</label>
                <input id="longitude" class="coord-input" required>
                <button class="coord-submit">Submit</button>
            </div>
            <h3>or</h3>
            <div class="other-options"><button class="current-location">Use my location</button></div></div>`
            $(popup).append(locationForm);
            $(popup).append(`<p class="delivery"></p>`)
            $(popup).css("visibility", "visible");

            $('.cancel-mark').on('click', () => {
                $(popup).empty();
                $(popup).css('visibility', 'hidden');
            })

            $('.coord-submit').on('click', () => {
                const customerLat = Number($('input#latitude').val());
                const customerLng = Number($('input#longitude').val());
                
                if (isNaN(customerLat) || isNaN(customerLng)) {
                    $('p.delivery').html(`Please input valid coordinates`);
                    $('p.delivery').css('color', '#f00');
                } else {
                    const deliveryFee = calcDeliveryFee([restaurantLat, restaurantLng], [customerLat, customerLng]);
                    if (deliveryFee > 300) {
                        $('p.delivery').html(`The destination is too far. Please choose another location, or a nearby restaurant`);  
                        $('p.delivery').css('color', '#f00');  
                    } else {
                        const inserted = `<p>Delivery Fee: ${deliveryFee} ETB. Total Price: ${totalPrice + deliveryFee}</p><button class="confirm-order">Confirm order</button>`;
                        $('p.delivery').html(inserted);
                        $('p.delivery').css('color', '#317006');
                    }
                }

                $('.confirm-order').on('click', () => {
                    const data = {
                        "dishes": orderDishes,
                        "destination_latitude": customerLat,
                        "destination_longitude": customerLng,
                        "restaurant_id": $('.main-content').attr('data-id')
                    }
                    custCreateOrder(data);
                    $('.confirm-order').empty();
                    $('.confirm-order').append('<p>Your order has been successfully made!</p>');
                    $('.confirm-order').addClass('order-success');
                    $('.order-success').removeClass('confirm-order');
                    $('.order-success').off('click');
                })
            })

            $('.current-location').on('click', () => {
                navigator.geolocation.getCurrentPosition((position) => {
                    const customerCoords = [position.coords.latitude, position.coords.longitude];

                    const deliveryFee = calcDeliveryFee([restaurantLat, restaurantLng], customerCoords);
                    if (deliveryFee > 300) {
                        $('p.delivery').html(`The destination is too far. Please choose another location, or a nearby restaurant`);
                        $('p.delivery').css('color', '#f00');    
                    } else {
                        const inserted = `<p>Delivery Fee: ${deliveryFee} ETB. Total Price: ${totalPrice + deliveryFee}</p><button class="confirm-order">Confirm order</button>`;
                        $('p.delivery').html(inserted);
                        $('p.delivery').css('color', '#317006');
                    }
                    $('.confirm-order').on('click', () => {
                        const data = {
                            "dishes": orderDishes,
                            "destination_latitude": customerCoords[0],
                            "destination_longitude": customerCoords[1],
                            "restaurant_id": $('.main-content').attr('data-id')
                        }
                        custCreateOrder(data);
                        $('.confirm-order').empty();
                        $('.confirm-order').append('<p>Your order has been successfully made!</p>');
                        $('.confirm-order').addClass('order-success');
                        $('.order-success').removeClass('confirm-order');
                        $('.order-success').off('click');
                    });
                });
            });
        });
    });

    $(toggleReviews).on('click', () => {
        if ($(toggleReviews).hasClass('show')) {
            $(toggleReviews).removeClass('show');
            $(toggleReviews).html('Hide');
            $(reviewsDiv).append(`<div class="loader"></div>`);
            custGetRestaurantReviews(reviewsDiv, restaurantId);
        } else {
            $(toggleReviews).addClass('show');
            $(toggleReviews).html('Show');
            $(reviewsDiv).empty();
        }
    });

    $('.make-review').on('click', () => {
        if ($(reviewText).val() === '') {
            $(reviewText).html('Please enter your review');
        } else if ($(reviewText).val() === 'Please enter your review') {
            $(reviewText).html('Please enter your review');
        } else {
            custMakeReview(restaurantId, reviewText, toggleReviews, reviewsDiv);
        }
    })
});

const getDateTime = (date) => {
    const dateTime = date.split('T');

    return (dateTime);
};

const calcDeliveryFee = (restaurantCoord, customerCoord) => {
    const lat1 = restaurantCoord[0] * (Math.PI / 180);
    const lat2 = customerCoord[0] * (Math.PI / 180);
    const lon1 = restaurantCoord[1] * (Math.PI / 180)
    const lon2 = customerCoord[1] * (Math.PI / 180)
    radius = 6371

    const dist = Math.acos(Math.sin(lat1)*Math.sin(lat2)+Math.cos(lat1)*Math.cos(lat2)*Math.cos(lon2-lon1))*radius;
    return (50 + Math.floor(dist * 15));

}

const custCreateOrder = (data) => {
    $.ajax({
        url: 'https://derash.zennoon.tech/api/customer/new_order',
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        data: JSON.stringify(data)
    });   
};

const custGetRestaurantReviews = (reviewsDiv, restaurantId) => {
    $.ajax({
        url: `https://derash.zennoon.tech/api/customer/restaurants/${restaurantId}/reviews`,
        success: (data, textStatus) => {
            $(reviewsDiv).empty();

            if (data.length === 0) {
                $(reviewsDiv).append('<p>No reviews made yet</p>')
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

                $(reviewsDiv).append(reviewData);
            }
        }
    });
};

const custMakeReview = (restaurantId, text, toggleReviews, reviewsDiv) => {
    $.ajax({
        url: `https://derash.zennoon.tech/api/customer/restaurants/${restaurantId}/make-review`,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        data: JSON.stringify({
            "text": $(text).val()
        }),
        success: () => {
            $(text).val('');
            if (! $(toggleReviews).hasClass('show')) {
                custGetRestaurantReviews(reviewsDiv, restaurantId);
            }
        }
    })
}
