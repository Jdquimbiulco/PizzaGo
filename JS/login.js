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
    setTimeout(() => {
        document.getElementById("loading-screen").style.display = "none";
    }, 2000);

    const loginForm = document.getElementById("login-form");

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const correo = document.getElementById("correo").value;
        const password = document.getElementById("password").value;

        const data = await obtenerDatos();
        if (!data) {
            alert("Error al obtener los datos de usuarios.");
            return;
        }
        console.log(data);
        const usuario = data.find(user => user.correo === correo && user.contraseña === password);
        console.log(usuario);
        if (!usuario) {
            alert("Usuario, contraseña o rol incorrectos.");
            return;
        }
        localStorage.setItem('usuario', JSON.stringify(usuario));
        if (usuario.rol === "admin") {
            alert("¡Bienvenido, Administrador!");
            window.location.href = "usuario.html"; 
            } else if (usuario.rol === "cliente") {
            alert("¡Bienvenido, Cliente!");
            window.location.href = "index.html"; 
            } 
    });
});

// REGISTRO DE NUEVO USUARIO
 document.getElementById("registro-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const nombre = document.getElementById("nombre").value;
    const correo = document.getElementById("correoRegistro").value;
    const password = document.getElementById("passwordRegistro").value;
    const telefono = document.getElementById("telefono").value;
    const direccion = document.getElementById("direccion").value;

    const nuevoUsuario = {
        nombre,
        correo,
        contraseña: password,
        telefono,
        direccion,
        rol: "cliente"
    };

    try {
        const response = await fetch("http://localhost:5000/agregar-usuario", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(nuevoUsuario)
        });

        const data = await response.json();
        if (!response.ok) {
            alert(data.message || "Error al registrar usuario.");
            return;
        }

        alert("Registro exitoso, ahora puedes iniciar sesión.");
        document.getElementById("registro-form").reset();
        document.getElementById("registroModal").querySelector(".btn-close").click();

    } catch (error) {
        console.error("Error:", error);
        alert("Error al conectar con el servidor.");
    }
});

























/*
window.onload = function() {
    // Si ya hay un cliente logueado, mostrar su nombre
    const cliente = JSON.parse(localStorage.getItem('cliente'));
    if (cliente) {
        document.getElementById('login-container').innerHTML = `
            <span>Hola, ${cliente.Nombre}</span>
            <button onclick="cerrarSesion()">Cerrar sesión</button>
        `;
    } else {
        const loginDropdown = document.querySelector('.login-dropdown');
        loginDropdown.style.display = 'none';
    }
*/