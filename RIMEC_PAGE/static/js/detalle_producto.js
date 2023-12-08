function mostrarCantidad() {
    // Obtiene el índice de la opción seleccionada
    var selectedIndex = document.getElementById("talla-selector").selectedIndex;
    // Obtiene la lista de cantidades disponibles para cada talla
    var cantidades = JSON.parse(document.getElementById("talla-selector").getAttribute("data-cantidades"));
    // Actualiza el texto con la cantidad disponible para la talla seleccionada
    document.getElementById("cantidadDisplay").innerText = cantidades[selectedIndex];
}

document.addEventListener('DOMContentLoaded', function () {
    const relatedProducts = document.querySelector('.related-products');
    const mainProductImg = document.querySelector('.main-product img');

    // Ocultar el producto relacionado que coincida con la imagen principal
    const relatedImgs = relatedProducts.querySelectorAll('img');
    for (let img of relatedImgs) {
        if (img.src === mainProductImg.src) {
            img.parentElement.style.display = 'none';
        }
    }

    relatedProducts.addEventListener('click', function (e) {
        if (e.target.tagName === 'IMG') {
            // Mostrar la imagen que estaba oculta anteriormente
            const hiddenProduct = relatedProducts.querySelector('a[style="display: none;"]');
            if (hiddenProduct) {
                hiddenProduct.style.display = 'block';
            }

            // Ocultar el producto que ahora es la imagen principal
            setTimeout(() => {
                for (let img of relatedImgs) {
                    if (img.src === mainProductImg.src) {
                        img.parentElement.style.display = 'none';
                    } else {
                        img.parentElement.style.display = 'block';
                    }
                }
            }, 100);
        }
    });
});

$(document).ready(function() {
    $('#talla-selector').change(mostrarCantidad);
    $('#add-to-cart-button').click(function() {
        var productoId = $('#producto-id').val();
        var tallaSeleccionada = $('#talla-selector').val();
        var cantidadSolicitada = parseInt($('#cantidad').val(), 10);

        if(!tallaSeleccionada) {
            alert('Por favor, selecciona una talla.');
            return;
        }
        if(isNaN(cantidadSolicitada) || cantidadSolicitada < 1) {
            alert('Por favor, introduce una cantidad válida.');
            return;
        }

        var dataToSend = {
            producto_id: productoId,
            talla: tallaSeleccionada,
            cantidad: cantidadSolicitada
        };

        $.ajax({
            type: 'POST',
            url: '/add_to_cart',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(dataToSend),
            success: function(response) {
                // Reemplaza el alert por notificación personalizada
                $('#cart-notification').fadeIn(500).delay(3000).fadeOut(500);
                // Actualiza la información del producto en la notificación
                $('.cart-product-name').text($('#producto-nombre').val());
                $('.cart-product-price').text('Gs.' + $('#producto-precio').val());
            },
            error: function(response) {
                alert('Error: ' + response.responseJSON.error);
            }
        });
    });
});