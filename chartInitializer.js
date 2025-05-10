// Import Runtime and Inspector once
import {Runtime, Inspector} from "./zoomable-sunburst/runtime.js";

/**
* Initializes a chart by dynamically importing the module and rendering it into the target container.
* @param {string} modulePath - The path to the module file.
* @param {string} targetSelector - The CSS selector for the target container.
*/
async function initializeChart(modulePath, targetSelector) {
    try {
        const define = (await import(modulePath + "/index.js")).default;
        if (!define || typeof define !== "function") {
            throw new Error(`Invalid or missing define function in module: ${modulePath}`);
        }
        const target = document.querySelector(targetSelector);
        if (!target) {
            throw new Error(`Target container not found: ${targetSelector}`);
        }
        const runtime = new Runtime();
        runtime.module(define, Inspector.into(target));
    } catch (error) {
        console.error("Error initializing chart:", error);
        throw error; // Re-throw the error for retry logic
    }
}

/**
* Delays execution for a specified number of milliseconds.
* @param {number} ms - The delay in milliseconds.
* @returns {Promise < void >}
*/
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
* Tries to initialize a chart until it succeeds.
* @param {string} modulePath - The path to the module file.
* @param {string} targetSelector - The CSS selector for the target container.
*/
async function tryInitializeChart(modulePath, targetSelector) {
    let success = false;
    while (!success) {
        try {
            await initializeChart(modulePath, targetSelector);
            success = true; // If no error, mark as successful
        } catch (error) {
            console.error(`Retrying chart initialization for ${targetSelector}:`, error);
            await delay(500); // Wait 500ms before retrying
        }
    }
}

export { initializeChart, tryInitializeChart };