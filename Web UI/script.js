"use strict";

function send(){
  let msg = document.getElementById("message").value;
  let sec = document.getElementById("secret").value;

  $.ajax({
  url: "/send",
  type: "POST",
  data: JSON.stringify({ message: msg, secret: sec }),
  contentType: "application/json",
  success: function(data, status) {
    if (status === "success" && data === "success") {
      alert("Message Sent");
      window.location.href = "/";
    } else if (status === "success" && data === "not authorized") {
      alert("Check your secret for any misspellings");
    } else {
      alert("Something went wrong\nPlease try again later...");
    }
  }
});
}