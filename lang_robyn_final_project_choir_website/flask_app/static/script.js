
var blink_speed = 3000; // every 1000 == 1 second, adjust to suit
var t = setInterval(function () {
    var ele = document.getElementById('myBlinkingDiv');
    ele.style.visibility = (ele.style.visibility == 'hidden' ? '' : 'hidden');
}, blink_speed);

function changeColor(element) {
    element.style.backgroundColor = "rgb(196, 6, 196)";
}

function changeBack(element) {
    element.style.backgroundColor = "black";
}

function changeColor2(element) {
    element.style.color = "blue";
}

function changeBack2(element) {
    element.style.color = "white";
}