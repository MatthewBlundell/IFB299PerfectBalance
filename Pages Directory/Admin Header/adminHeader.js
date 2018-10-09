'use strict';

// document ready function
$(function(){

    // going to start coding for login form only appeariong once login button has been pressed

    //setting up global variable and configs

    var arrow = $(".arrow");
    var form = $(".login-form");
    var status =  false;
    var disable = $(".wrapper");
    

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