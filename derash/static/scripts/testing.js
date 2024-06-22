$(document).ready(() => {
    // Customers
    const custGetDetails = () => {
        $.ajax({
            url: 'http://127.0.0.1:5000/api/customer',
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    }
    // custGetDetails();

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
                console.log(data);
            }
        })
    };
    // custGetOrderDetails("8c23e934-83da-4de6-b46b-16469599f6261b1d8093-cb2b-4660-ad2b-47553a9e8181");
    // custGetOrderDetails("1b6c4ee8-a19b-4357-b86d-7ad431ceb0e36c68378a-e0b3-46e3-a899-04284b9df1f6");

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

    const custRepeatOrder = (orderId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/customer/orders/${orderId}`,
            success: (data, textStatus) => {
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
            }
        });
    };
    // custRepeatOrder("f9ae688f-e5a5-4902-bdaf-f085c9cbae847904798b-2f77-41b5-a274-925ae08ee65c");



    // Owners
    const ownerGetDetails = () => {
        $.ajax({
            url: 'http://127.0.0.1:5000/api/owner',
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    }
    // ownerGetDetails();

    const ownerGetMyRestaurants = () => {
        $.ajax({
            url: 'http://127.0.0.1:5000/api/owner/my_restaurants',
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // ownerGetMyRestaurants();

    const ownerGetRestaurantDetails = (restaurantId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}`,
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // ownerGetRestaurantDetails("503f2d53-82aa-4bdf-9812-16a9db999ef47c14963d-fa31-4c06-bd58-76f56458cbec");

    const ownerGetRestaurantReviews = (restaurantId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}/reviews`,
            success: (data, textStatus) => {
                console.log(data);
            }
        });    
    };
    // ownerGetRestaurantReviews("503f2d53-82aa-4bdf-9812-16a9db999ef47c14963d-fa31-4c06-bd58-76f56458cbec");

    const ownerOpenRestaurant = (restaurantId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}/open`,
            method: "PUT",
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // ownerOpenRestaurant("503f2d53-82aa-4bdf-9812-16a9db999ef47c14963d-fa31-4c06-bd58-76f56458cbec");

    const ownerCloseRestaurant = (restaurantId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}/close`,
            method: "PUT",
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // ownerCloseRestaurant("503f2d53-82aa-4bdf-9812-16a9db999ef47c14963d-fa31-4c06-bd58-76f56458cbec");

    const ownerGetMonthlyReceipt = (restaurantId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}/monthly`,
            method: "GET",
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // ownerGetMonthlyReceipt("503f2d53-82aa-4bdf-9812-16a9db999ef47c14963d-fa31-4c06-bd58-76f56458cbec");

    const ownerGetPastMonthReceipt = (restaurantId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}/past_month`,
            method: "GET",
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    ownerGetPastMonthReceipt("503f2d53-82aa-4bdf-9812-16a9db999ef47c14963d-fa31-4c06-bd58-76f56458cbec");

    const ownerGetAllRestaurantOrders = (restaurantId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}/all_orders`,
            method: "GET",
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // ownerGetAllRestaurantOrders("503f2d53-82aa-4bdf-9812-16a9db999ef47c14963d-fa31-4c06-bd58-76f56458cbec");

    const ownerGetPastRestaurantOrders = (restaurantId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}/past_orders`,
            method: "GET",
            success: (data, textStatus) => {
                console.log(data);
            }
        });  
    };
    // ownerGetPastRestaurantOrders("503f2d53-82aa-4bdf-9812-16a9db999ef47c14963d-fa31-4c06-bd58-76f56458cbec");

    const ownerGetPendingRestaurantOrders = (restaurantId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}/pending_orders`,
            method: "GET",
            success: (data, textStatus) => {
                console.log(data);
            }
        });  
    };
    // ownerGetPendingRestaurantOrders("503f2d53-82aa-4bdf-9812-16a9db999ef47c14963d-fa31-4c06-bd58-76f56458cbec");

    const ownerGetOrderDetails = (orderId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/owner/my_orders/${orderId}`,
            method: "GET",
            success: (data, textStatus) => {
                console.log(data);
            }
        }); 
    };
    // ownerGetOrderDetails("03e14db8-197e-4c9b-93eb-20bffe8a17241194f80d-f28a-4f8e-b38a-e3c6b6df9031");

    const ownerConfirmOrderMade = (orderId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/owner/my_orders/${orderId}/done`,
            method: "PUT",
            success: (data, textStatus) => {
                console.log(data);
            }
        }); 
    };
    // ownerConfirmOrderMade("03e14db8-197e-4c9b-93eb-20bffe8a17241194f80d-f28a-4f8e-b38a-e3c6b6df9031");

    

    // Driver
    const driverGetDetails = () => {
        $.ajax({
            url: 'http://127.0.0.1:5000/api/driver',
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    }
    // driverGetDetails();

    const driverGetAllDeliveries = () => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/driver/all_deliveries`,
            method: "GET",
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // driverGetAllDeliveries();

    const driverGetPastDeliveries = () => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/driver/past_deliveries`,
            method: "GET",
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // driverGetPastDeliveries();

    const driverActivate = () => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/driver/activate`,
            method: "PUT",
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // driverActivate();

    const driverDeactivate = () => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/driver/deactivate`,
            method: "PUT",
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // driverDeactivate();

    const driverGetPossibleDeliveries = () => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/driver/possible_deliveries`,
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify({
                "coords": [47.7272, 96.8460]
            }),
            success: (data, textStatus) => {
                console.log(data);
            }
        });   
    }
    // driverGetPossibleDeliveries();

    const driverAcceptDelivery = (orderId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/driver/${orderId}/accept`,
            method: "PUT",
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // driverAcceptDelivery("ef2cea46-8922-4218-8aab-71d9f9551cc4ab0df35d-5202-458b-a598-918ff0170700");

    const driverCurrentDelivery = (orderId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/driver/current_delivery`,
            method: "GET",
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // driverCurrentDelivery();

    const driverConfirmDelivery = (orderId) => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/driver/${orderId}/delivered`,
            method: "PUT",
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // driverConfirmDelivery("035e08a6-7a73-4ce9-8e62-9829b3811b13e70fb4ec-e192-4808-8c7b-19717d5d02f7");

    const driverGetMonthlyReceipt = () => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/driver/monthly`,
            method: "GET",
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // driverGetMonthlyReceipt();

    const driverGetPastMonthReceipt = () => {
        $.ajax({
            url: `http://127.0.0.1:5000/api/driver/past_month`,
            method: "GET",
            success: (data, textStatus) => {
                console.log(data);
            }
        });
    };
    // driverGetPastMonthReceipt();
});
