// 1. CALCULATION LOGIC (Discount & Total)
function calculateBill() {
    let price = parseFloat(document.getElementById('item_price').value) || 0;
    let qty = parseInt(document.getElementById('item_qty').value) || 0;
    let discount = parseFloat(document.getElementById('discount_input').value) || 0;

    // Pehle subtotal nikaalo
    let subtotal = price * qty;
    
    // Final Total = Subtotal - Discount
    let finalTotal = subtotal - discount;

    // UI par update karo
    document.getElementById('display_subtotal').innerText = subtotal.toFixed(2);
    document.getElementById('display_final_total').innerText = finalTotal.toFixed(2);
    
    // Hidden input mein save karo taaki Python ko bhej sakein
    document.getElementById('total_input_hidden').value = finalTotal;
}

// 2. ITEM MODIFICATION (Pre-fill Form for Editing)
function editItem(id, name, cost, price, stock) {
    // Form ka title badal do
    document.getElementById('form-title').innerText = "Modify Item: " + name;
    
    // Inputs mein purana data bhar do
    document.getElementById('item_id').value = id;
    document.getElementById('item_name').value = name;
    document.getElementById('item_cost').value = cost; // Cost optional hai, handle ho jayega
    document.getElementById('item_price').value = price;
    document.getElementById('item_stock').value = stock;

    // Focus on first input
    document.getElementById('item_name').focus();
    
    // Scroll karke form tak le jao
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 3. DATE FILTER (Daybook Logic)
function filterByDate() {
    let selectedDate = document.getElementById('date_picker').value;
    if (selectedDate) {
        // Page reload hoga naye date parameter ke saath
        window.location.href = "/daybook?date=" + selectedDate;
    }
}

// 4. PRINT COMMAND
function printInvoice() {
    // Print se pehle check karlo agar bill khali hai
    let total = document.getElementById('display_final_total').innerText;
    if (total == "0" || total == "0.00") {
        alert("Bhai, khali bill print karke kya karoge? Pehle item add karo!");
        return;
    }
    window.print();
}

// 5. AUTO-INITIALIZE
document.addEventListener('DOMContentLoaded', () => {
    console.log("Accounting System Ready!");
    
    // Agar cost field khali hai to placeholder dikhao (Optional Logic)
    const costInput = document.getElementById('item_cost');
    if (costInput) {
        costInput.addEventListener('blur', function() {
            if (this.value === "") {
                console.log("Cost left empty, setting as optional (0)");
            }
        });
    }
});
    renderTable();
}

function renderTable() {
    let tbody = document.querySelector("#billTable tbody");
    if(!tbody) return;
    tbody.innerHTML = "";
    let sub = 0;
    cart.forEach(i => {
        sub += i.price * i.qty;
        tbody.innerHTML += `<tr><td>${i.name}</td><td>${i.qty}</td><td>${i.price * i.qty}</td></tr>`;
    });
    document.getElementById('netTotal').innerText = sub;
}

function saveItem() {
    let data = {
        name: document.getElementById('newIName').value,
        price: document.getElementById('newIPrice').value,
        cost: document.getElementById('newICost').value,
        co_id: document.getElementById('coId').value
    };
    fetch('/add-item', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(() => location.reload());
}

function saveAndPrint() {
    let grand = parseFloat(document.getElementById('netTotal').innerText);
    let totalCost = cart.reduce((a, b) => a + (b.cost * b.qty), 0);
    let data = {
        company_id: document.getElementById('coId').value,
        total: grand,
        profit: grand - totalCost
    };
    fetch('/save-bill', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(() => {
        window.print();
        location.reload();
    });
}
