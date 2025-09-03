export function success(msg) {
    let class_alerta = document.querySelectorAll('.alerta');
    let alerta = document.getElementById('alerta');
    let contenido = `<div class="alert alert-success alert-dismissible fade show" role="alert">
                            <strong><i class="fa-solid fa-circle-check"></i> ${msg}</strong>
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>`;
    alerta.innerHTML = contenido;
    class_alerta.forEach(div => div.innerHTML = contenido);
    setTimeout(() => {
        alerta.innerHTML = ''
        class_alerta.forEach(div => div.innerHTML = '');
    }, 3000);
}

export function warning(msg) {
    let alerta = document.getElementById('alerta');
    let class_alerta = document.querySelectorAll('.alerta');
    let contenido = `<div class="alert alert-warning alert-dismissible fade show" role="alert">
                            <strong><i class="fa-solid fa-triangle-exclamation"></i> ${msg}</strong>
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>`;
    alerta.innerHTML = contenido;
    class_alerta.forEach(div => div.innerHTML = contenido);
    setTimeout(() => {
        alerta.innerHTML = ''
        class_alerta.forEach(div => div.innerHTML = '');
    }, 3000);
}

export function danger(msg) {
    let alerta = document.getElementById('alerta');
    let class_alerta = document.querySelectorAll('.alerta');
    let contenido = `<div class="alert alert-danger alert-dismissible fade show" role="alert">
                            <strong><i class="fa-solid fa-triangle-exclamation"></i> ${msg}</strong>
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>`;

    alerta.innerHTML = contenido
    class_alerta.forEach(div => div.innerHTML = contenido);

    setTimeout(() => {
        alerta.innerHTML = ''
        class_alerta.forEach(div => div.innerHTML = '');
    }, 3000);
}