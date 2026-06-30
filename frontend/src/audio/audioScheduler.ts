import type { SchedulerDecision } from './playbackTypes';

/**
 * pure timeline scheduler that decides the next action based on available chunks and playback state.
 */
export function determineNextAction(params: {
  nextIndex: number;
  audioContextTime: number;
  lastChunkEndTime: number | null; // AudioContext time when the last scheduled chunk ends
  decodedChunks: Map<number, { duration: number }>;
  overlap: number;
  jobStatus: 'starting' | 'queued' | 'active' | 'completed' | 'failed' | 'idle';
  hasMoreChunks: boolean; // whether there are more chunks expected in the future
  lookahead: number; // small delay (in seconds) to schedule future playbacks reliably
}): SchedulerDecision {
  const {
    nextIndex,
    audioContextTime,
    lastChunkEndTime,
    decodedChunks,
    overlap,
    jobStatus,
    hasMoreChunks,
    lookahead,
  } = params;

  // 1. If job failed, stop playback with error
  if (jobStatus === 'failed') {
    return {
      action: 'error',
      reason: 'Live job failed on backend.',
    };
  }

  // 2. Check if we have the chunk decoded
  const chunk = decodedChunks.get(nextIndex);

  if (!chunk) {
    // Chunk is NOT decoded yet.
    // Are there more chunks expected?
    if (hasMoreChunks || jobStatus === 'starting' || jobStatus === 'queued' || jobStatus === 'active') {
      return {
        action: 'wait',
        chunkIndex: nextIndex,
        reason: `Waiting for chunk ${nextIndex} to be ready and decoded.`,
      };
    } else {
      // No more chunks expected and not in active/starting states (i.e. completed)
      return {
        action: 'complete',
        reason: 'All chunks have finished playing.',
      };
    }
  }

  // 3. Chunk is decoded. Let's calculate its start time.
  let startTime = audioContextTime + lookahead;

  if (lastChunkEndTime !== null) {
    const expectedStartTime = lastChunkEndTime - overlap;
    // If the expected start time is in the future, or close enough to be scheduled, use it
    if (expectedStartTime >= audioContextTime) {
      startTime = expectedStartTime;
    } else {
      // We are late (probably due to waiting/stalling). Schedule with lookahead.
      startTime = audioContextTime + lookahead;
    }
  }

  return {
    action: 'schedule',
    chunkIndex: nextIndex,
    scheduledStartTime: startTime,
  };
}
