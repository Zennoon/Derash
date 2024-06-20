$(document).ready(() => {
    $.ajax({
        url: 'http://127.0.0.1:5000/api/restaurants/nearme',
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        data: JSON.stringify({
            "coords": [60.9949, 71.88]
        }),
        success: (data, textStatus) => {
            console.log(data);
        }
    })
})