document.addEventListener("DOMContentLoaded", function() {
    const ctx = document.getElementById('enrollmentChart').getContext('2d');
    // Obtener datos desde atributos `data-*` en el HTML
    const classNames = JSON.parse(document.getElementById('enrollmentChart').getAttribute('data-class-names'));
    const enrollmentCounts = JSON.parse(document.getElementById('enrollmentChart').getAttribute('data-enrollment-counts'));

    const enrollmentChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: classNames,
            datasets: [{
                label: 'Número de Inscripciones',
                data: enrollmentCounts,
                backgroundColor: [
    'rgba(154, 224, 231, 0.6)',
    'rgba(182, 237, 226, 0.7)',
    'rgba(128, 206, 220, 0.5)',
    'rgba(185, 243, 240, 0.6)',
    'rgba(120, 199, 255, 0.5)',
    'rgba(167, 239, 217, 0.6)',
    'rgba(203, 243, 228, 0.7)',
    'rgba(116, 183, 196, 0.5)',
    'rgba(143, 220, 239, 0.5)',
    'rgba(155, 217, 248, 0.6)'
] , // Color azul claro
            borderColor: '#275972',       // Color azul oscuro
            borderWidth: 3,
            borderRadius: 2,
            borderSkipped: false,

            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }


    });
});
