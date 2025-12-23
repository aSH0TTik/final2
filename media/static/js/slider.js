let slideIndex = 0;
showSlides(slideIndex);

function changeSlide(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let slides = document.querySelectorAll(".slide-new");
    let dots = document.querySelectorAll(".dot");

    if (n >= slides.length) { slideIndex = 0; }
    if (n < 0) { slideIndex = slides.length - 1; }

    // Сдвигаем слайдер
    document.getElementById("slider-wrapper").style.transform = `translateX(-${slideIndex * 100}%)`;

    // Обновляем активную точку
    dots.forEach(dot => dot.classList.remove("active"));
    if (dots[slideIndex]) {
        dots[slideIndex].classList.add("active");
    }
}