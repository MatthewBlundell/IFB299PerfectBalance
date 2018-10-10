'use strict';

// document ready function
$(function(){
    
    // global configurations
    var width = 1750;
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
            if(currentSlide === $slides.length + 1){
                currentSlide = 1;
                $slideContainer.css('margin-left', 0);
            }
        });
    }, pause);

    // going to start coding for login form only appeariong once login button has been pressed

    //setting up global variable and configs

    var arrow = $(".arrow");
    var form = $(".login-form");
    var status =  false;
    var disable = $(".wrapper");
    
    $(".submit").click(function(event){
        event.preventDefault();
        if(status == false){
            arrow.fadeIn();
            form.fadeIn();
            form.css({'z-index': '3', 'opacity': '1'});
            disable.css({'z-index': '2', 'opacity': '0.6'});           
            status = true;
        }
        else{
            arrow.fadeOut();
            form.fadeOut();
            form.css({'z-index': '0', 'opacity': '1'});
            disable.css({'z-index': '0', 'opacity': '0'}); 
            status = false;
        }
    })

    $(".loginbtn").click(function(event){
        event.preventDefault();
        if(status == false){
            arrow.fadeIn();
            form.fadeIn();
            form.css({'z-index': '3', 'opacity': '1'});
            disable.css({'z-index': '2', 'opacity': '0.6'});           
            status = true;
        }
        else{
            arrow.fadeOut();
            form.fadeOut();
            form.css({'z-index': '0', 'opacity': '1'});
            disable.css({'z-index': '0', 'opacity': '0'}); 
            status = false;
        }
    })
});

function toggleSidebar(){
    document.getElementById('sidebar').classList.toggle('active');
}