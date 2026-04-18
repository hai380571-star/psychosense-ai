let cart = [];
document.getElementById('billDate').innerText = new Date().toLocaleDateString();

function addItem(name, price, cost) {
    let item = cart.find(i => i.name === name);
    if(item) { item.qty++; } 
    else { cart.push({name, price, cost, qty: 1}); }
    renderTable();
}

function renderTable() {
    let tbody = document.querySelector("#billTable tbody");
    tbody.innerHTML = "";
    let sub = 0;
    cart.forEach(i => {
        let total = i.price * i.qty;
        sub += total;
        tbody.innerHTML += `<tr><td>${i.name}</td><td>${i.price}</td><td>${i.qty}</td><td>${total}</td></tr>`;
    });
    calculateTotal(sub);
}

function calculateTotal(sub = null) {
    if(sub === null) {
        sub = cart.reduce((a, b) => a + (b.price * b.qty), 0);
    }
    let disc = parseFloat(document.getElementById('disc').value) || 0;
    document.getElementById('gTotal').innerText = sub - disc;
}

function saveBill() {
    let grand = parseFloat(document.getElementById('gTotal').innerText);
    let totalCost = cart.reduce((a, b) => a + (b.cost * b.qty), 0);
    
    let data = {
        company_id: document.getElementById('activeCoId').value,
        type: document.getElementById('bType').value,
        ref_no: document.getElementById('refNo').value,
        total: grand,
        profit: grand - totalCost,
        payment: document.getElementById('pay').value
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
