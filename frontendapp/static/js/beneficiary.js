document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("serviceRequestForm");

    if (form) {
        form.addEventListener("submit", function(event) {
            event.preventDefault(); // Prevents default form submission
            const selectedService = form.querySelector("select[name='service_type']").value;

            if (selectedService) {
                alert(`✅ Request submitted for: ${selectedService}`);
                form.submit();
            } else {
                alert("⚠ Please select a service before submitting.");
            }
        });
    }
});
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("serviceRequestForm");

    if (form) {
        form.addEventListener("submit", function(event) {
            event.preventDefault(); // Prevents default form submission
            const selectedService = form.querySelector("select[name='service_type']").value;

            if (selectedService) {
                // ✅ Show SweetAlert2 Success Popup
                Swal.fire({
                    title: "Request Submitted!",
                    text: `Your request for ${selectedService} has been sent successfully.`,
                    icon: "success",
                    confirmButtonText: "OK"
                }).then(() => {
                    form.submit(); // ✅ Submit form after clicking OK
                });
            } else {
                // ❌ Show SweetAlert2 Error Popup
                Swal.fire({
                    title: "Oops!",
                    text: "Please select a service before submitting.",
                    icon: "warning",
                    confirmButtonText: "OK"
                });
            }
        });
    }
});
function confirmLogout() {
    Swal.fire({
        title: "Are you sure?",
        text: "You will be logged out.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, Logout!"
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = "{% url 'logout_user' %}"; // Redirect to logout URL
        }
    });
}
