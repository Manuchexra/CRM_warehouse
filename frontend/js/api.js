const API_BASE_URL = 'http://localhost:8000/api';

const API = {
    async request(endpoint, options = {}) {
        const token = localStorage.getItem('access_token');
        const headers = {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
            ...options.headers
        };

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers
        });

        if (response.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            const isLoginPage = window.location.pathname.endsWith('index.html') || window.location.pathname === '/';
            if (!isLoginPage) {
                showNotification('Sessiya tugadi. Qayta kiring.', 'error');
                setTimeout(() => { window.location.href = 'index.html'; }, 1500);
            }
            throw new Error('Unauthorized');
        }

        const data = await response.json();
        if (!response.ok) {
            const msg = data.detail || (Array.isArray(data) ? JSON.stringify(data) : 'Xatolik yuz berdi');
            throw new Error(msg);
        }
        return data;
    },

    // ── Auth ──────────────────────────────────────────────────────────────
    async login(username, password) {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || 'Login xatosi');
        return data;
    },

    getMe: () => API.request('/auth/me'),

    async logout() {
        try { await API.request('/auth/logout', { method: 'POST' }); } catch (_) {}
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = 'index.html';
    },

    // ── CRM ───────────────────────────────────────────────────────────────
    getCustomers: (search = '') =>
        API.request(`/crm/customers${search ? `?search=${encodeURIComponent(search)}` : ''}`),
    getCustomer: (id) => API.request(`/crm/customers/${id}`),
    createCustomer: (data) => API.request('/crm/customers', { method: 'POST', body: JSON.stringify(data) }),
    updateCustomer: (id, data) => API.request(`/crm/customers/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deleteCustomer: (id) => API.request(`/crm/customers/${id}`, { method: 'DELETE' }),
    getCustomerOrders: (id) => API.request(`/crm/customers/${id}/orders`),

    // ── ERP ───────────────────────────────────────────────────────────────
    getOrders: (status = '') =>
        API.request(`/erp/orders${status ? `?status=${encodeURIComponent(status)}` : ''}`),
    getOrder: (id) => API.request(`/erp/orders/${id}`),
    createOrder: (data) => API.request('/erp/orders', { method: 'POST', body: JSON.stringify(data) }),
    updateOrder: (id, data) => API.request(`/erp/orders/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    updateOrderStatus: (id, status) =>
        API.request(`/erp/orders/${id}/status?status=${encodeURIComponent(status)}`, { method: 'PUT' }),
    deleteOrder: (id) => API.request(`/erp/orders/${id}`, { method: 'DELETE' }),

    // ── WMS ───────────────────────────────────────────────────────────────
    getProducts: (category = '') =>
        API.request(`/wms/products${category ? `?category=${encodeURIComponent(category)}` : ''}`),
    getProduct: (id) => API.request(`/wms/products/${id}`),
    createProduct: (data) => API.request('/wms/products', { method: 'POST', body: JSON.stringify(data) }),
    updateProduct: (id, data) => API.request(`/wms/products/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deleteProduct: (id) => API.request(`/wms/products/${id}`, { method: 'DELETE' }),
    getInventory: () => API.request('/wms/inventory'),
    updateInventory: (productId, quantity) =>
        API.request(`/wms/inventory/${productId}?stock_quantity=${quantity}`, { method: 'PUT' }),
    getLowStock: (threshold = 10) => API.request(`/wms/inventory/low?threshold=${threshold}`),

    // ── Reports ───────────────────────────────────────────────────────────
    getDashboardStats: () => API.request('/reports/dashboard'),
    getSalesReport: (days = 30) => API.request(`/reports/sales?days=${days}`),
    getInventoryReport: () => API.request('/reports/inventory'),
    getOrdersStatusReport: () => API.request('/reports/orders-status'),
};

// ── Notification helper ───────────────────────────────────────────────────
function showNotification(message, type = 'success') {
    const container = document.getElementById('notification-container');
    if (!container) return;

    const icons = {
        success: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:16px;height:16px"><polyline points="20 6 9 17 4 12"/></svg>`,
        error:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:16px;height:16px"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`,
        info:    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:16px;height:16px"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`
    };

    const div = document.createElement('div');
    div.className = `notification ${type}`;
    div.innerHTML = `${icons[type] || ''}<span>${message}</span>`;
    container.appendChild(div);

    setTimeout(() => {
        div.style.transition = 'opacity 0.3s, transform 0.3s';
        div.style.opacity = '0';
        div.style.transform = 'translateX(110%)';
        setTimeout(() => div.remove(), 300);
    }, 3500);
}
