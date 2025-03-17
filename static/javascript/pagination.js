let currentPage = 1;
const totalPages = 10; 

document.getElementById("prevBtn").addEventListener("click", ()=> {
    if (currentPage > 1){
        currentPage--;
        updatePagination();
    }
});

document.getElementById("pageInput").addEventListener("change", (e) => {
    const inputPage = parseInt(e.target.value);
    if (inputPage >= 1 && inputPage <= totalPages){
        currentPage = inputPage;
    } else {
        e.target.value = currentPage;
    }
    updatePagination();
});

function updatePagination (){
    document.getElementById("pageInput").value = currentPage;
    document.getElementById("prevBtn").disabled = currentPage === 1;
    document.getElementById("nextBtn").disabled = currentPage === totalPages;
}
updatePagination();