document.getElementById("contactForm").addEventListener("submit", function(event) {
    let mensagem = document.getElementById("mensagem").value.trim();
    let mensagemAlerta = document.getElementById("mensagemAlerta");
    

    if (mensagem === "") {
        mensagemAlerta.className = "alert alert-danger mt-2 p-1 text-center";
        mensagemAlerta.textContent = "Erro: O campo de mensagem não pode estar vazio!";
        event.preventDefault(); // Evita o envio se o campo estiver vazio
        return;
    }

    mensagemAlerta.className = "alert alert-success mt-2 p-1 text-center";
    mensagemAlerta.textContent = "Mensagem encaminhada!";
});

document.addEventListener("DOMContentLoaded", function () {
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

    setInterval(nextSlide, 3000); // Muda de slide a cada 3 segundos (3000 milissegundos)
    
    // Exibe o primeiro slide inicialmente
    showSlide(currentSlide);
});
