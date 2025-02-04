async function obtenerDatos() {
    try {
        const response = await fetch('http://localhost:5000/get-usuarios'); 
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}       

document.addEventListener("DOMContentLoaded", () => {
    obtenerDatos().then(data => {
        document.getElementById('usuarios-count').textContent = data.length.toString();
    });
});


async function obtenerDatosProductos() {
    try {
        const response = await fetch('http://localhost:5000/get-productos'); 
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}       

document.addEventListener("DOMContentLoaded", () => {
    obtenerDatosProductos().then(data => {
        document.getElementById('productos-count').textContent = data.length.toString();
    });
});

async function obtenerDatosPedidos() {
    try {
        const response = await fetch('http://localhost:5000/get-pedidos'); 
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}       

document.addEventListener("DOMContentLoaded", () => {
    obtenerDatosPedidos().then(data => {
        document.getElementById('pedidos-count').textContent = data.length.toString();
    });
});


async function obtenerDatosPedidos() {
    try {
        const response = await fetch('http://localhost:5000/get-ventas'); 
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}       

document.addEventListener("DOMContentLoaded", () => {
    obtenerDatosPedidos().then(data => {
        document.getElementById('ventas-count').textContent = data.length.toString();
    });
});