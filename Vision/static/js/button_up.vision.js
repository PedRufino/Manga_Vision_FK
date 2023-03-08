document.addEventListener("DOMContentLoaded", function () {
    var prevScrollpos = window.pageYOffset; // Define a variável prevScrollpos aqui

    window.onscroll = function () {

        var menuContainer = document.getElementById("menu-vision");
        var btnVoltarAoTopo = document.getElementById("btnVoltarAoTopo");
        var currentScrollPos = window.pageYOffset;

        // Controla o comportamento do menu de navegação
        if (currentScrollPos) {
            menuContainer.style.position = "absolute";
        }
        prevScrollpos = currentScrollPos;
        // console.log("Evento onscroll chamado");
        // console.log("Valor de document.body.scrollTop: " + document.body.scrollTop);
        // console.log("Valor de document.documentElement.scrollTop: " + document.documentElement.scrollTop);

        // Verifica se a largura da tela é menor que 860 pixels
        if (window.innerWidth < 860) {
            // Se for, exibe o botão apenas quando o usuário chegar ao final da página
            if (window.innerHeight + window.pageYOffset >= document.body.offsetHeight) {
                document.getElementById("btnVoltarAoTopo").style.display = "block";
            } else {
                document.getElementById("btnVoltarAoTopo").style.display = "none";
            }
        } else {
            // Se não, usa a lógica original
            if (document.body.scrollTop > 2000 || document.documentElement.scrollTop > 2000) {
                document.getElementById("btnVoltarAoTopo").style.display = "block";
            } else {
                document.getElementById("btnVoltarAoTopo").style.display = "none";
            }
        }
    };

    window.voltarAoTopo = function () {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    };
});


