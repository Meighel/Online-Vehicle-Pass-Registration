document.addEventListener("DOMContentLoaded", async () => {
    // await loadSidebar();
    // setupSidebarToggle();
    setupSidebarHighlight();
    displayCurrentDate();
    // fixSidebarImagePaths();
});

// // Get the user role (Can be dynamic based on auth logic)
// function getUserRole() {
//     return "admin"; // Change this for testing
// }

// // Get the correct sidebar path - SOMETHING IS WRONG
// function getSidebarPath(userRole) {
//     const currentPath = window.location.pathname;
//     const depth = currentPath.split("/").filter(Boolean).length - 2;
//     const basePath = "../".repeat(Math.max(depth, 0));
    
//     return `${basePath}templates/includes/${userRole}_sidebar.html`;
// }

// // Fix broken sidebar image paths
// function fixSidebarImagePaths() {
//     const images = document.querySelectorAll(".sidebar img[data-src]");
    
//     if (!images.length) return;

//     const depth = window.location.pathname.split("/").length - 2;
//     const basePath = "../".repeat(Math.max(depth, 0)) + "static/images/";

//     images.forEach(img => {
//         img.src = basePath + img.dataset.src;
//         console.log(`Image fixed: ${img.src}`);
//     });
// }

// // Load Sidebar Dynamically
// async function loadSidebar() {
//     const userRole = getUserRole();
//     const sidebarContainer = document.getElementById("sidebar-container");

//     if (!sidebarContainer) {
//         console.error("Sidebar container not found!");
//         return;
//     }

//     const sidebarPath = getSidebarPath(userRole);
//     console.log(`Fetching sidebar from: ${sidebarPath}`);

//     try {
//         const response = await fetch(sidebarPath);
//         if (!response.ok) throw new Error(`Failed to fetch sidebar: ${response.statusText}`);

//         sidebarContainer.innerHTML = await response.text();
//         console.log("Sidebar loaded successfully.");

//         fixSidebarImagePaths(); // Ensure images load correctly after sidebar loads
//     } catch (error) {
//         console.error(`❌ Error loading sidebar: ${error.message}`);
//         sidebarContainer.innerHTML = `<p>Error loading sidebar. (${error.message})</p>`;
//     }
// }

// 📌 Sidebar toggle functionality
function setupSidebarToggle() {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("toggle-btn");

    if (!sidebar || !toggleBtn) return;

    toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed");
        localStorage.setItem("sidebarState", sidebar.classList.contains("collapsed") ? "collapsed" : "expanded");
    });

    if (localStorage.getItem("sidebarState") === "collapsed") {
        sidebar.classList.add("collapsed");
    }
}

// Highlight active sidebar menu & navigate
function setupSidebarHighlight() {
    const sidebarItems = document.querySelectorAll(".sidebar ul li");
    const activeMenu = localStorage.getItem("activeMenu") || "dashboard";

    sidebarItems.forEach(item => {
        const menuName = item.dataset.menu;
        item.classList.toggle("active", menuName === activeMenu);

        item.addEventListener("click", () => {
            document.querySelector(".sidebar ul li.active")?.classList.remove("active");
            item.classList.add("active");
            localStorage.setItem("activeMenu", menuName);

            // Navigate to the corresponding page
            const link = item.querySelector("a");
            if (link) window.location.href = link.href;
        });
    });
}

// Display current date
function displayCurrentDate() {
    const dateElement = document.getElementById("date");
    if (dateElement) {
        dateElement.textContent = new Date().toLocaleDateString("en-US", {
            weekday: "long",
            day: "numeric",
            month: "long",
            year: "numeric"
        });
    }
}