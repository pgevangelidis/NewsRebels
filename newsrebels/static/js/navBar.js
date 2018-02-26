function moveToElement(kati) {
  console.log($(kati).offset().top);
  $('html, body').animate({
    scrollTop: $(kati).offset().top - $('#navBarID').height() + 'px'
  }, 'fast');
  return false;
}
