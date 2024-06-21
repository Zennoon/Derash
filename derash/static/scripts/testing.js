$(document).ready(() => {
    const custGetAllRestaurants = () => {
        $.ajax({
            url: 'http://127.0.0.1:5000/api/customer/all_restaurants',
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    }
    // custGetAllRestaurants();

    const custGetOpenRestaurants = () => {
        $.ajax({
            url: 'http://127.0.0.1:5000/api/customer/open_restaurants',
            success: (data, textStatus) => {
                console.log(data);
            }
        })  ; 
    };
    // custGetOpenRestaurants();

    const custGetRestaurantsNear = () => {
        $.ajax({
            url: 'http://127.0.0.1:5000/api/customer/restaurants_near',
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify({
                "coords": [24.402, 114.55]
            }),
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // custGetRestaurantsNear();

    const custGetRestaurantDetails = (restaurantId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/customer/restaurants/${restaurantId}`,
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // custGetRestaurantDetails("41a93543-9853-4aab-80db-4da6bb01ce9683fae4ae-ff65-4393-81ee-0ba93d83f64d");

    const custGetRestaurantReviews = (restaurantId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/customer/restaurants/${restaurantId}/reviews`,
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // custGetRestaurantReviews("5bc0d60c-0bff-4858-89d0-d94e6586d8993981e1e6-3de9-4457-bcc7-3e2c6dca1283");

    const custGetDishDetails = (dishId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/customer/dishes/${dishId}`,
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // custGetDishDetails("1fb457a9-23a4-4294-a613-feb60f4f7db41355bb8b-9a94-480c-928b-0486f0b3ad56");

    const custGetPastOrders = () => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/customer/past_orders`,
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // custGetPastOrders();

    const custGetPendingOrders = () => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/customer/pending_orders`,
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // custGetPendingOrders();

    const custGetAllOrders = () => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/customer/all_orders`,
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // custGetAllOrders();

    const custConfirmOrderDelivered = (orderId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/customer/confirm_delivered/${orderId}`,
            method: "PUT",
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // custConfirmOrderDelivered("0578a4ac-c5f4-4c2f-b8d7-85157a652c85b5c3e06c-ef48-4d7b-b6bb-277a98cf4786");
    const custGetOrderDetails = (orderId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/customer/orders/${orderId}`,
            success: (data, textStatus) => {
                console.log(data)
            }
        })
    };
    custGetOrderDetails("8c23e934-83da-4de6-b46b-16469599f6261b1d8093-cb2b-4660-ad2b-47553a9e8181");
    custGetOrderDetails("1b6c4ee8-a19b-4357-b86d-7ad431ceb0e36c68378a-e0b3-46e3-a899-04284b9df1f6");

    const custCreateOrder = (data) => {
        $.ajax({
            url: 'http://127.0.0.1:5000/api/customer/new_order',
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify(data),
            success: (data, textStatus) => {
                console.log(data);
            }
        });   
    };
});
