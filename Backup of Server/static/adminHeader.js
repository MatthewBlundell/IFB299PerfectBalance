'use strict';

  var arrow;
  var loginform;
  var activestatus;
  var disable;
  var temp;
  var badlogin;
// document ready function
$(function(){
	
    // going to start coding for login form only appeariong once login button has been pressed

    //setting up global variable and configs
	arrow = $(".arrow");
    loginform = $(".login-form");

	activestatus =  false;
	if (badlogin == true) {
		activestatus = true;
		badlogin = false;
	}
    disable = $(".wrapper");

    $(".loginbtn").click(function(event){
        event.preventDefault();
        if(activestatus == false){
            arrow.fadeIn();
            loginform.fadeIn();
            loginform.css({'z-index': '3', 'opacity': '1'});
            disable.css({'z-index': '2', 'opacity': '0'});           
            activestatus = true;
        }
        else{
            arrow.fadeOut();
            loginform.fadeOut();
            loginform.css({'z-index': '1', 'opacity': '1'});
            disable.css({'z-index': '0', 'opacity': '0'}); 
            activestatus = false;
        }
    })
	
});


function BadLogin() {
	arrow = $(".arrow");
    loginform = $(".login-form");
    disable = $(".wrapper");
	arrow.fadeIn();
	loginform.fadeIn();
	loginform.css({'z-index': '3', 'opacity': '1'});
	disable.css({'z-index': '2', 'opacity': '0.6'});           
	badlogin = true;
}