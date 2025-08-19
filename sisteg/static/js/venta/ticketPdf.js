export function ticketPdf(servicio_id) {
    fetch(`/servicio/ticket-pdf/?servicio_id=${servicio_id}`).then(res => {
        // Verificar si la respuesta es exitosa
        if (!res.ok) {
            throw new Error(`Error HTTP! estado: ${res.status}`);
        }
        return res.blob();
    }).then(data => {
        console.log(data);
        // Crear URL del blob
        const blobUrl = URL.createObjectURL(data);

        // Abrir en nueva pestaña
        const newWindow = window.open(blobUrl, '_blank');

        // Esperar a que cargue el PDF
        newWindow.onload = () => {
            try {
                // Intentar imprimir
                newWindow.print();
            } catch (e) {
                console.error('Error al imprimir:', e);
                alert('El PDF se abrió pero no se pudo imprimir automáticamente');
            }

            // Limpiar recursos después de un tiempo
            setTimeout(() => {
                URL.revokeObjectURL(blobUrl);
            }, 5000);
        };
    });
}