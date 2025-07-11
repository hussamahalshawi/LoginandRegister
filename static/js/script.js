const cover_box = document.querySelector('.cover_box');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');


function activateCoverBox() {
    cover_box.classList.add('active');
}
function deactivateCoverBox() {
    cover_box.classList.remove('active');
}
function activatePopup() {
    cover_box.classList.add('active-popup');
}
function deactivatePopup() {
    cover_box.classList.remove('active-popup');
}
registerLink.addEventListener('click', activateCoverBox);
loginLink.addEventListener('click', deactivateCoverBox);
btnPopup.addEventListener('click', activatePopup);
iconClose.addEventListener('click', deactivatePopup);
