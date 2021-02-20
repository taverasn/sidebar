let year;

const yearEl = document.getElementById('year');

init()

function init() {
    year = new Date().getFullYear();
    yearEl.innerText = year
}