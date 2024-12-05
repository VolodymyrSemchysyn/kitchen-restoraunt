"use strict";

document.addEventListener("DOMContentLoaded", function() {

  var fullHeight = function() {
    var elements = document.querySelectorAll('.js-fullheight');
    var windowHeight = window.innerHeight;

    elements.forEach(function(element) {
      element.style.height = windowHeight + 'px';
    });

    window.addEventListener('resize', function() {
      elements.forEach(function(element) {
        element.style.height = windowHeight + 'px';
      });
    });
  };

  fullHeight();

  var togglePassword = function() {
    var toggleButtons = document.querySelectorAll(".toggle-password");

    toggleButtons.forEach(function(button) {
      button.addEventListener("click", function() {
        button.classList.toggle("fa-eye");
        button.classList.toggle("fa-eye-slash");

        var input = document.querySelector(button.getAttribute("toggle"));

        if (input.getAttribute("type") === "password") {
          input.setAttribute("type", "text");
        } else {
          input.setAttribute("type", "password");
        }
      });
    });
  };

  togglePassword();

});
