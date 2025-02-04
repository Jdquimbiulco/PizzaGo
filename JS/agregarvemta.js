// Mostrar el formulario de registrar venta
document.getElementById('register-sale').addEventListener('click', function() {
    document.getElementById('register-sale-form').style.display = 'block';
    document.getElementById('generate-report-form').style.display = 'none';
});

// Mostrar el formulario de generar reporte de ventas
document.getElementById('generate-report').addEventListener('click', function() {
    document.getElementById('register-sale-form').style.display = 'none';
    document.getElementById('generate-report-form').style.display = 'block';
});

// Obtener clientes y productos desde el backend
window.addEventListener('DOMContentLoaded', function() {
    fetch('http://127.0.0.1:5000/get-clientes')
        .then(response => response.json())
        .then(data => {
            const clienteSelect = document.getElementById('clienteVenta');
            data.forEach(cliente => {
                const option = document.createElement('option');
                option.value = cliente._id;
                option.textContent = cliente.nombre;
                clienteSelect.appendChild(option);
            });
        });

    fetch('http://127.0.0.1:5000/get-productos')
        .then(response => response.json())
        .then(data => {
            const productoSelect = document.getElementById('productoVenta');
            data.forEach(producto => {
                const option = document.createElement('option');
                option.value = producto._id;
                option.textContent = producto.producto;
                productoSelect.appendChild(option);
            });
        });
});

// Manejar el envío del formulario de venta
document.getElementById('venta-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const clienteId = document.getElementById('clienteVenta').value;
    const productoId = document.getElementById('productoVenta').value;
    const cantidad = document.getElementById('cantidadVenta').value;

    const data = { clienteId, productoId, cantidad };

    fetch('http://127.0.0.1:5000/registrar-venta', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => console.error('Error:', error));
});

// Generar reporte de ventas
document.getElementById('generate-report-button').addEventListener('click', function() {
    window.location.href = 'http://127.0.0.1:5000/generar-reporte-ventas';
});
// Función para mostrar la pantalla de carga
function showLoading() {
    const loadingScreen = document.getElementById('loading-screen');
    loadingScreen.style.visibility = 'visible';
    loadingScreen.style.opacity = '1';
}

// Función para ocultar la pantalla de carga
function hideLoading() {
    const loadingScreen = document.getElementById('loading-screen');
    loadingScreen.style.visibility = 'hidden';
    loadingScreen.style.opacity = '0';
}

// Al cargar la ventana, ocultar la pantalla de carga
window.onload = function() {
    hideLoading(); // Ocultar la pantalla de carga cuando la página esté completamente cargada
};
