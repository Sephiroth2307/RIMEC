$(document).ready(function() {
    function formatearPrecio(valor) {
        // Asegúrate de que la conversión de número a cadena maneje bien los miles
        return valor.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    }

    function actualizarTotalCarrito() {
        let total = 0;
        // Usa 'data-subtotal' para obtener el valor del subtotal de cada producto
        $('td[data-subtotal]').each(function() {
            total += parseFloat($(this).data('subtotal'));
        });
        // Actualiza el total con el formato correcto
        $('#total').text('Gs. ' + formatearPrecio(total));
    }

    $('.btn-eliminar').on('click', function() {
        var productoId = $(this).data('producto-id');
        $.ajax({
            type: 'POST',
            url: '/eliminar/' + productoId,
            success: function(response) {
                if(response.success) {
                    // Elimina la fila del producto del DOM
                    $('button[data-producto-id="' + productoId + '"]').closest('tr').remove();
                    // Actualiza el total del carrito después de eliminar un producto
                    actualizarTotalCarrito();
                } else {
                    alert('Hubo un error al eliminar el producto.');
                }
            },
            error: function() {
                alert('Error al comunicarse con el servidor.');
            }
        });
    });

    $('.quantity-input').on('change', function() {
        var productoId = $(this).data('producto-id');
        var nuevaCantidad = $(this).val();
        var precio = $(this).closest('tr').find('td[data-precio]').data('precio');
        
        // Actualiza el subtotal en la fila del producto
        var nuevoSubtotal = nuevaCantidad * precio;
        $(this).closest('tr').find('td[data-subtotal]').data('subtotal', nuevoSubtotal).text('Gs. ' + formatearPrecio(nuevoSubtotal));
        
        // Actualiza el total del carrito después de cambiar la cantidad de un producto
        actualizarTotalCarrito();
    });

    // Inicializa el total del carrito en la carga inicial
    actualizarTotalCarrito();
});