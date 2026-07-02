import type { LiveJob } from '../types/liveJob';

export interface ProgressMetrics {
  totalDuration: number;
  processedFrontier: number;
  bufferedFrontier: number;
  playedPercent: number;
  bufferedPercent: number;
  processedPercent: number;
}

function getTimelineOrigin(job: LiveJob): number {
  if (job.chunks.length === 0) return 0;
  return Math.min(...job.chunks.map((chunk) => chunk.start_seconds));
}

function normalizeSeconds(seconds: number, origin: number): number {
  return Math.max(0, seconds - origin);
}

export function calculateProgressMetrics(
  job: LiveJob | null,
  playheadSeconds: number,
  bufferedChunks: number[]
): ProgressMetrics {
  if (!job) {
    return {
      totalDuration: 0.1,
      processedFrontier: 0,
      bufferedFrontier: 0,
      playedPercent: 0,
      bufferedPercent: 0,
      processedPercent: 0,
    };
  }

  const origin = getTimelineOrigin(job);

  // 1. Calculate total duration
  let totalDuration = job.video_duration || 0;
  if (totalDuration <= 0 && job.chunks.length > 0) {
    totalDuration = normalizeSeconds(Math.max(...job.chunks.map(c => c.end_seconds)), origin);
  }
  totalDuration = Math.max(0.1, totalDuration); // Avoid division by zero

  // 2. Calculate processed frontier (backend ready)
  const readyChunks = job.chunks.filter(c => c.status === 'ready');
  const processedFrontier = readyChunks.length > 0
    ? normalizeSeconds(Math.max(...readyChunks.map(c => c.end_seconds)), origin)
    : 0;

  // 3. Calculate buffered frontier (browser decoded)
  const bufferedChunkObjects = job.chunks.filter(c => bufferedChunks.includes(c.index));
  const bufferedFrontier = bufferedChunkObjects.length > 0
    ? normalizeSeconds(Math.max(...bufferedChunkObjects.map(c => c.end_seconds)), origin)
    : 0;

  const clamp = (val: number, min: number, max: number): number => {
    return Math.max(min, Math.min(max, val));
  };

  // 4. Calculate percentages
  const playedPercent = clamp((playheadSeconds / totalDuration) * 100, 0, 100);
  const bufferedPercent = clamp((bufferedFrontier / totalDuration) * 100, 0, 100);
  const processedPercent = clamp((processedFrontier / totalDuration) * 100, 0, 100);

  return {
    totalDuration,
    processedFrontier,
    bufferedFrontier,
    playedPercent,
    bufferedPercent,
    processedPercent,
  };
}
