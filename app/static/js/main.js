// RE Garage - Client-Side Interactive Logic

document.addEventListener('DOMContentLoaded', function () {
    // 1. Auto-dismiss flash alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            try {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } catch (e) {
                // Ignore if already dismissed
            }
        }, 5000);
    });

    // 2. Mobile Sidebar Toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('d-none');
        });
    }

    // 3. Dynamic Motorcycle Cascading Dropdown in Booking Form
    const customerSelect = document.getElementById('customer_id_select');
    const motorcycleSelect = document.getElementById('motorcycle_id_select');

    if (customerSelect && motorcycleSelect) {
        customerSelect.addEventListener('change', function () {
            const customerId = this.value;
            motorcycleSelect.innerHTML = '<option value="">-- Loading motorcycles... --</option>';

            if (!customerId) {
                motorcycleSelect.innerHTML = '<option value="">-- First Select Customer --</option>';
                return;
            }

            fetch(`/motorcycles/by-customer/${customerId}`)
                .then(response => response.json())
                .then(bikes => {
                    motorcycleSelect.innerHTML = '';
                    if (bikes.length === 0) {
                        motorcycleSelect.innerHTML = '<option value="">No bikes registered for this customer</option>';
                        return;
                    }
                    motorcycleSelect.innerHTML = '<option value="">-- Select Motorcycle --</option>';
                    bikes.forEach(bike => {
                        const opt = document.createElement('option');
                        opt.value = bike.id;
                        opt.textContent = `${bike.registration_number} (${bike.model}) - ${bike.odometer} km`;
                        motorcycleSelect.appendChild(opt);
                    });
                })
                .catch(err => {
                    console.error('Error fetching motorcycles:', err);
                    motorcycleSelect.innerHTML = '<option value="">Error loading motorcycles</option>';
                });
        });
    }

    // 4. Dynamic Billing Form Calculation & Line Items
    const itemsTableBody = document.getElementById('billing-items-body');
    const addItemBtn = document.getElementById('add-item-btn');
    const labourChargeInput = document.getElementById('labour_charge');
    const partsTotalDisplay = document.getElementById('parts_total_display');
    const grandTotalDisplay = document.getElementById('grand_total_display');

    if (itemsTableBody && addItemBtn) {
        let partsList = [];

        // Fetch available spare parts catalog
        fetch('/inventory/api/list')
            .then(res => res.json())
            .then(data => {
                partsList = data;
            })
            .catch(err => console.error('Error fetching inventory:', err));

        function calculateTotals() {
            let partsTotal = 0;
            const rows = itemsTableBody.querySelectorAll('tr.item-row');
            rows.forEach(row => {
                const qtyInput = row.querySelector('.item-qty');
                const priceInput = row.querySelector('.item-price');
                const totalCell = row.querySelector('.item-total');

                const qty = parseInt(qtyInput.value) || 0;
                const price = parseFloat(priceInput.value) || 0;
                const total = Math.round(qty * price * 100) / 100;

                totalCell.textContent = 'Rs. ' + total.toFixed(2);
                partsTotal += total;
            });

            const labour = parseFloat(labourChargeInput ? labourChargeInput.value : 0) || 0;
            const grandTotal = partsTotal + labour;

            if (partsTotalDisplay) partsTotalDisplay.textContent = 'Rs. ' + partsTotal.toFixed(2);
            if (grandTotalDisplay) grandTotalDisplay.textContent = 'Rs. ' + grandTotal.toFixed(2);
        }

        addItemBtn.addEventListener('click', function () {
            const tr = document.createElement('tr');
            tr.className = 'item-row';

            let optionsHtml = '<option value="">-- Choose Spare Part --</option>';
            partsList.forEach(p => {
                const stockBadge = p.quantity <= 0 ? ' [OUT OF STOCK]' : ` (In Stock: ${p.quantity})`;
                optionsHtml += `<option value="${p.id}" data-price="${p.unit_price}" data-stock="${p.quantity}">${p.name} - Rs. ${p.unit_price}${stockBadge}</option>`;
            });

            tr.innerHTML = `
                <td>
                    <select name="part_id[]" class="form-select form-select-dark item-select" required>
                        ${optionsHtml}
                    </select>
                </td>
                <td style="width: 140px;">
                    <input type="number" name="quantity[]" class="form-control form-control-dark item-qty" value="1" min="1" required>
                </td>
                <td style="width: 160px;">
                    <div class="input-group">
                        <span class="input-group-text bg-dark text-muted border-secondary">Rs.</span>
                        <input type="number" step="0.01" class="form-control form-control-dark item-price" value="0.00" readonly>
                    </div>
                </td>
                <td style="width: 150px;" class="fw-bold text-end item-total">Rs. 0.00</td>
                <td style="width: 60px;" class="text-center">
                    <button type="button" class="btn btn-sm btn-outline-danger remove-item-btn"><i class="bi bi-trash"></i></button>
                </td>
            `;

            itemsTableBody.appendChild(tr);

            const select = tr.querySelector('.item-select');
            const qtyInput = tr.querySelector('.item-qty');
            const priceInput = tr.querySelector('.item-price');
            const removeBtn = tr.querySelector('.remove-item-btn');

            select.addEventListener('change', function () {
                const selectedOpt = this.options[this.selectedIndex];
                const price = parseFloat(selectedOpt.getAttribute('data-price')) || 0;
                const stock = parseInt(selectedOpt.getAttribute('data-stock')) || 0;

                priceInput.value = price.toFixed(2);
                if (stock > 0) {
                    qtyInput.max = stock;
                }
                calculateTotals();
            });

            qtyInput.addEventListener('input', calculateTotals);

            removeBtn.addEventListener('click', function () {
                tr.remove();
                calculateTotals();
            });
        });

        if (labourChargeInput) {
            labourChargeInput.addEventListener('input', calculateTotals);
        }
    }
});
