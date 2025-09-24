export function estadistica() {
    fetch('/estadistica/').then(data => data.json()).then(data => {
        let div = document.getElementById('estadistica');
        let grafica = document.getElementById('grafica');
        div.innerHTML = '';
        // Mostrando datos de compra
        div.insertAdjacentHTML("beforeend",
            `<div class="col">
                <div class="card">
                    <div class="card-header">Compras</div>
                    <div class="card-body">
                        <h5 class="card-title">${data.compra[0].total}</h5>
                        <p class="card-text">${data.compra[0].cantidad}</p>
                    </div>
                </div>
            </div>`
        );
        // Mostrando datos de servicio
        data.servicio.forEach(servicio => {
            let titulo = servicio.tipo_servicio.charAt(0).toUpperCase() + servicio.tipo_servicio.slice(1);
            div.insertAdjacentHTML("beforeend",
                `<div class="col">
                <div class="card">
                    <div class="card-header">${titulo}</div>
                    <div class="card-body">
                        <h5 class="card-title">${servicio.total}</h5>
                        <p class="card-text">${servicio.cantidad}</p>
                    </div>
                </div>
            </div>`
            );
        });

        // Mostrar gráfica
        let descripcion = []
        let cantidad = [];
        data.grafica.forEach(items => {
            descripcion.push(items.descripcion);
            cantidad.push(items.cantidad);
        });
        new Chart(grafica, {
            type: 'polarArea',
            data: {
                labels: descripcion,
                datasets: [{
                    label: 'Gráfica',
                    data: cantidad,
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: false
                    }
                }
            }
        });
    });
}