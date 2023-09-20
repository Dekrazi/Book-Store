document.addEventListener('DOMContentLoaded', function() {
    var updateBtns = document.getElementsByClassName('update-cart');
    console.log(updateBtns); // Check if elements are selected

    for (var i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function () {
            var productId = this.dataset.product;
            var action = this.dataset.action;
            console.log('productId:', productId, 'Action:', action);

            if (user === 'AnonymousUser') {
                console.log('Not logged in');
            } else {
                updateUserOrder(productId, action);
            }
        });
    }
});

function updateUserOrder(productId, action) {
    console.log('User is logged in, sending data...');

    var url = '/update_item/';
    var data = {
        'productId': productId,
        'action': action
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((data) => {
        console.log('Received data:', data);
        location.reload();

        var addButton = document.getElementById(`add-to-cart-${productId}`);
        var removeButton = document.getElementById(`remove-from-cart-${productId}`);
        if (action === 'add') {
            addButton.classList.add('d-none');
            removeButton.classList.remove('d-none');
        } else if (action === 'remove') {
            addButton.classList.remove('d-none');
            removeButton.classList.add('d-none');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}