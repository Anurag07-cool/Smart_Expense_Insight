document.addEventListener("DOMContentLoaded", function() {
    fetch('/dashboard/api/chart_data')
        .then(response => response.json())
        .then(data => {
            renderCategoryChart(data.category_data);
            renderMonthlyChart(data.monthly_trend);
            renderPaymentMethodChart(data.payment_method_data);
        });

    function renderCategoryChart(data) {
        const ctx = document.getElementById('categoryChart');
        if (!ctx) return;
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    data: Object.values(data),
                    backgroundColor: ['#4361ee', '#4cc9f0', '#f72585', '#3f37c9', '#ffb703', '#2b2d42']
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }

    function renderMonthlyChart(data) {
        const ctx = document.getElementById('monthlyChart');
        if (!ctx) return;
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    label: 'Monthly Spend',
                    data: Object.values(data),
                    backgroundColor: '#4361ee'
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }

    function renderPaymentMethodChart(data) {
        const ctx = document.getElementById('paymentChart');
        if (!ctx) return;
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    data: Object.values(data),
                    backgroundColor: ['#4cc9f0', '#f72585', '#ffb703', '#4361ee', '#2b2d42']
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }
});
