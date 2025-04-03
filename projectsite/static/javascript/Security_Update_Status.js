document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const appId = urlParams.get("id") || "N/A";
    const username = decodeURIComponent(urlParams.get("username") || "N/A");
    const status = decodeURIComponent(urlParams.get("status") || "Pending");
    const date = urlParams.get("date") !== "N/A" ? urlParams.get("date") : "";
    const remarks = urlParams.get("remarks") !== "N/A" ? urlParams.get("remarks") : "";
    const processBy = decodeURIComponent(urlParams.get("processby") || "N/A");

    // Display Application Info
    document.getElementById("app-id").value = appId;
    document.getElementById("username").value = username;
    document.getElementById("status").value = status;
    document.getElementById("date-processed").value = date;
    document.getElementById("remarks").value = remarks;
    document.getElementById("processed-by").value = processBy;

    document.getElementById("update-form").addEventListener("submit", (e) => {
        e.preventDefault();

        const updatedData = {
            id: appId,
            username: username,
            status: document.getElementById("status").value,
            date: date || "N/A",
            remarks: document.getElementById("remarks").value.trim(),
            processBy: processBy
        };

        // Move user from payments to registration history
        let registered = JSON.parse(localStorage.getItem("registered")) || [];
        registered.push(updatedData);
        localStorage.setItem("registered", JSON.stringify(registered));

        // Remove from payments list
        localStorage.removeItem(`security_${updatedData.id}`);

        // Set sidebar to registered
        localStorage.setItem("activeMenu", "registered");

        // Redirect to history.html
        alert("Updated successfully!");
        window.location.href = "../../templates/Security Dashboard/Security_Reg_History.html";
    });
});
