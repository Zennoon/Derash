$(document).ready(() => {
    const restaurantsDiv = $('.owner-restaurants');
    const popUp = $('.popup-new-restaurant')
    $(restaurantsDiv).append('<div class="loader"></div>');
    
    ownerGetMyRestaurants(restaurantsDiv);
    $('.add-restaurant').on('click', () => {
        $(popUp).css('visibility', 'visible');
        $('i.cancel').on('click', () => {
            $(popUp).css('visibility', 'hidden');
        })
    })
})

const ownerGetMyRestaurants = (element) => {
    $.ajax({
        url: 'http://127.0.0.1:5000/api/owner/my_restaurants',
        success: (data, textStatus) => {
            $(element).empty();

            if (data.length === 0) {
                $(element).append(`<p>No results</p>`);
            } else {
                for (const restaurant of data) {
                    let activate = `<button class="activate" data-id=${restaurant.id}>Activate</button>`;
                    let deactivate = `<button class="deactivate" data-id=${restaurant.id}>Deactivate</button>`;

                    if (restaurant.is_open) {
                        activate = '';
                    } else {
                        deactivate = '';
                    }
                    const restaurantDiv = $(`<div class="owner-restaurant" data-id="${restaurant.id}">
                        <div class="restaurant-headline">
                            <img src="/static/images/restaurant-pics/${restaurant.image_file}" class="restaurant-img">
                            <a href="http://127.0.0.1:5000/o/restaurants/${restaurant.id}"><h2 class="restaurant-name">${restaurant.name}</h2></a>
                            <div>
                                <span></span>
                                ${activate}
                                ${deactivate}    
                            </div>
                        </div>
                        <p class="restaurant-description">${restaurant.description || ""}</p>
                    </div>`)

                    if (restaurant.is_open) {
                        $(restaurantDiv).find('span').addClass('active');
                    }

                    $(element).append(restaurantDiv);
                }
            }
            $('.activate').on('click', (event) => {
                console.log($(event.currentTarget).attr('data-id'));
                ownerOpenRestaurant($(event.currentTarget).attr('data-id'), element);
            })

            $('.deactivate').on('click', (event) => {
                console.log($(event.currentTarget).attr('data-id'));
                ownerCloseRestaurant($(event.currentTarget).attr('data-id'), element);
            })
        }
    });
};

const ownerOpenRestaurant = (restaurantId, element) => {
    $.ajax({
        url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}/open`,
        method: "PUT",
        success: () => {
            ownerGetMyRestaurants(element);
        }
    });
};

const ownerCloseRestaurant = (restaurantId, element) => {
    $.ajax({
        url: `http://127.0.0.1:5000/api/owner/my_restaurants/${restaurantId}/close`,
        method: "PUT",
        success: () => {
            ownerGetMyRestaurants(element);
        }
    });
};