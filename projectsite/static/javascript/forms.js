function toggleOwnerDetails() {
    const isOwner = document.getElementById('Yes').checked;
    const ownerFields = document.querySelectorAll('#owner-details input');

    ownerFields.forEach(field => {
        field.disabled = isOwner;
        field.required = !isOwner;
    });
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("Yes").addEventListener("change", toggleOwnerDetails);
    document.getElementById("No").addEventListener("change", toggleOwnerDetails);
    toggleOwnerDetails();
});

// for next form
document.getElementById("nextButton").addEventListener("click", function(event) {
    event.preventDefault(); // Prevent actual form submission
    window.location.href = "../Forms/forms_2.html"; // Redirect to the next form page
});
function toggleOwnerDetails() {
    const yesRadio = document.getElementById('Yes');
    const ownerFields = document.querySelectorAll('#owner-details input');

    if (yesRadio) {
        const isOwner = yesRadio.checked;

        ownerFields.forEach(field => {
            field.disabled = isOwner;
            field.required = !isOwner;
        });
    }
}

document.addEventListener("DOMContentLoaded", function () {
    let yesRadio = document.getElementById("Yes");
    let noRadio = document.getElementById("No");

    if (yesRadio && noRadio) {
        yesRadio.addEventListener("change", toggleOwnerDetails);
        noRadio.addEventListener("change", toggleOwnerDetails);
        toggleOwnerDetails();
    }

    let nextButton = document.getElementById("nextButton");
    if (nextButton) {
        nextButton.addEventListener("click", function (event) {
            event.preventDefault();
            window.location.href = "../Forms/forms_2.html";
        });
    }

    populateFormData(); // Populate data when the page loads
});

function populateFormData() {
    let params = new URLSearchParams(window.location.search);
    let userId = params.get("user") || "2025-0-001"; // Default user if no ID is provided

    // Sample hardcoded data
    let sampleData = {
        "2025-0-001": {
            firstName: "Taylor",
            lastName: "Swift",
            email: "taylor@example.com",
            phoneNumber: "123-456-7890",
            address: "123 Nashville Ave",
            dateOfBirth: "1989-12-13",
            gender: "Female",
            vehicleType: "Sedan",
            licensePlate: "ABC-1234",
            licenseNumber: "TAYLOR-001",
            registrationNumber: "REG-2025-001",
            insuranceCompany: "Swift Insurance",
            policyNumber: "POLICY-5678",
            driveLink: "https://example.com/sample-drive-link"
        }
    };

    let data = sampleData[userId];

    if (!data) {
        alert("No application data found for this user.");
        return;
    }

    // Fill out Form 1 fields
    $("input[name='firstName']").val(data.firstName);
    $("input[name='lastName']").val(data.lastName);
    $("input[name='email']").val(data.email);
    $("input[name='phoneNumber']").val(data.phoneNumber);
    $("input[name='address']").val(data.address);
    $("input[name='dateOfBirth']").val(data.dateOfBirth);
    $("input[name='gender'][value='" + data.gender + "']").prop("checked", true);

    // Fill out Form 2 fields (Vehicle Information)
    $("input[name='vehicleType']").val(data.vehicleType);
    $("input[name='licensePlate']").val(data.licensePlate);
    $("input[name='licenseNumber']").val(data.licenseNumber);
    $("input[name='registrationNumber']").val(data.registrationNumber);
    $("input[name='insuranceCompany']").val(data.insuranceCompany);
    $("input[name='policyNumber']").val(data.policyNumber);
    $("#drive-link").val(data.driveLink);
}
