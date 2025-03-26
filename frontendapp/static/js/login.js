document.addEventListener("DOMContentLoaded", function () {
    let container = document.getElementById('container');

    function toggle() {
        container.classList.toggle('sign-in');
        container.classList.toggle('sign-up');
    }

    // Attach event listeners to toggle elements
    document.querySelectorAll(".pointer").forEach((element) => {
        element.addEventListener("click", toggle);
    });

    // Default to Sign In view
    container.classList.add('sign-in');
});
