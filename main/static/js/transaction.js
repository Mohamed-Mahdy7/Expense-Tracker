console.log("transaction.js loaded");

const categorySelect = document.getElementById("category_id");
const priceInput = document.getElementById("price");

function updatePrice() {
    const selectedOption = categorySelect.options[categorySelect.selectedIndex];
    priceInput.value = selectedOption.dataset.price || 0;
}

categorySelect.addEventListener("change", updatePrice);

// Initialize on page load
updatePrice();