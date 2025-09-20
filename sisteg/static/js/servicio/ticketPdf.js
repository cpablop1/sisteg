export function ticketPdf(servicio_id) {
    const url = `/servicio/ticket-pdf/?servicio_id=${servicio_id}`;
    let imprimir = window.open(url, '_blank');
    imprimir.print();
}