// Traz algumas informações da api
$(document).ready(function () {
    var mangas = {};
    $.ajax({
        url: "/api/v1/",
        dataType: "json",
        success: function (data) {
            for (var i = 0; i < data.length; i++) {
                mangas[data[i].id_manga] = data[i];
            }
        },
        error: function () {
            alert("Ocorreu um erro ao buscar as informações dos mangás.");
        }
    });
    $(document).on("click", ".acard", ".atitle", function(event) {
        event.preventDefault();
        var id_manga = $(this).data("item-id");
        console.log(id_manga);
        var manga = mangas[id_manga];
        var url = window.location.origin;
        var genres = manga.genres.join(', ')
        $("#MangaBaseName").text(manga.title);
        $("#manga-sinopse").text(manga.sinopse);
        $("#manga-genres").text(genres);
        $("#manga-capa-img").attr("src", manga.capa);
        $("#manga-url-capitulo").attr({
            "href": url + '/manga/' + manga.slug,
            "title": 'Ler ' + manga.title + ' Online!'
        });
    });
////////////////////////////////////////////////////////////////////////////////////
    $('#manga-name-input').on('input', function() {
        var notPaginationDiv = $('#not-pagination');
        var mangaName = $(this).val();
        if (mangaName.length >= 1) {
            notPaginationDiv.hide().css('display', 'none');
        } else {
            notPaginationDiv.show();
        }
        $.ajax({
            url: '/lista-de-titulos/A-Z/search/',
            data: {manga_name: mangaName},
            success: function(data) {
                var html = '';
                for (var i = 0; i < data.length; i++) {
                    var manga = data[i];
                    html += '<div class="col-my card-manga">';
                    html += '<div class="card">';
                    html += '<a data-bs-toggle="modal" data-bs-target="#exampleModal" class="acard" href="#" title="Leia '+ manga.title +' Online!" data-item-id="'+ manga.id_manga +'">';
                    html += '<img class="card-img-top unic" src="'+ manga.capa +'" alt="'+ manga.title +'">';
                    html += '</a>';
                    html += '<div class="card-body">';
                    html += '<a data-bs-toggle="modal" data-bs-target="#exampleModal" href="#" title="Leia '+ manga.title +' Online!" data-item-id="'+ manga.id_manga +'">';
                    html += '<h5 class="card-title1">'+ manga.title +'</h5>';
                    html += '</a>';
                    html += '</div>';
                    html += '</div>';
                    html += '</div>';
                }
                $('#search-results').html(html);
            }
        });
    });
});
// codigo para deixar as letras do alfhabetos ativas ao clicar
document.addEventListener("DOMContentLoaded", function() {
    var activeButtonId = localStorage.getItem("activeButton");
    var link = activeButtonId ? document.getElementById(activeButtonId) : null;

    var alphabetDivs = document.querySelectorAll(".alphabet");

    alphabetDivs.forEach(function(div) {
        div.addEventListener("click", function() {
        if (link) {
            link.classList.remove("active");
        }
        div.classList.add("active");
        link = div;
        localStorage.setItem("activeButton", div.id);
        });
    });
    document.addEventListener("click", function(event) {
        var isClickInside = false;
        alphabetDivs.forEach(function(div) {
        if (div.contains(event.target)) {
            isClickInside = true;
        }
    });
    if (!isClickInside && link) {
        link.classList.remove("active");
        link = null;
        localStorage.removeItem("activeButton");
        }
    });
    if (!link) {
        var azButton = document.getElementById("A-Z");
        azButton.classList.add("active");
        link = azButton;
        localStorage.setItem("activeButton", azButton.id);
    } else {
        link.classList.add("active");
    }
});
var selectElement = document.getElementById("select-genre");
var selectedGenre = localStorage.getItem("selectedGenre");
if (selectedGenre) {
    selectElement.value = selectedGenre;
}

function redirectToGenre() {
    var selectedGenre = selectElement.value;

    if (selectedGenre !== "") {
        console.log(selectedGenre)
        localStorage.setItem("selectedGenre", selectedGenre);
        window.location.href = "/lista-de-titulos/A-Z/search-genero/" + selectedGenre;
    }if(selectedGenre === "Selecione o genero"){
        window.location.href = "/lista-de-titulos/A-Z";
    }
}

var selectElement = document.getElementById("select-genre");
var selectedGenre = localStorage.getItem("selectedGenre");

localStorage.removeItem("selectedGenre");

if (!selectedGenre) {
    localStorage.setItem("selectedGenre", "Selecione o genero");
} else {
    selectElement.value = selectedGenre;
}

function redirectToGenre() {
    var selectedGenre = selectElement.value;
    if (selectedGenre === "Selecione o genero"){
        window.location.href = "/lista-de-titulos/A-Z";
    }else if (selectedGenre !== "") {
        localStorage.setItem("selectedGenre", selectedGenre);
        window.location.href = "/lista-de-titulos/A-Z/search-genero/" + selectedGenre;
    }
}