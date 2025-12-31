console.log("transaction.js loaded");

const itemSelect = document.getElementById("item_id");
const priceInput = document.getElementById("price");

if (itemSelect && priceInput) { 
  function updatePrice() {
    const selectedOption = itemSelect.options[itemSelect.selectedIndex];
    priceInput.value = selectedOption.dataset.price || 0;
  }

  itemSelect.addEventListener("change", updatePrice);

  // Initialize on page load
  updatePrice();
  }console.log("transaction.js loaded");

document.addEventListener("DOMContentLoaded", () => {

    const itemSelect = document.getElementById("item_id");
    const priceInput = document.getElementById("price");

    function updatePrice() {
        if (!itemSelect || !priceInput) return; // Prevent errors
        const selectedOption = itemSelect.options[itemSelect.selectedIndex];
        priceInput.value = selectedOption.dataset.price || 0;
    }

    if (itemSelect) {
        itemSelect.addEventListener("change", updatePrice);
        updatePrice(); // Initialize on page load
    }

    async function getTransactions() {
        if (!window.fetchWithRefresh) {
            console.error("fetchWithRefresh not available!");
            return;
        }

        try {
            const response = await window.fetchWithRefresh("/transactions", {
                method: "GET",
            });

            if (response.ok) {
                const data = await response.json();
                console.log("Transactions:", data);
            } else {
                console.error("Failed to fetch transactions", response.status);
            }
        } catch (error) {
            console.error("Fetch transactions error:", error);
        }
    }
});