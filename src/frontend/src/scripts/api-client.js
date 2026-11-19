// src/scripts/api-client.js

// Punto unico de configuracion:  cambiar la costatnte i se llega a definir otra subruta (ej. '/api/mensaje')

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
export async function fetchBackendMessage() {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(API_ENDPOINT, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
      signal: controller.signal,
    });

    if (!response.ok) {
      throw new Error(`El servidor respondió con estado HTTP ${response.status} (${response.statusText || 'Error'})`);
    }

    const json = await response.json();
    return extractMessage(json);
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('Tiempo de espera agotado (5s). Verifica que el backend y PostgreSQL estén activos.');
    }
    throw error;
  } finally {
    clearTimeout(timeoutId);
  }
}