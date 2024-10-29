$(document).ready(function() {
    // Handle registration form submission
    $("#registerForm").on("submit", function(event) {
        event.preventDefault();

        const username = $("#username").val();
        const password = $("#password").val();
        const name = $("#name").val();
        const email = $("#email").val();
        const isAdmin = $("#isAdmin").is(":checked");

        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/register", // Update with your server URL
            contentType: "application/json",
            data: JSON.stringify({
                username: username,
                password: password,
                name: name,
                email: email,
                is_admin: isAdmin
            }),
            success: function(response) {
                $("#registerMessage").text(response.message).css("color", "green");
                $("#registerForm")[0].reset(); // Reset the form
            },
            error: function(xhr) {
                $("#registerMessage").text(xhr.responseJSON.error).css("color", "red");
            }
        });
    });

    // Handle login form submission
    $("#loginForm").on("submit", function(event) {
        event.preventDefault();

        const username = $("#loginUsername").val();
        const password = $("#loginPassword").val();

        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/login", // Update with your server URL
            contentType: "application/json",
            data: JSON.stringify({
                username: username,
                password: password
            }),
            success: function(response) {
                $("#loginMessage").text("Login successful!").css("color", "green");
                // You can redirect or perform other actions here
            },
            error: function(xhr) {
                $("#loginMessage").text(xhr.responseJSON.error).css("color", "red");
            }
        });
    });
});
