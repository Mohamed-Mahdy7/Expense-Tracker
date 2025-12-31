console.log("transaction.js loaded");

const itemSelect = document.getElementById("item_id");
const priceInput = document.getElementById("price");

function updatePrice() {
  const selectedOption = itemSelect.options[itemSelect.selectedIndex];
  priceInput.value = selectedOption.dataset.price || 0;
}

itemSelect.addEventListener("change", updatePrice);

// Initialize on page load
updatePrice();
