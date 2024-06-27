$(document).ready(() => {
    $('.restaurant-details').addClass('clicked');

    const contentDiv = $('div.content');
    const restaurantId = $(contentDiv).attr('data-id');
    const popUpCont = $(contentDiv).html();

    console.log(popUpCont)
    $(contentDiv).empty();
    $(contentDiv).append('<div class="loader"></div>');
    ownerGetRestaurantDetails(contentDiv, restaurantId, popUpCont);
//     ownerGOpenRestaurants(contentDiv);

//     $('.nav-item').on('click', (event) => {
//         for (const link of $('.nav-item')) {
//             $(link).removeClass('clicked');
//         }

//         $(event.currentTarget).addClass('clicked');
//     });

//     $('.open-restaurants').on('click', () => {
//         $(contentDiv).empty()
//         $(contentDiv).append('<div class="loader"></div>');
//         custGetOpenRestaurants(contentDiv);
//     });

//     $('.nearby-restaurants').on('click', () => {
//         $(contentDiv).empty();
//         $(contentDiv).append(`<div class="nearby-select"><div class="coord-form">
//             <label for="latitude">Latitude:</label>
//             <input id="latitude" class="coord-input" required>
//             <label for="longitude">Longitude:</label>
//             <input id="longitude" class="coord-input" required>
//             <button class="coord-submit"><i class="fa-solid fa-magnifying-glass"></i></button>
//         </div><h3>or</h3><div class="other-options"><button class="show-map">Select on map</button><button class="current-location">Use my location</button></div></div>`);
//         $('.coord-submit').on('click', () => {
//             let lat = Number($('input#latitude').val()), lng = Number($('input#longitude').val());
//             if (isNaN(lat)) {
//                 lat = 0;
//             }
//             if (isNaN(lng)) {
//                 lng = 0;
//             }
//             const coords = {
//                 "coords": [lat, lng]
//             };
//             $(contentDiv).empty();
//             $(contentDiv).append('<div class="loader"></div>');
//             custGetRestaurantsNear(coords, contentDiv);
//         });

//         $('.current-location').on('click', () => {
//             navigator.geolocation.getCurrentPosition((position) => {
//                 const coords = {"coords": [position.coords.latitude, position.coords.longitude]};

//                 $(contentDiv).empty();
//                 $(contentDiv).append('<div class="loader"></div>');
//                 custGetRestaurantsNear(coords, contentDiv);
//             });
//         });
//     });

//     $('.pending-orders').on('click', () => {
//         $(contentDiv).empty()
//         $(contentDiv).append('<div class="loader"></div>');
//         custGetPendingOrders(contentDiv);
//     })

//     $('.past-orders').on('click', () => {
//         $(contentDiv).empty()
//         $(contentDiv).append('<div class="loader"></div>');
//         custGetPastOrders(contentDiv);
//     })
// })

// const mergeDishNames = (dishNames) => {
//     let dishesArray = [];

//     for (const dishName in dishNames) {
//         dishesArray.push(`${dishNames[dishName]}&times; ${dishName}`);
//     }
//     return (dishesArray.join(', '));
// }

// const getDateTime = (date) => {
//     const dateTime = date.split('T');

//     return (dateTime);
// }

// const fillContentRestaurants = (element, data, title) => {
//     $(element).empty();
//     $(element).append(`<h1 class='section-title'>${title}</h1>`);
//     const restaurants = $('<div class="restaurants"></div>');
//     if (data.length === 0) {
//         $(restaurants).append('<p class="empty-list">No result has been found. Try another query</p>')
//     }
//     for (const restaurant of data) {
//         if (!restaurant.description) {
//             restaurant.description = "";
//         }
//         const restaurantDiv = `<a href="http://127.0.0.1:5000/c/restaurants/${restaurant.id}"><div class="restaurant" data-id=${restaurant.id}>
//             <h3 class="restaurant-name">${restaurant.name}</h3>
//             <img src="/static/images/restaurant-pics/${restaurant.image_file}" class="restaurant-img">
//             <div class="restaurant-text">
//                 <p>${restaurant.description}</p>
//                 <p class="restaurant-location"><i class="fa-solid fa-location-dot"></i>lat: ${restaurant.latitude} lng: ${restaurant.longitude}</p>
//             </div>
//         </div></a>`
//         $(restaurants).append(restaurantDiv);
//     }
//     $(element).append(restaurants);
// }

// const fillContentOrders = (element, data, title) => {
//     $(element).empty();
//     $(element).append(`<h1 class='section-title'>${title}</h1>`);
//     const orders = $('<div class="orders"></div>');
//     let repeatButton = '';

//     if (data.length === 0) {
//         $(orders).append('<p class="empty-list">No result has been found. Try another query</p>')
//     }
//     if (title === "Past Orders") {
//         repeatButton = '<button class="repeat-order">Repeat Order</button>';
//     }

//     for (const order of data) {
//         let confirmDelivered = '<button class="order-delivered">Confirm Delivery</button>';
//         if (title === "Pending Orders" && order.customer_confirm) {
//             confirmDelivered = '<p class="awaiting-driver">Waiting for driver confirmation</p>';
//         }
//         if (title === "Past Orders") {
//             confirmDelivered = '';
//         }
//         const dateTime = getDateTime(order.created_at);
//         const orderDiv = `<a href="#"><div class="order" data-id=${order.id}>
//         <div class="order-headline">
//             <h3 class="order-restaurant-name">Ordered from ${order.restaurant.name}</h3>
//             <p class="order-time">${dateTime[0]} at ${dateTime[1]}</p>
//         </div>
//         <div class="order-body">
//             <div class="order-text">
//                 <p class="order-driver-name">Delivered by ${order.driver.first_name+ ' ' + order.driver.last_name}, License Plate number: <span class="order-license-num">${order.driver.license_num}</span></p>
//                 <p class="order-dishes">${mergeDishNames(order.dish_names)}</p>
//             </div>
//             ${repeatButton}
//             ${confirmDelivered}
//         </div>
//     </div></a>`
//         $(orders).append(orderDiv);
//     }
//     $(element).append(orders);
// }

// const custGetOpenRestaurants = (element) => {
//     $.ajax({
//         url: 'http://127.0.0.1:5000/api/customer/open_restaurants',
//         success: (data, textStatus) => {
//             fillContentRestaurants(element, data, "Open Restaurants");
//         }
//     }); 
// };

// const custGetRestaurantsNear = (coords, element) => {
//     $.ajax({
//         url: 'http://127.0.0.1:5000/api/customer/restaurants_near',
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         data: JSON.stringify(coords),
//         success: (data, textStatus) => {
//             fillContentRestaurants(element, data, "Nearby Restaurants");
//         }
//     });
// };

// const custGetPendingOrders = (element) => {
//     $.ajax({
//         url: `http://127.0.0.1:5000/api/customer/pending_orders`,
//         success: (data, textStatus) => {
//             fillContentOrders(element, data, "Pending Orders");
//             $('.order-delivered').on('click', (event) => {
//                 custConfirmOrderDelivered(element, $(event.currentTarget).parent().parent().attr("data-id"));
//             })
//         }
//     });
// };

// const custConfirmOrderDelivered = (element, orderId) => {
//     $(element).empty();
//     $(element).append('<div class="loader"></div>');
//     $.ajax({
//         url: `http://127.0.0.1:5000/api/customer/confirm_delivered/${orderId}`,
//         method: "PUT",
//         success: (data, textStatus) => {
//             custGetPendingOrders(element);
//         }
//     });
// };

// const addCustomEventListener = (element, eventName, callback) => {
//     $(element).on(eventName, callback);
// }

// const custGetPastOrders = (element) => {
//     $.ajax({
//         url: `http://127.0.0.1:5000/api/customer/past_orders`,
//         success: (data, textStatus) => {
//             fillContentOrders(element, data, 'Past Orders');
//             $('.repeat-order').on('click', (event) => {
//                 $(event.currentTarget).parent().parent().append(`<div class="nearby-select"><div class="coord-form">
//                 <label for="latitude">Latitude:</label>
//                 <input id="latitude" class="coord-input" required>
//                 <label for="longitude">Longitude:</label>
//                 <input id="longitude" class="coord-input" required>
//                 <button class="coord-submit">Submit</button>
//             </div><h3>or</h3><div class="other-options"><button class="current-location">Use my location</button></div><button class="cancel-repeat">Cancel</button></div>`);
//                 $(event.currentTarget).remove()
//                 $('.cancel-repeat').on('click', (event) => {
//                     $(element).empty();
//                     $(element).append('<div class="loader"></div>');
//                     custGetPastOrders(element);
//                 })
//             })
//         }
//     });
});

const ownerGetRestaurantDetails = (element, restaurantId, popUp) => {
    $.ajax({
        url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}`,
        success: (data, textStatus) => {
            $(element).empty();
            const restaurantIntro = `<div class="intro">
                <h1>${data.name}</h1>
                <button class="edit-restaurant"><i class="fa-solid fa-pen"></i> Edit</button>
            </div>`;
            const restaurantDesc = `<div class="description">
                <img src="/static/images/restaurant-pics/${data.image_file}" class="restaurant-img">
                <p>${data.description || ''}</p>
                <p><i class="fa-solid fa-location-dot"></i> Lat: ${data.latitude} Lng: ${data.longitude}</p>
            </div>`;
            const restaurantDishes = `<div class="dishes-section">
                <div class="dishes-intro">
                    <h2>Dishes</h2>
                    <button class="new-dish"><i class="fa-solid fa-plus"></i> New</button>
                </div>
                <div class="dishes">
                </div>
            </div>`
            for (const dish of data.dishes) {
                $($(restaurantDishes).find('.dishes')).append(`<div class="dish" data-id=${dish.id}>
                    <div class="dish-main">
                        <div class="dish-intro">
                            <img src="/static/images/dish-pics/${dish.image_file}">
                            <h3>${dish.name}</h3>
                        </div>
                        <span class="dish-price">${dish.price}</span>
                        <a class="edit-dish" href="http://127.0.0.1:5000/o/dish/${dish.id}"><i class="fa-solid fa-pen"> Edit</a>
                    </div>
                    <div class="dish-desc">
                        <p>${dish.description || ''}</p>
                        <p>${dish.ingredients}</p>
                    </div>
                </div>`)
            }
            $(element).append(restaurantIntro);
            $(element).append(restaurantDesc);
            $(element).append(restaurantDishes);

            $('.edit-restaurant').on('click', () => {
                const forms = $(popUp);
                const editRestaurantForm = $(forms).children('div.popup-edit-restaurant');

                console.log($(popUp).html())
                $($(element).find('.popup-cont')).remove();
                $(element).html(popUp + $(element).html());
                $('.popup-edit-restaurant').css('visibility', 'visible');
                $('.cancel').on('click', () => {
                    $('.popup-edit-restaurant').css('visibility', 'hidden');
                });
                // console.log($(forms).html())
            //     console.log(editRestaurantForm)
                // $(element).append($(editRestaurantForm));
            })

            $('.new-dish').on('click', () => {
                const forms = $(popUp);
                const newDishForm = $(forms).children('div.popup-new-dish');

                console.log($(newDishForm).html());
                $($(element).find('.popup-cont')).remove();
                $(element).html(popUp + $(element).html());
                $('.popup-new-dish').css('visibility', 'visible');
                $('.cancel').on('click', () => {
                    $('.popup-new-dish').css('visibility', 'hidden');
                })
                // console.log($(forms).html())
            //     console.log(editRestaurantForm)
                // $(element).append($(editRestaurantForm));
            })
        }
    });
};