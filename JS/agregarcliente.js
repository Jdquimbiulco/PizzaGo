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

