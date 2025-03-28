document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const appId = urlParams.get("id") || "N/A";
    const username = decodeURIComponent(urlParams.get("username") || "N/A");
    const email = decodeURIComponent(urlParams.get("email") || "N/A");

    // Display Application Info
    document.getElementById("appId").textContent = appId;
    document.getElementById("username").textContent = username;
    document.getElementById("email").textContent = email;

    // Populate form fields
    document.getElementById("status").value = decodeURIComponent(urlParams.get("status") || "Pending");
    document.getElementById("paidDate").value = urlParams.get("date") !== "N/A" ? urlParams.get("date") : "";

    document.getElementById("updateForm").addEventListener("submit", (e) => {
        e.preventDefault();
    
        const updatedData = {
            id: document.getElementById("appId").textContent,
            username: document.getElementById("username").textContent,
            email: document.getElementById("email").textContent,
            status: document.getElementById("status").value,
            paidDate: document.getElementById("paidDate").value || "N/A",
            remarks: document.getElementById("remarks").value.trim()
        };
    
        // Move user from payments to transactions
        let transactions = JSON.parse(localStorage.getItem("transactions")) || [];
        transactions.push(updatedData);
        localStorage.setItem("transactions", JSON.stringify(transactions));
    
        // Remove from payments list
        localStorage.removeItem(`payment_${updatedData.id}`);
    
        // Set sidebar to transactions
        localStorage.setItem("activeMenu", "transactions");
    
        // Redirect to transaction.html
        alert("Payment details updated successfully!");
        window.location.href = "../../templates/Cashier Dashboard/Cashier_Transaction.html";
    });
});