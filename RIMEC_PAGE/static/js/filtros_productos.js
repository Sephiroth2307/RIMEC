$(document).ready(function() {
    function filtrarProductos() {
        var marcasSeleccionadas = $('input.marca-filter:checked').map(function() { return $(this).val(); }).get();
        var coloresSeleccionados = $('input.color-filter:checked').map(function() { return $(this).val(); }).get();

        $('.product-card').each(function() {
            var marcaProducto = $(this).data('marca');
            var colorProducto = $(this).data('color');
            var mostrarPorMarca = marcasSeleccionadas.length === 0 || marcasSeleccionadas.includes(marcaProducto);
            var mostrarPorColor = coloresSeleccionados.length === 0 || coloresSeleccionados.includes(colorProducto);

            if (mostrarPorMarca && mostrarPorColor) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }

    $('input.marca-filter, input.color-filter').on('change', filtrarProductos);

    // Aplicar filtros inicialmente
    filtrarProductos();
});