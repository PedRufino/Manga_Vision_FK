var prevScrollpos = window.pageYOffset;
window.onscroll = function () {
    var menuContainer = document.getElementById("menu-vision");
    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
        menuContainer.style.top = "0";
    } else {
        menuContainer.style.top = "-110px";
    }
    prevScrollpos = currentScrollPos;
}

var footer = document.querySelector("footer");
function updateFooter() {
    var pageHeight = document.documentElement.scrollHeight;
    var windowHeight = window.innerHeight;

    if (pageHeight <= windowHeight) {
        footer.style.position = "fixed";
        footer.style.bottom = "0";
        footer.style.width = "100%";
    } else {
        footer.style.bottom = "0";
        footer.style.width = "100%";
    }
}

updateFooter();

window.addEventListener("resize", updateFooter);

document.getElementById('myTextarea').addEventListener('input', function () {
    // Obtenha o valor do textarea
    var text = this.value;

    // Armazene o valor no armazenamento local do navegador
    localStorage.setItem('text', text);
});

window.addEventListener('beforeunload', function () {
    // Obtenha o valor do textarea
    var text = document.getElementById('myTextarea').value;

    // Armazene o valor no armazenamento local do navegador
    localStorage.setItem('text', text);
});

window.addEventListener('load', function () {
    // Obtenha o valor armazenado no armazenamento local do navegador
    var text = localStorage.getItem('text');

    // Exiba o valor no textarea
    document.getElementById('myTextarea').value = text;
});