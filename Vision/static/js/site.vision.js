document.addEventListener("DOMContentLoaded", function () {
    var prevScrollpos = window.pageYOffset; // Define a variável prevScrollpos aqui

    window.onscroll = function () {
        var menuContainer = document.getElementById("menu-vision");
        var btnVoltarAoTopo = document.getElementById("btnVoltarAoTopo");
        var currentScrollPos = window.pageYOffset;

        // Controla o comportamento do menu de navegação
        if (prevScrollpos > currentScrollPos) {
            menuContainer.style.top = "0";
        } else {
            menuContainer.style.top = "-110px";
        }
        prevScrollpos = currentScrollPos;

        // console.log("Evento onscroll chamado");
        // console.log("Valor de document.body.scrollTop: " + document.body.scrollTop);
        // console.log("Valor de document.documentElement.scrollTop: " + document.documentElement.scrollTop);
        // Verifica se a largura da tela é menor que 860 pixels
        if (window.innerWidth < 860) {
            // Se for, exibe o botão apenas quando o usuário chegar ao final da página
            if (window.innerHeight + window.pageYOffset >= document.body.offsetHeight) {
                document.getElementById("btnVoltarAoTopoIndex").style.display = "block";
            } else {
                document.getElementById("btnVoltarAoTopoIndex").style.display = "none";
            }
        } else {
            // Se não, usa a lógica original
            if (document.body.scrollTop > 1000 || document.documentElement.scrollTop > 1000) {
                document.getElementById("btnVoltarAoTopoIndex").style.display = "block";
            } else {
                document.getElementById("btnVoltarAoTopoIndex").style.display = "none";
            }
        }
    };

    window.voltarAoTopoIndex = function () {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    };

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


});