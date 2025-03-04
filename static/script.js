document.addEventListener("DOMContentLoaded", function () {
    let form = document.getElementById("contactForm");
    if (form) {
        form.addEventListener("submit", function (event) {
            let mensagem = document.getElementById("mensagem").value.trim();
            let mensagemAlerta = document.getElementById("mensagemAlerta");

            if (mensagem === "") {
                mensagemAlerta.className = "alert alert-danger mt-2 p-1 text-center";
                mensagemAlerta.textContent = "Erro: O campo de mensagem não pode estar vazio!";
                event.preventDefault();
                return;
            }

            mensagemAlerta.className = "alert alert-success mt-2 p-1 text-center";
            mensagemAlerta.textContent = "Mensagem encaminhada!";
        });
    }

    const slides = document.querySelectorAll(".carousel-slide");
    let currentSlide = 0;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.style.display = i === index ? "block" : "none";
        });
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }

    if (slides.length > 0) {
        setInterval(nextSlide, 3000);
        showSlide(currentSlide);
    }
});
