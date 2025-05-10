// Con cargar un módulo cualquiera de D3.js ya podemos usarlo para el resto de gráficos
import {Runtime, Inspector} from "./charts/zoomable-sunburst/runtime.js";

/**
* Inicializa un gráfico utilizando el módulo especificado.
* @param {string} modulePath - El path de la carpeta del módulo.
* @param {string} targetSelector - El selector CSS del contenedor objetivo.
*/
async function initializeChart(modulePath, targetSelector) {
    try {
        const define = (await import(modulePath + "/index.js")).default;
        if (!define || typeof define !== "function") {
            throw new Error(`Función no reconocida en el módulo: ${modulePath}`);
        }
        const target = document.querySelector(targetSelector);
        if (!target) {
            throw new Error(`No se ha encontrado la carpeta del gráfico: ${targetSelector}`);
        }
        const runtime = new Runtime();
        runtime.module(define, Inspector.into(target));
    } catch (error) {
        console.error("Error al inicializar el gráfico:", error);
        throw error; // Re-throw the error for retry logic
    }
}

/**
* Espera un tiempo específico antes de continuar.
* @param {number} ms - El tiempo en milisegundos a esperar.
* @returns {Promise < void >}
*/
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
* Intenta inicializar un gráfico con reintentos. Esto es nos has sido necesario dado que había veces que un error
 * hacía que no se cargase el gráfico por lo que preferimos reintentarlo. No suele necesitar más de 1 o 2 reintentos.
* @param {string} modulePath - El path de la carpeta del módulo.
* @param {string} targetSelector - El selector CSS del contenedor objetivo.
*/
async function tryInitializeChart(modulePath, targetSelector) {
    let success = false;
    let attempts = 0;
    while (!success && attempts < 3) {
        try {
            await initializeChart(modulePath, targetSelector);
            success = true; // If no error, mark as successful
        } catch (error) {
            console.error(`Reintentando para ${targetSelector}:`, error);
            await delay(500); // Wait 500ms before retrying
        }
    }
    if (!success) {
        console.error(`No se ha podido cargar el gráfico después de ${attempts} intentos.`);
    }
}

export { tryInitializeChart };