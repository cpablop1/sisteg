export function success(msg) {
    let alerta = document.getElementById('alerta');
    alerta.innerHTML = `<div class="alert alert-success alert-dismissible fade show" role="alert">
                            <strong><i class="fa-solid fa-circle-check"></i> ${msg}</strong>
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>`;

    setTimeout(() => alerta.innerHTML = '', 3000);
}

export function warning(msg) {
    let alerta = document.getElementById('alerta');
    alerta.innerHTML = `<div class="alert alert-warning alert-dismissible fade show" role="alert">
                            <strong><i class="fa-solid fa-triangle-exclamation"></i> ${msg}</strong>
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>`;

    setTimeout(() => alerta.innerHTML = '', 3000);
}

export function danger(msg) {
    let alerta = document.getElementById('alerta');
    alerta.innerHTML = `<div class="alert alert-danger alert-dismissible fade show" role="alert">
                            <strong><i class="fa-solid fa-triangle-exclamation"></i> ${msg}</strong>
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>`;

    setTimeout(() => alerta.innerHTML = '', 3000);
}