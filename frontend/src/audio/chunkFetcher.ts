/**
 * Fetches the audio bytes of a ready chunk as an ArrayBuffer.
 * @param url The full browser-fetchable URL of the chunk's instrumental audio.
 */
export async function fetchChunkAudio(url: string): Promise<ArrayBuffer> {
  const targetUrl = url.startsWith('/') ? `http://localhost:8000${url}` : url;
  const response = await fetch(targetUrl);
  if (!response.ok) {
    throw new Error(`Failed to fetch chunk audio from ${targetUrl}: Status ${response.status}`);
  }
  return response.arrayBuffer();
}
