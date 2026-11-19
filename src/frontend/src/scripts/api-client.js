// src/scripts/api-client.js

const API_ENDPOINT = '/api';
const REQUEST_TIMEOUT_MS = 5000

/**
 * Extrae el texto del mensaje sin importar pequeñas variaciones en el contrato JSON.
 */

function extractMessage(payload) {
    if (typeof payload === 'string') return payload;

    // Si el backend devuelve una lista de filas (ej. [{"mensaje": "Hola Mundo"}])
    const data = Array.isArray(payload) ? payload[0] : payload

    if (data && typeof data === 'object') {
    return (
      data.mensaje ??
      data.message ??
      data.texto ??
      data.text ??
      data.content ??
      JSON.stringify(data)
    );
  }

  throw new Error('El formato del JSON recibido no contiene un mensaje legible.');

} 

/**
 * Consulta el endpoint del backend usando ruta relativa.
 */
export async function testEndToEndFlow() {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  const startTime = performance.now();

  try {
    const response = await fetch(API_ENDPOINT, {
      method: 'GET',
      headers: { Accept: 'application/json' },
      signal: controller.signal,
    });

    const latencyMs = Math.round(performance.now() - startTime);

    if (!response.ok) {
      const err = new Error(`HTTP ${response.status} (${response.statusText || 'Error de servidor'})`);
      err.status = response.status;
      throw err;
    }

    const json = await response.json();
    return {
      message: extractMessage(json),
      status: response.status,
      latencyMs,
    };
  } catch (error) {
    if (error.name === 'AbortError') {
      const timeoutErr = new Error('Timeout (5s): El servidor no respondió a tiempo.');
      timeoutErr.status = 504;
      throw timeoutErr;
    }
    throw error;
  } finally {
    clearTimeout(timeoutId);
  }
}