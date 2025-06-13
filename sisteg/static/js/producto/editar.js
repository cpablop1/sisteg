import { cambiar } from "./cambiar.js";

export function editar(id) {
    cambiar();
    fetch(`/producto/listar-producto/?id=${id}`).then(res => res.json()).then(data => {
        console.log(data);
        let inputs = ['id', 'descripcion', 'detalle', 'costo', 'precio', 'stock', 'marca_id', 'categoria_id'];
        setTimeout(() => {
            Array.from(inputs, value => {
                /* console.log(data.data[0][value]);
                console.log(document.getElementById(value)); */
                document.getElementById(value).value = data.data[0][value];
            });
            if (data.data[0]['img1'] != '') {
                document.getElementById('ver_img1').innerHTML = `
                    <img src="../../media/${data.data[0]['img1']}" class="img-thumbnail" style="width: 10rem;">
                    <div class="form-check text-danger fs-4 mx-5">
                        <input class="form-check-input" type="checkbox" id="eliminar_img1" name="eliminar_img1">
                        <label class="form-check-label" for="flexCheckIndeterminate">
                            <i class="fa-solid fa-trash-can"></i>
                        </label>
                    </div>
                `;
            }
            if (data.data[0]['img2'] != '') {
                document.getElementById('ver_img2').innerHTML = `
                    <img src="../../media/${data.data[0]['img2']}" class="img-thumbnail" style="width: 10rem;">
                    <div class="form-check text-danger fs-4 mx-5">
                        <input class="form-check-input" type="checkbox" id="eliminar_img2" name="eliminar_img2">
                        <label class="form-check-label" for="flexCheckIndeterminate">
                            <i class="fa-solid fa-trash-can"></i>
                        </label>
                    </div>
                `;
            }
        }, 1000);
    });
}