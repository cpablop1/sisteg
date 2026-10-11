export function analisisIa() {
    const btnAnalizarIa = document.getElementById("btnAnalizarIa");
    const btnCerrarAnalisisIa = document.getElementById("btnCerrarAnalisisIa");
    const btnDescartarAnalisisIa = document.getElementById("btnDescartarAnalisisIa");

    const descripcionInput = document.getElementById("observacion");
    const contadorDescripcion = document.getElementById("contadorDescripcion");

    const panelAnalisisIa = document.getElementById("panelAnalisisIa");
    const mensajeAnalisisIa = document.getElementById("mensajeAnalisisIa");

    const iaResumen = document.getElementById("iaResumen");
    const iaCategoria = document.getElementById("iaCategoria");
    const iaSubcategoria = document.getElementById("iaSubcategoria");
    const iaPrioridad = document.getElementById("iaPrioridad");
    const iaPosiblesCausas = document.getElementById("iaPosiblesCausas");
    const iaPreguntasSugeridas = document.getElementById("iaPreguntasSugeridas");
    const iaAdvertencia = document.getElementById("iaAdvertencia");

    /*
     * El último análisis generado se conserva temporalmente aquí.
     * Posteriormente se enviará cuando se cree el mantenimiento.
     */
    let analisisIaActual = null;

    /*
     * Guarda la descripción exacta que se utilizó para generar
     * el análisis. Esto permite detectar cambios posteriores.
     */
    let descripcionAnalizada = "";

    /* if (!btnAnalizarIa || !descripcionInput) {
        return;
    } */

    if (
        !descripcionInput ||
        !panelAnalisisIa ||
        !iaResumen ||
        !iaCategoria ||
        !iaSubcategoria ||
        !iaPrioridad ||
        !iaPosiblesCausas ||
        !iaPreguntasSugeridas ||
        !iaAdvertencia
    ) {
        console.warn(
            "No se encontraron todos los elementos necesarios para mostrar el análisis de IA."
        );

        return;
    }

    actualizarContador();

    descripcionInput.addEventListener("input", function () {
        actualizarContador();

        const descripcionActual = descripcionInput.value.trim();

        /*
         * Si ya existía un análisis y recepción modifica la descripción,
         * el análisis anterior deja de ser válido.
         */
        if (
            analisisIaActual !== null &&
            descripcionActual !== descripcionAnalizada
        ) {
            invalidarAnalisisAnterior();
        }
    });

    /* btnAnalizarIa.addEventListener("click", async function () {
        await analizarDescripcionConIa();
    }); */
    if (btnAnalizarIa) {
        btnAnalizarIa.addEventListener(
            "click",
            async function () {
                await analizarDescripcionConIa();
            }
        );
    }

    if (btnCerrarAnalisisIa) {
        btnCerrarAnalisisIa.addEventListener("click", function () {
            panelAnalisisIa.classList.add("d-none");
        });
    }

    if (btnDescartarAnalisisIa) {
        btnDescartarAnalisisIa.addEventListener("click", function () {
            descartarAnalisisIa();
        });
    }

    async function analizarDescripcionConIa() {
        const descripcion = descripcionInput.value.trim();
        const url = btnAnalizarIa.dataset.url;

        ocultarMensaje();

        if (!url) {
            mostrarMensaje(
                "No se encontró la dirección del servicio de análisis.",
                "danger"
            );
            return;
        }

        if (descripcion.length < 15) {
            mostrarMensaje(
                "Escriba una descripción más detallada. Debe contener al menos 15 caracteres.",
                "warning"
            );

            descripcionInput.focus();
            return;
        }

        if (descripcion.length > 2000) {
            mostrarMensaje(
                "La descripción no puede superar los 2000 caracteres.",
                "warning"
            );

            descripcionInput.focus();
            return;
        }

        activarCarga();

        try {
            const respuesta = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": obtenerCsrfToken(),
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: JSON.stringify({
                    descripcion: descripcion
                })
            });

            let datos;

            try {
                datos = await respuesta.json();
            } catch (error) {
                throw new Error(
                    "El servidor devolvió una respuesta que no es válida."
                );
            }

            if (!respuesta.ok) {
                throw new Error(
                    datos.mensaje ||
                    "No fue posible analizar la descripción."
                );
            }

            if (!datos.ok || !datos.analisis) {
                throw new Error(
                    datos.mensaje ||
                    "La respuesta no contiene el análisis esperado."
                );
            }

            analisisIaActual = datos.analisis;
            descripcionAnalizada = descripcion;

            renderizarAnalisis(datos.analisis);

            mostrarMensaje(
                datos.mensaje ||
                "La descripción fue analizada correctamente.",
                "success"
            );
        } catch (error) {
            console.error("Error al analizar con IA:", error);

            mostrarMensaje(
                error.message ||
                "Ocurrió un error inesperado al analizar la descripción.",
                "danger"
            );
        } finally {
            desactivarCarga();
        }
    }

    function renderizarAnalisis(analisis) {
        iaResumen.textContent =
            analisis.resumen || "Sin resumen";

        iaCategoria.textContent =
            analisis.categoria || "Sin categoría";

        iaCategoria.className =
            "badge bg-primary text-white p-2";

        iaSubcategoria.textContent =
            analisis.subcategoria || "Sin subcategoría";

        iaSubcategoria.className =
            "badge bg-secondary text-white p-2";

        configurarPrioridad(
            analisis.prioridad || "Sin prioridad"
        );

        renderizarLista(
            iaPosiblesCausas,
            analisis.posibles_causas,
            "No se identificaron posibles causas."
        );

        renderizarLista(
            iaPreguntasSugeridas,
            analisis.preguntas_sugeridas,
            "No se generaron preguntas sugeridas."
        );

        iaAdvertencia.textContent =
            analisis.advertencia ||
            "El análisis es preliminar y debe ser validado por el técnico.";

        panelAnalisisIa.classList.remove("d-none");

        panelAnalisisIa.scrollIntoView({
            behavior: "smooth",
            block: "nearest"
        });
    }

    function renderizarLista(elemento, valores, mensajeVacio) {
        elemento.innerHTML = "";

        if (!Array.isArray(valores) || valores.length === 0) {
            const item = document.createElement("li");
            item.textContent = mensajeVacio;
            elemento.appendChild(item);
            return;
        }

        valores.forEach(function (valor) {
            const item = document.createElement("li");
            item.textContent = valor;
            item.classList.add("mb-1");

            elemento.appendChild(item);
        });
    }

    function configurarPrioridad(prioridad) {
        iaPrioridad.textContent = prioridad;

        iaPrioridad.classList.remove(
            "bg-success",
            "bg-info",
            "bg-warning",
            "bg-danger",
            "bg-secondary",
            "text-dark",
            "text-white"
        );

        const prioridadNormalizada = prioridad
            .toString()
            .trim()
            .toLowerCase();

        switch (prioridadNormalizada) {
            case "baja":
                iaPrioridad.classList.add(
                    "bg-success",
                    "text-white"
                );
                break;

            case "media":
                iaPrioridad.classList.add(
                    "bg-info",
                    "text-dark"
                );
                break;

            case "alta":
                iaPrioridad.classList.add(
                    "bg-warning",
                    "text-dark"
                );
                break;

            case "crítica":
            case "critica":
                iaPrioridad.classList.add(
                    "bg-danger",
                    "text-white"
                );
                break;

            default:
                iaPrioridad.classList.add(
                    "bg-secondary",
                    "text-white"
                );
                break;
        }
    }

    /* function activarCarga() {
        btnAnalizarIa.disabled = true;

        btnAnalizarIa.dataset.textoOriginal =
            btnAnalizarIa.innerHTML;

        btnAnalizarIa.innerHTML = `
            <span
                class="spinner-border spinner-border-sm me-1"
                role="status"
                aria-hidden="true"
            ></span>
            Analizando...
        `;

        descripcionInput.readOnly = true;
    } */

    function activarCarga() {
        if (!btnAnalizarIa) {
            return;
        }

        btnAnalizarIa.disabled = true;

        btnAnalizarIa.dataset.textoOriginal =
            btnAnalizarIa.innerHTML;

        btnAnalizarIa.innerHTML = `
                <span
                    class="spinner-border spinner-border-sm me-1"
                    role="status"
                    aria-hidden="true"
                ></span>
                Analizando...
            `;

        descripcionInput.readOnly = true;
    }

    /* function desactivarCarga() {
        btnAnalizarIa.disabled = false;

        btnAnalizarIa.innerHTML =
            btnAnalizarIa.dataset.textoOriginal ||
            '<i class="fas fa-magic"></i> Analizar con IA';

        descripcionInput.readOnly = false;
    } */
    function desactivarCarga() {
        if (!btnAnalizarIa) {
            return;
        }

        btnAnalizarIa.disabled = false;

        btnAnalizarIa.innerHTML =
            btnAnalizarIa.dataset.textoOriginal ||
            '<i class="fas fa-magic"></i> Analizar con IA';

        descripcionInput.readOnly = false;
    }

    function invalidarAnalisisAnterior() {
        analisisIaActual = null;
        descripcionAnalizada = "";

        panelAnalisisIa.classList.add("d-none");

        mostrarMensaje(
            "La descripción fue modificada. Vuelva a analizarla para actualizar las sugerencias de IA.",
            "warning"
        );
    }

    function descartarAnalisisIa() {
        analisisIaActual = null;
        descripcionAnalizada = "";

        limpiarPanel();
        panelAnalisisIa.classList.add("d-none");

        mostrarMensaje(
            "El análisis generado por IA fue descartado.",
            "secondary"
        );
    }

    function limpiarPanel() {
        iaResumen.textContent = "";
        iaCategoria.textContent = "";
        iaSubcategoria.textContent = "";
        iaPrioridad.textContent = "";
        iaPosiblesCausas.innerHTML = "";
        iaPreguntasSugeridas.innerHTML = "";
        iaAdvertencia.textContent = "";
    }

    function actualizarContador() {
        if (!contadorDescripcion) {
            return;
        }

        contadorDescripcion.textContent =
            descripcionInput.value.length;
    }

    function mostrarMensaje(mensaje, tipo) {
        if(mensajeAnalisisIa){
            mensajeAnalisisIa.className =
                `alert alert-${tipo} mt-3`;
    
            mensajeAnalisisIa.textContent = mensaje;
            mensajeAnalisisIa.classList.remove("d-none");
        }
    }

    function ocultarMensaje() {
        mensajeAnalisisIa.textContent = "";
        mensajeAnalisisIa.className = "mt-3 d-none";
    }

    function obtenerCsrfToken() {
        /*
         * Primera opción:
         * busca el token dentro del formulario de Django.
         */
        const tokenFormulario = document.querySelector(
            '[name="csrfmiddlewaretoken"]'
        );

        if (tokenFormulario) {
            return tokenFormulario.value;
        }

        /*
         * Segunda opción:
         * busca la cookie csrftoken.
         */
        const cookies = document.cookie
            ? document.cookie.split(";")
            : [];

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith("csrftoken=")) {
                return decodeURIComponent(
                    cookie.substring("csrftoken=".length)
                );
            }
        }

        return "";
    }

    /*
     * Dejamos disponible una función controlada para que el código
     * que crea el mantenimiento pueda obtener el análisis.
     */
    window.obtenerAnalisisIaMantenimiento = function () {
        return analisisIaActual;
    };

    window.cargarAnalisisIaMantenimiento = function (
        analisis,
        descripcionOriginal = "",
        fechaAnalisis = null
    ) {
        let analisisProcesado = analisis;

        // Si el backend envía el JSON como texto, convertirlo en objeto
        if (typeof analisisProcesado === "string") {
            try {
                analisisProcesado = JSON.parse(analisisProcesado);
            } catch (error) {
                console.error(
                    "El análisis guardado no contiene un JSON válido:",
                    error
                );

                analisisProcesado = null;
            }
        }

        // Si el servicio no tiene análisis de IA, ocultar el panel
        if (
            !analisisProcesado ||
            typeof analisisProcesado !== "object" ||
            Array.isArray(analisisProcesado) ||
            Object.keys(analisisProcesado).length === 0
        ) {
            analisisIaActual = null;
            descripcionAnalizada = "";

            limpiarPanel();
            ocultarMensaje();

            panelAnalisisIa.classList.add("d-none");

            if (btnAnalizarIa) {
                btnAnalizarIa.innerHTML = `
                    <i class="fas fa-magic"></i>
                    Analizar nuevamente
                `;
            }

            return;
        }

        // Guardar el análisis cargado en el estado de JavaScript
        analisisIaActual = analisisProcesado;

        // Asociar el análisis con la descripción guardada
        descripcionAnalizada = (
            descripcionOriginal ||
            descripcionInput.value ||
            ""
        ).trim();

        // Mostrar el análisis en el panel
        renderizarAnalisis(analisisProcesado);

        // Actualizar el contador del textarea
        actualizarContador();

        // Cambiar el texto del botón
        if (btnAnalizarIa) {
            btnAnalizarIa.innerHTML = `
                <i class="fas fa-magic"></i>
                Analizar nuevamente
            `;
        }

        // Mostrar mensaje con la fecha del análisis, si existe
        if (fechaAnalisis) {
            const fecha = new Date(fechaAnalisis);

            const fechaFormateada = fecha.toLocaleString(
                "es-GT",
                {
                    dateStyle: "medium",
                    timeStyle: "short"
                }
            );

            mostrarMensaje(
                `Análisis de IA guardado el ${fechaFormateada}.`,
                "info"
            );
        } else {
            mostrarMensaje(
                "Se cargó el análisis de IA guardado para este mantenimiento.",
                "info"
            );
        }
    };

    /*
     * Esta función será útil cuando el formulario se limpie
     * después de crear el mantenimiento.
     */
    window.limpiarAnalisisIaMantenimiento = function () {
        analisisIaActual = null;
        descripcionAnalizada = "";

        limpiarPanel();
        ocultarMensaje();

        panelAnalisisIa.classList.add("d-none");

        if (btnAnalizarIa) {
            btnAnalizarIa.innerHTML = `
                <i class="fas fa-magic"></i>
                Analizar con IA
            `;
        }
    };
}