import { iniciar } from "./iniciar.js";

window.onload = () => {
    setTimeout(() => {
        document.getElementById('usuario').focus();
    }, 500);
}

document.getElementById('form_login').addEventListener('submit', e => {
    e.preventDefault();
    iniciar(e.target);
});