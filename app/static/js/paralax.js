function parallax() {
  var body = document.body;
  body.style.setProperty("--scroll", -(window.pageYOffset / 3) + "px");
}

window.addEventListener("scroll", parallax, false);
