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
        
        // Enfocar automáticamente el campo de búsqueda cuando se abre el dropdown
        $(selectElement).on('select2:opening', function() {
            setTimeout(() => {
                const searchField = $('.select2-search__field, .select2-search input, .select2-container--open .select2-search__field');
                if (searchField.length > 0) {
                    searchField.focus();
                    searchField.trigger('focus');
                    searchField[0].focus();
                    console.log('Campo de búsqueda enfocado');
                } else {
                    console.log('No se encontró el campo de búsqueda');
                }
            }, 200);
        });
        
        // También intentar con el evento select2:open como respaldo
        $(selectElement).on('select2:open', function() {
            setTimeout(() => {
                const searchField = $('.select2-search__field, .select2-search input, .select2-container--open .select2-search__field');
                if (searchField.length > 0) {
                    searchField.focus();
                    searchField.trigger('focus');
                    searchField[0].focus();
                    console.log('Campo de búsqueda enfocado (respaldo)');
                }
            }, 100);
        });
        
        // Intentar enfoque con múltiples métodos después de que se abra completamente
        $(selectElement).on('select2:open', function() {
            setTimeout(() => {
                const searchField = $('.select2-search__field, .select2-search input, .select2-container--open .select2-search__field');
                if (searchField.length > 0) {
                    // Método 1: focus() de jQuery
                    searchField.focus();
                    // Método 2: focus() nativo
                    searchField[0].focus();
                    // Método 3: trigger focus
                    searchField.trigger('focus');
                    // Método 4: click para asegurar enfoque
                    searchField.click();
                    console.log('Enfoque múltiple aplicado');
                }
            }, 300);
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