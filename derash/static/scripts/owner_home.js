$(document).ready(() => {
    const restaurantsDiv = $('.owner-restaurants');
    const popUp = $('.popup-new-restaurant')
    $(restaurantsDiv).append('<div class="loader"></div>');
    
    ownerGetMyRestaurants(restaurantsDiv);
    $('.add-restaurant').on('click', () => {
        $('.popup-cont').empty();
        $(popUp).append(`<h2>New Restaurant</h2>
        <form></form>`)
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
                    let activate = '<button class="activate">Activate</button>';
                    let deactivate = '<button class="deactivate">Deactivate</button>';

                    if (restaurant.open) {
                        activate = '';
                    } else {
                        deactivate = '';
                    }
                    const restaurantDiv = $(`<a href="http://127.0.0.1:5000/o/restaurants/${restaurant.id}"><div class="restaurant">
                        <div class="restaurant-headline">
                            <h2 class="restaurant-name">${restaurant.name}</h2>
                            <div>
                                <span>Inactive</span>
                                ${activate}
                                ${deactivate}    
                            </div>
                        </div>
                        <p>${restaurant.description || ""}</p>
                    </div></a>`)

                    if (restaurant.open) {
                        $(restaurantDiv).find('span').addClass('active');
                        $(restaurantDiv).find('span').html('Active');
                    }

                    $(element).append(restaurantDiv);
                }
            }
        }
    });
};