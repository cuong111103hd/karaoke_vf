/**
 * Decodes the raw audio ArrayBuffer into an AudioBuffer using the provided AudioContext.
 */
export async function decodeAudio(
  audioContext: AudioContext,
  arrayBuffer: ArrayBuffer
): Promise<AudioBuffer> {
  // Newer browsers return a Promise from decodeAudioData.
  // Older browsers might use callback style, but standard modern environments support Promise.
  try {
    return await audioContext.decodeAudioData(arrayBuffer);
  } catch (error) {
    throw new Error(`Audio decoding failed: ${error instanceof Error ? error.message : String(error)}`);
  }
}
