$(document).ready(function () {
  $(".btn").click(function () {
    var redirectTo = $(this).attr("redirect-to");

    if (redirectTo) {
      window.location.href = redirectTo;
    }
  });
});
