export type PlaybackState =
  | 'idle'
  | 'waiting_chunk_0'
  | 'buffering'
  | 'playing'
  | 'waiting_next_chunk'
  | 'stopped'
  | 'completed'
  | 'error';

export interface DecodedChunk {
  index: number;
  buffer: AudioBuffer;
  duration: number; // decoded buffer duration in seconds
  startSeconds: number; // original chunk start time in seconds
  endSeconds: number; // original chunk end time in seconds
}

export interface ScheduledChunk {
  index: number;
  sourceNode: AudioBufferSourceNode;
  gainNode: GainNode;
  scheduledStartTime: number; // AudioContext time
  scheduledEndTime: number; // AudioContext time
  displayStartTime: number; // UI playback time, independent from source timestamps
  displayEndTime: number; // UI playback time, independent from source timestamps
  duration: number;
}

export interface CrossfadePlan {
  fadeInStart: number;
  fadeInEnd: number;
  fadeOutStart: number;
  fadeOutEnd: number;
  playStartTime: number;
  playDuration: number;
  bufferOffset: number; // position within the buffer to start playing (usually 0, unless resuming)
}

export interface PlayerError {
  message: string;
  chunkIndex?: number;
  details?: string;
}

export interface SchedulerDecision {
  action: 'schedule' | 'wait' | 'complete' | 'error';
  chunkIndex?: number;
  scheduledStartTime?: number;
  reason?: string;
}
