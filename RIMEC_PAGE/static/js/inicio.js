// (document).ready(function(){
   // $('.slider').slick({
     //   infinite: true,
       // slidesToShow: 3, // Imágenes a mostrar
        //slidesToScroll: 1,
        // autoplay: true, // Reproducción automática
        // autoplaySpeed: 2000, // Tiempo en milisegundos owO
    // });
// });

$(document).ready(function(){
    $('.slider').slick({
        infinite: true, // Movimiento infinito
        slidesToShow: 3, // Cantidad de Slides
        slidesToScroll: 0.7,
        autoplay: true, // Reproducción automática
        autoplaySpeed: 0, // Reproducción continua sin demora
        speed: 5000, // Velocidad de deslizamiento (5000ms para que se vea mas piola pe)
        cssEase: 'linear' // Transición lineal para un movimiento constante
    });
});