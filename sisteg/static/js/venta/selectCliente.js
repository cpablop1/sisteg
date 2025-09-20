function initializeSelect2(selectElement, selectedValue = null) {
    // Verificar que jQuery y Select2 estén disponibles
    if (typeof $ !== 'undefined' && typeof $.fn.select2 !== 'undefined') {
        // Destruir Select2 si ya existe
        if ($(selectElement).hasClass('select2-hidden-accessible')) {
            $(selectElement).select2('destroy');
        }
        
        // Inicializar Select2
        $(selectElement).select2({
            theme: 'bootstrap-5',
            placeholder: 'Buscar cliente...',
            allowClear: true,
            language: {
                noResults: function() {
                    return "No se encontraron clientes";
                },
                searching: function() {
                    return "Buscando...";
                }
            }
        });
        
        // Establecer valor seleccionado después de la inicialización
        if (selectedValue) {
            $(selectElement).val(selectedValue).trigger('change');
        }
        
        return true;
    }
    return false;
}

export function selectCliente(selectedValue = null) {
    fetch('/servicio/listar-cliente/?select=select').then(res => res.json()).then(data => {
        const selectElement = document.getElementById('cliente_id');
        selectElement.innerHTML = '';
        
        // Agregar opción por defecto
        selectElement.add(new Option('Seleccione un cliente...', '', true, true));
        
        Array.from(data.data, item => {
            selectElement.add(new Option(`${item.nombres} ${item.apellidos}`, item.id));
        });
        
        // Intentar inicializar Select2 con retry
        let attempts = 0;
        const maxAttempts = 10;
        
        function tryInitialize() {
            if (initializeSelect2(selectElement, selectedValue)) {
                console.log('Select2 inicializado correctamente con valor:', selectedValue);
            } else if (attempts < maxAttempts) {
                attempts++;
                console.log(`Intento ${attempts} de inicializar Select2...`);
                setTimeout(tryInitialize, 100);
            } else {
                console.warn('No se pudo inicializar Select2 después de varios intentos. El select funcionará sin búsqueda.');
                // Establecer valor manualmente si Select2 no funciona
                if (selectedValue) {
                    selectElement.value = selectedValue;
                }
            }
        }
        
        tryInitialize();
    });
}