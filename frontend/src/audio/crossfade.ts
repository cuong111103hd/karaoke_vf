import type { CrossfadePlan } from './playbackTypes';

/**
 * Calculates start times, durations, and gain automation schedules for a chunk.
 */
export function calculateCrossfadePlan(params: {
  startTime: number; // expected start time in AudioContext timeline
  duration: number; // duration of the current chunk buffer in seconds
  overlap: number; // overlap setting in seconds
  isFirst: boolean;
  hasNext: boolean;
}): CrossfadePlan {
  const { startTime, duration, overlap, isFirst, hasNext } = params;

  // Ensure overlap is sane and does not exceed duration
  const safeOverlap = Math.max(0, Math.min(overlap, duration));

  const playStartTime = startTime;
  const playDuration = duration;
  const endTime = startTime + duration;

  // Fade-in occurs at the start of the chunk if it's not the first chunk (crossfading with previous)
  const fadeInStart = startTime;
  const fadeInEnd = isFirst ? startTime : startTime + safeOverlap;

  // Fade-out occurs at the end of the chunk if there is a next chunk coming
  const fadeOutStart = hasNext ? endTime - safeOverlap : endTime;
  const fadeOutEnd = endTime;

  return {
    fadeInStart,
    fadeInEnd,
    fadeOutStart,
    fadeOutEnd,
    playStartTime,
    playDuration,
    bufferOffset: 0,
  };
}

/**
 * Helper to apply gain scheduling to a WebAudio GainNode based on a plan.
 */
export function applyGainPlan(
  gainNode: GainNode,
  plan: CrossfadePlan,
  audioContextTime: number
): void {
  const { fadeInStart, fadeInEnd, fadeOutStart, fadeOutEnd } = plan;
  const gainParam = gainNode.gain;

  // Clear any existing schedules
  gainParam.cancelScheduledValues(audioContextTime);

  // Default is full volume (1.0) unless it's fading in
  if (fadeInEnd > fadeInStart) {
    gainParam.setValueAtTime(0, Math.max(audioContextTime, fadeInStart));
    gainParam.linearRampToValueAtTime(1, Math.max(audioContextTime, fadeInEnd));
  } else {
    gainParam.setValueAtTime(1, Math.max(audioContextTime, fadeInStart));
  }

  // Fade-out schedule
  if (fadeOutEnd > fadeOutStart) {
    gainParam.setValueAtTime(1, Math.max(audioContextTime, fadeOutStart));
    gainParam.linearRampToValueAtTime(0, Math.max(audioContextTime, fadeOutEnd));
  }
}
