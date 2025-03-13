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


