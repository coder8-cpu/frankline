// let designBtn = document.getElementById('designBtn');
// let designDiv = document.getElementById('design');
// let performanceBtn = document.getElementById('performanceBtn');
// let performanceDiv = document.getElementById('performance');
// let durabilityBtn = document.getElementById('durabilityBtn');
// let durabilityDiv = document.getElementById('durability');
// let designExp = document.getElementById('design-explaination');


// designBtn.addEventListener("click", () => {
//     designBtn.style.color = "#ff7900"
//     designDiv.style.display = "block"
//     designExp.style.alignSelf = "center"
//     performanceDiv.style.display = "none"
//     performanceBtn.style.color = "#2a2a2a"
//     durabilityBtn.style.color = "#2a2a2a"
//     durabilityDiv.style.display = "none"
// })

// performanceBtn.addEventListener("click", () => {
//     performanceBtn.style.color = "#ff7900"
//     designDiv.style.display = "none"
//     durabilityDiv.style.display = "none"
//     durabilityBtn.style.color = "#2a2a2a"
//     performanceDiv.style.display = "block"
//     designBtn.style.color = "#2a2a2a"
// })

// durabilityBtn.addEventListener("click", () => {
//     durabilityBtn.style.color = "#ff7900"
//     performanceBtn.style.color = "#2a2a2a"
//     designBtn.style.color = "#2a2a2a"
//     durabilityDiv.style.display = "block"
//     designDiv.style.display = "none"
//     performanceDiv.style.display = "none"
// })

// scroll function{
    window.addEventListener("scroll",() => {
        var navBar = document.getElementById("navBarBG");
        navBar.classList.toggle("sticky", window.scrollY > 0);
        navBar.classList.toggle("navBarFixed", window.scrollY > 80)
    })
// let toggleBtn = document.getElementById("togglerBtn");
// let hamburger = document.getElementById("hamburger");
// let tabNav = document.getElementById("medium-devices-navBar");
// toggleBtn.onclick = () => {
//     tabNav.classList.toggle("medium-Navbar");
// }

window.addEventListener("scroll", () => {
    let smNav = document.getElementById("nv-sm");
    smNav.classList.toggle("sticky", window.scrollY > 0);
    smNav.classList.toggle("navBarFixed", window.scrollY > 80);
} )


// cards

// var container = document.getElementById('container')
// var slider = document.getElementById('slider');
// var slides = document.getElementsByClassName('slide').length;
// var buttons = document.getElementsByClassName('btn');


// var currentPosition = 0;
// var currentMargin = 0;
// var slidesPerPage = 0;
// var slidesCount = slides - slidesPerPage;
// var containerWidth = container.offsetWidth;
// var prevKeyActive = false;
// var nextKeyActive = true;

// window.addEventListener("resize", checkWidth);

// function checkWidth() {
//     containerWidth = container.offsetWidth;
//     setParams(containerWidth);
// }

// function setParams(w) {
//     if (w < 551) {
//         slidesPerPage = 1;
//     } else {
//         if (w < 901) {
//             slidesPerPage = 2;
//         } else {
//             if (w < 1101) {
//                 slidesPerPage = 3;
//             } else {
//                 slidesPerPage = 4;
//             }
//         }
//     }
//     slidesCount = slides - slidesPerPage;
//     if (currentPosition > slidesCount) {
//         currentPosition -= slidesPerPage;
//     };
//     currentMargin = - currentPosition * (100 / slidesPerPage);
//     slider.style.marginLeft = currentMargin + '%';
//     if (currentPosition > 0) {
//         buttons[0].classList.remove('inactive');
//     }
//     if (currentPosition < slidesCount) {
//         buttons[1].classList.remove('inactive');
//     }
//     if (currentPosition >= slidesCount) {
//         buttons[1].classList.add('inactive');
//     }
// }

// setParams();

// function slideRight() {
//     if (currentPosition != 0) {
//         slider.style.marginLeft = currentMargin + (100 / slidesPerPage) + '%';
//         currentMargin += (100 / slidesPerPage);
//         currentPosition--;
//     };
//     if (currentPosition === 0) {
//         buttons[0].classList.add('inactive');
//     }
//     if (currentPosition < slidesCount) {
//         buttons[1].classList.remove('inactive');
//     }
// };

// function slideLeft() {
//     if (currentPosition != slidesCount) {
//         slider.style.marginLeft = currentMargin - (100 / slidesPerPage) + '%';
//         currentMargin -= (100 / slidesPerPage);
//         currentPosition++;
//     };
//     if (currentPosition == slidesCount) {
//         buttons[1].classList.add('inactive');
//     }
//     if (currentPosition > 0) {
//         buttons[0].classList.remove('inactive');
//     }
// };

// sv carousel


// popup
// var delay = 12000; //in milleseconds

// jQuery(document).ready(function($){
//   setTimeout(function(){ showNewsletterPopup(); }, delay);
  
//   $('.popup-close').click(function(){
//       $('.newsletter-overlay').hide();
      
//       //when closed create a cookie to prevent popup to show again on refresh
//       setCookie('newsletter-popup', 'popped', 30);
//   });
// });

// function showNewsletterPopup(){
//   if( getCookie('newsletter-popup') == ""){
//      $('.newsletter-overlay').show();
//      setCookie('newsletter-popup', 'popped', 30);
//   }
//   else{
//     console.log("Newsletter popup blocked.");
//   }
// }


// function setCookie(cname,cvalue,exdays)
// {
//     var d = new Date();
//     d.setTime(d.getTime()+(exdays*24*60*60*1000));
//     var expires = "expires="+d.toGMTString();
//     document.cookie = cname+"="+cvalue+"; "+expires+"; path=/";
// }

// function getCookie(cname)
// {
//     var name = cname + "=";
//     var ca = document.cookie.split(';');
//     for(var i=0; i<ca.length; i++) 
//     {
//         var c = jQuery.trim(ca[i]);
//         if (c.indexOf(name)==0) return c.substring(name.length,c.length);
//     }
//     return "";
// }

// function newsletter(){
//     let newsSubscriber = document.getElementById("email-news");
//     let subscribeBtn = document.getElementById("news-submit");
//     let subscriber = newsSubscriber.value;
//     newsSubscriber.value = "";
//     // console.log(subscriber);
// }

// small devices navBar

// let ham = document.getElementById("togglerBtn");
// function menu() {
//     let svMenu = document.getElementById("sm-nav");
//     svMenu.classList.toggle('nothing');
//     console.log('nothing');
// }

