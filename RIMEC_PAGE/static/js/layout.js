document.addEventListener('DOMContentLoaded', function() {
    var addToCartButtons = document.querySelectorAll('.btn-anadir');
    addToCartButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            var productId = this.dataset.productId;
            addToCart(productId);
        });
    });
});

function addToCart(productId) {
    fetch('/add_to_cart', {
        method: 'POST',
        body: JSON.stringify({
            // Datos a enviar
            'ID_ARTICULO': productId
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Suponiendo que la respuesta incluya la nueva cantidad para el contador del carrito
        updateCartCount(data.new_cart_count);
    })
    .catch(error => console.error('Error:', error));
}

function updateCartCount(newCount) {
    document.querySelector('#carrito-count').textContent = newCount;
}