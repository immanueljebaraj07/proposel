
        const API_URL = 'http://localhost:5000/api';
        let itemCount = 0;
        let currentProposalId = null;

        // Initialize dates
        function initializeDates() {
            const today = new Date();
            document.getElementById('proposalDate').valueAsDate = today;
            
            const expiry = new Date(today);
            expiry.setDate(expiry.getDate() + 30);
            document.getElementById('expiryDate').valueAsDate = expiry;
        }

        // Add new item
        function addItem(desc = '', qty = 1, price = 0) {
            itemCount++;
            const itemHTML = `
                <div class="item" id="item-${itemCount}">
                    <div class="item-row">
                        <input type="text" placeholder="Description" value="${desc}" class="item-desc">
                        <input type="number" placeholder="Quantity" value="${qty}" class="item-qty" min="1" step="1">
                        <input type="number" placeholder="Unit Price" value="${price}" class="item-price" min="0" step="0.01">
                        <button class="btn btn-danger" onclick="removeItem(${itemCount})">✕</button>
                    </div>
                </div>
            `;
            document.getElementById('itemsContainer').insertAdjacentHTML('beforeend', itemHTML);
            generateProposal();
        }

        // Remove item
        function removeItem(id) {
            const element = document.getElementById(`item-${id}`);
            if (element) element.remove();
            generateProposal();
        }

        // Get all items
        function getItems() {
            const items = [];
            document.querySelectorAll('.item').forEach(item => {
                const desc = item.querySelector('.item-desc').value;
                const qty = parseFloat(item.querySelector('.item-qty').value) || 0;
                const price = parseFloat(item.querySelector('.item-price').value) || 0;
                if (desc && qty > 0) {
                    items.push({ description: desc, quantity: qty, unitPrice: price });
                }
            });
            return items;
        }

        // Format currency
        function formatCurrency(amount) {
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD'
            }).format(amount);
        }

        // Format date
        function formatDate(dateString) {
            return new Date(dateString).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        }

        // Show message
        function showMessage(message, type = 'success') {
            const successEl = document.getElementById('successMessage');
            const errorEl = document.getElementById('errorMessage');
            
            if (type === 'success') {
                successEl.textContent = message;
                successEl.style.display = 'block';
                errorEl.style.display = 'none';
                setTimeout(() => successEl.style.display = 'none', 3000);
            } else {
                errorEl.textContent = message;
                errorEl.style.display = 'block';
                successEl.style.display = 'none';
                setTimeout(() => errorEl.style.display = 'none', 3000);
            }
        }

        // Generate proposal preview
        function generateProposal() {
            const company = document.getElementById('companyName').value;
            const clientName = document.getElementById('clientName').value;
            const clientCompany = document.getElementById('clientCompany').value;
            const title = document.getElementById('proposalTitle').value;
            const proposalDate = document.getElementById('proposalDate').value;
            const expiryDate = document.getElementById('expiryDate').value;
            const description = document.getElementById('description').value;
            const terms = document.getElementById('terms').value;
            const items = getItems();

            let itemsHTML = '';
            let subtotal = 0;

            items.forEach(item => {
                const total = item.quantity * item.unitPrice;
                subtotal += total;
                itemsHTML += `
                    <tr>
                        <td>${item.description}</td>
                        <td style="text-align: center;">${item.quantity}</td>
                        <td style="text-align: right;">${formatCurrency(item.unitPrice)}</td>
                        <td style="text-align: right; font-weight: bold;">${formatCurrency(total)}</td>
                    </tr>
                `;
            });

            const tax = subtotal * 0.1;
            const total = subtotal + tax;

            const previewHTML = `
                <div class="proposal-preview">
                    <div class="proposal-header">
                        <h1>${title || 'Proposal'}</h1>
                        <p style="color: #666; margin: 10px 0;">Proposal for: <strong>${clientCompany}</strong></p>
                    </div>

                    <div class="proposal-section">
                        <h3>📧 From</h3>
                        <p><strong>${company}</strong></p>
                        <p>Email: ${document.getElementById('companyEmail').value}</p>
                        <p>Phone: ${document.getElementById('companyPhone').value}</p>
                    </div>

                    <div class="proposal-section">
                        <h3>👤 To</h3>
                        <p><strong>${clientName}</strong></p>
                        <p>${clientCompany}</p>
                        <p>Email: ${document.getElementById('clientEmail').value}</p>
                    </div>

                    <div class="proposal-section">
                        <h3>📅 Dates</h3>
                        <p>Proposal Date: <strong>${proposalDate ? formatDate(proposalDate) : 'Not set'}</strong></p>
                        <p>Valid Until: <strong>${expiryDate ? formatDate(expiryDate) : 'Not set'}</strong></p>
                    </div>

                    <div class="proposal-section">
                        <h3>📝 Description</h3>
                        <p>${description}</p>
                    </div>

                    <div class="proposal-section">
                        <h3>💼 Services & Items</h3>
                        <table class="proposal-table">
                            <thead>
                                <tr>
                                    <th>Description</th>
                                    <th style="text-align: center;">Quantity</th>
                                    <th style="text-align: right;">Unit Price</th>
                                    <th style="text-align: right;">Total</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${itemsHTML || '<tr><td colspan="4" style="text-align: center; color: #999;">No items added</td></tr>'}
                                <tr class="total-row">
                                    <td colspan="3" style="text-align: right;">Subtotal:</td>
                                    <td style="text-align: right;">${formatCurrency(subtotal)}</td>
                                </tr>
                                <tr class="total-row">
                                    <td colspan="3" style="text-align: right;">Tax (10%):</td>
                                    <td style="text-align: right;">${formatCurrency(tax)}</td>
                                </tr>
                                <tr class="total-row" style="background: #667eea; color: white;">
                                    <td colspan="3" style="text-align: right;">Total:</td>
                                    <td style="text-align: right;">${formatCurrency(total)}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="proposal-section">
                        <h3>⚖️ Terms & Conditions</h3>
                        <p>${terms}</p>
                    </div>

                    <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd;">
                        <p style="color: #666; font-size: 0.9em;">Thank you for your consideration. We look forward to working with you!</p>
                    </div>
                </div>
            `;

            document.getElementById('proposalPreview').innerHTML = previewHTML;
            document.getElementById('proposalsList').style.display = 'none';
        }

        // Save proposal to backend
        async function saveProposal() {
            try {
                const data = {
                    company_name: document.getElementById('companyName').value,
                    client_name: document.getElementById('clientName').value,
                    client_company: document.getElementById('clientCompany').value,
                    title: document.getElementById('proposalTitle').value,
                    proposal_date: document.getElementById('proposalDate').value,
                    expiry_date: document.getElementById('expiryDate').value,
                    description: document.getElementById('description').value,
                    terms: document.getElementById('terms').value,
                    items: getItems()
                };

                const response = await fetch(`${API_URL}/proposals/create`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                if (result.status === 'success') {
                    currentProposalId = result.id;
                    showMessage(`✅ Proposal saved successfully! (ID: ${result.id})`);
                } else {
                    showMessage(`❌ Error: ${result.message}`, 'error');
                }
            } catch (error) {
                showMessage(`❌ Error: ${error.message}`, 'error');
            }
        }

        // Download proposal as PDF
        async function downloadProposal() {
            if (!currentProposalId) {
                showMessage('❌ Please save the proposal first', 'error');
                return;
            }
            window.open(`${API_URL}/proposals/${currentProposalId}/pdf`);
        }


 // ...existing code...

// Show saved proposals
async function showProposalsList() {
    try {
        const response = await fetch(`${API_URL}/proposals`);
        const result = await response.json();

        if (result.status === 'success' && result.data.length > 0) {
            let listHTML = '<h2>📂 All Saved Proposals</h2>';
            result.data.forEach(proposal => {
                listHTML += `
                    <div class="proposal-item">
                        <div class="proposal-item-info">
                            <strong>${proposal.title}</strong><br>
                            Client: ${proposal.client_name} (${proposal.client_company})<br>
                            Date: ${proposal.proposal_date} | Total: ${formatCurrency(proposal.total)}
                        </div>
                        <div class="proposal-item-actions">
                            <button class="btn btn-small btn-primary" onclick="loadProposal(${proposal.id})">📋 View</button>
                            <button class="btn btn-small btn-download" onclick="printProposal(${proposal.id})">🖨️ Print</button>
                            <button class="btn btn-small btn-download" onclick="downloadProposalById(${proposal.id})">📥 PDF</button>
                            <button class="btn btn-small btn-danger" onclick="deleteProposal(${proposal.id})">🗑️ Delete</button>
                        </div>
                    </div>
                `;
            });
            document.getElementById('proposalsList').innerHTML = listHTML;
            document.getElementById('proposalsList').style.display = 'block';
            document.getElementById('proposalPreview').innerHTML = '';
        } else {
            showMessage('❌ No proposals found', 'error');
        }
    } catch (error) {
        showMessage(`❌ Error: ${error.message}`, 'error');
    }
}

// Load proposal from backend
async function loadProposal(id) {
    try {
        const response = await fetch(`${API_URL}/proposals/${id}`);
        const result = await response.json();

        if (result.status === 'success') {
            const data = result.data;
            document.getElementById('companyName').value = data.company_name;
            document.getElementById('clientName').value = data.client_name;
            document.getElementById('clientCompany').value = data.client_company;
            document.getElementById('proposalTitle').value = data.title;
            document.getElementById('proposalDate').value = data.proposal_date;
            document.getElementById('expiryDate').value = data.expiry_date;
            document.getElementById('description').value = data.description;
            document.getElementById('terms').value = data.terms;

            document.getElementById('itemsContainer').innerHTML = '';
            itemCount = 0;
            data.items.forEach(item => {
                addItem(item.description, item.quantity, item.unitPrice);
            });

            currentProposalId = id;
            document.getElementById('proposalsList').style.display = 'none';
            showMessage('✅ Proposal loaded successfully');
        }
    } catch (error) {
        showMessage(`❌ Error: ${error.message}`, 'error');
    }
}

// Print proposal
async function printProposal(id) {
    try {
        const response = await fetch(`${API_URL}/proposals/${id}`);
        const result = await response.json();

        if (result.status === 'success') {
            const data = result.data;
            
            // Create print window
            const printWindow = window.open('', 'PRINT', 'height=800,width=1000');
            
            let itemsHTML = '';
            let subtotal = 0;

            data.items.forEach(item => {
                const total = item.quantity * item.unitPrice;
                subtotal += total;
                itemsHTML += `
                    <tr>
                        <td>${item.description}</td>
                        <td style="text-align: center;">${item.quantity}</td>
                        <td style="text-align: right;">${formatCurrency(item.unitPrice)}</td>
                        <td style="text-align: right; font-weight: bold;">${formatCurrency(total)}</td>
                    </tr>
                `;
            });

            const tax = subtotal * 0.1;
            const total = subtotal + tax;

            const printContent = `
                <html>
                <head>
                    <style>
                        body { font-family: Arial, sans-serif; margin: 20px; }
                        .header { text-align: center; margin-bottom: 30px; border-bottom: 2px solid #333; padding-bottom: 20px; }
                        .header h1 { margin: 0; color: #667eea; }
                        .section { margin-bottom: 20px; }
                        .section h3 { color: #667eea; border-bottom: 1px solid #ddd; padding-bottom: 8px; }
                        table { width: 100%; border-collapse: collapse; margin: 15px 0; }
                        th { background: #667eea; color: white; padding: 10px; text-align: left; }
                        td { padding: 10px; border-bottom: 1px solid #ddd; }
                        tr:nth-child(even) { background: #f9f9f9; }
                        .total-row { background: #f0f0f0; font-weight: bold; }
                        .total-row.final { background: #667eea; color: white; }
                        @media print { body { margin: 0; } }
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>${data.title}</h1>
                        <p>Proposal for: <strong>${data.client_company}</strong></p>
                    </div>

                    <div class="section">
                        <h3>📧 From</h3>
                        <p><strong>${data.company_name}</strong></p>
                        <p>Email: ${document.getElementById('companyEmail').value}</p>
                        <p>Phone: ${document.getElementById('companyPhone').value}</p>
                    </div>

                    <div class="section">
                        <h3>👤 To</h3>
                        <p><strong>${data.client_name}</strong></p>
                        <p>${data.client_company}</p>
                        <p>Email: ${document.getElementById('clientEmail').value}</p>
                    </div>

                    <div class="section">
                        <h3>📅 Dates</h3>
                        <p>Proposal Date: <strong>${formatDate(data.proposal_date)}</strong></p>
                        <p>Valid Until: <strong>${formatDate(data.expiry_date)}</strong></p>
                    </div>

                    <div class="section">
                        <h3>📝 Description</h3>
                        <p>${data.description}</p>
                    </div>

                    <div class="section">
                        <h3>💼 Services & Items</h3>
                        <table>
                            <thead>
                                <tr>
                                    <th>Description</th>
                                    <th style="text-align: center;">Quantity</th>
                                    <th style="text-align: right;">Unit Price</th>
                                    <th style="text-align: right;">Total</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${itemsHTML}
                                <tr class="total-row">
                                    <td colspan="3" style="text-align: right;">Subtotal:</td>
                                    <td style="text-align: right;">${formatCurrency(subtotal)}</td>
                                </tr>
                                <tr class="total-row">
                                    <td colspan="3" style="text-align: right;">Tax (10%):</td>
                                    <td style="text-align: right;">${formatCurrency(tax)}</td>
                                </tr>
                                <tr class="total-row final">
                                    <td colspan="3" style="text-align: right;">Total:</td>
                                    <td style="text-align: right;">${formatCurrency(total)}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="section">
                        <h3>⚖️ Terms & Conditions</h3>
                        <p>${data.terms}</p>
                    </div>

                    <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd;">
                        <p style="color: #666; font-size: 0.9em;">Thank you for your consideration. We look forward to working with you!</p>
                    </div>

                    <script>
                        window.print();
                        window.close();
                    </script>
                </body>
                </html>
            `;

            printWindow.document.write(printContent);
            printWindow.document.close();
            showMessage('✅ Print preview opened');
        }
    } catch (error) {
        showMessage(`❌ Error: ${error.message}`, 'error');
    }
}

// Download proposal by ID
function downloadProposalById(id) {
    window.open(`${API_URL}/proposals/${id}/pdf`);
}

// Delete proposal
async function deleteProposal(id) {
    if (!confirm('Are you sure you want to delete this proposal?')) return;

    try {
        const response = await fetch(`${API_URL}/proposals/${id}`, {
            method: 'DELETE'
        });
        const result = await response.json();

        if (result.status === 'success') {
            showMessage('✅ Proposal deleted successfully');
            showProposalsList();
        } else {
            showMessage(`❌ Error: ${result.message}`, 'error');
        }
    } catch (error) {
        showMessage(`❌ Error: ${error.message}`, 'error');
    }
}

// ...rest of existing code...
        // Sample items
        const sampleItems = [
            { description: 'Website Design', quantity: 1, unitPrice: 5000 },
            { description: 'Frontend Development', quantity: 1, unitPrice: 8000 },
            { description: 'Backend Development', quantity: 1, unitPrice: 10000 }
        ];

        // Initialize
        initializeDates();
        sampleItems.forEach(item => {
            addItem(item.description, item.quantity, item.unitPrice);
        });
        generateProposal();

        // Real-time preview update
        document.addEventListener('input', generateProposal);