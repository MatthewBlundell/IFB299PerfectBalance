'use strict';

// document ready function
$(function(){
    
    // global configurations
    var width = 1280;
    var animationSpeed = 1000;
    var pause = 5000;
    var currentSlide = 1;

    // cache the DOM
    var $slider = $('#slider');
    var $slideContainer = $slider.find('.slides');
    var $slides = $slideContainer.find('.slide');

    //setInterval for image slider
    setInterval(function(){
        //animate the images by animating margin-left
        $slideContainer.animate({'margin-left': '-=' + width}, animationSpeed, function(){
            //if the slides reach last slide then go back to beginning
            currentSlide++;
            console.log(currentSlide);
            if(currentSlide === $slides.length){
                currentSlide = 1;
                $slideContainer.css('margin-left', 0);
            }
        });
    }, pause);
});

function toggleSidebar(){
    document.getElementById('sidebar').classList.toggle('active');
}