document.addEventListener("DOMContentLoaded", function () {
    // Check if this is a fresh page load or if a donation is being made
    let donationForm = document.getElementById("donationForm");

    if (!sessionStorage.getItem("donor_welcome_shown")) {
        // SweetAlert for Welcome (Show only once per session)
        Swal.fire({
            title: "Welcome!",
            text: "You are logged into your Donor Dashboard.",
            icon: "success",
            confirmButtonText: "OK"
        });

        sessionStorage.setItem("donor_welcome_shown", "true"); // Prevent re-showing
    }

    // Logout function
    document.getElementById("logout").addEventListener("click", function () {
        Swal.fire({
            title: "Are you sure?",
            text: "You will be logged out.",
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Logout",
            cancelButtonText: "Cancel"
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = "{% url 'login_form' %}"; // Redirect to login page
            }
        });
    });

    // Donation Form Handling
    if (donationForm) {
        donationForm.addEventListener("submit", function (event) {
            event.preventDefault(); // Prevent default form submission

            let amount = document.getElementById("amount").value.trim();

            if (!amount || amount <= 0) {
                Swal.fire({
                    title: "Invalid Amount",
                    text: "Please enter a valid donation amount.",
                    icon: "error"
                });
                return;
            }

            Swal.fire({
                title: "Confirm Donation",
                text: "You are about to donate ₹" + amount,
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                confirmButtonText: "Yes, Donate"
            }).then((result) => {
                if (result.isConfirmed) {
                    // Process the donation after confirmation
                    Swal.fire({
                        title: "Processing...",
                        text: "Your donation is being processed.",
                        icon: "info",
                        timer: 2000,
                        showConfirmButton: false
                    });

                    setTimeout(() => {
                        donationForm.submit();
                    }, 2000); // Delay submission to allow processing alert
                }
            });
        });
    }
});
fetch('/api/donate/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + userToken
    },
    body: JSON.stringify({
        amount: donationAmount,
        donation_type: donationType
    })
})
.then(response => response.json())
.then(data => {
    console.log("Donation Successful:", data);
})
.catch(error => console.error("Error:", error));
$.ajax({
    type: 'POST',
    url: '/donate/',
    data: {
        name: name,
        amount: amount
        // Don't include csrfmiddlewaretoken here
    },
    success: function(response) {
        // handle success
    }
});
