import { describe, it, expect } from 'vitest';
import { calculateProgressMetrics } from '../audio/progressMath';
import type { LiveJob } from '../types/liveJob';

describe('calculateProgressMetrics', () => {
  it('handles null job safely', () => {
    const metrics = calculateProgressMetrics(null, 0, []);
    expect(metrics.totalDuration).toBe(0.1);
    expect(metrics.processedFrontier).toBe(0);
    expect(metrics.bufferedFrontier).toBe(0);
    expect(metrics.playedPercent).toBe(0);
    expect(metrics.bufferedPercent).toBe(0);
  });

  it('uses job.video_duration as preferred total duration', () => {
    const mockJob: Partial<LiveJob> = {
      video_duration: 180,
      chunks: [
        { index: 0, status: 'ready', start_seconds: 0, end_seconds: 30 } as any,
      ],
    };
    const metrics = calculateProgressMetrics(mockJob as LiveJob, 30, [0]);
    expect(metrics.totalDuration).toBe(180);
    expect(metrics.playedPercent).toBe(16.666666666666664);
  });

  it('falls back to furthest chunk end_seconds if video_duration is missing', () => {
    const mockJob: Partial<LiveJob> = {
      video_duration: undefined,
      chunks: [
        { index: 0, status: 'ready', start_seconds: 0, end_seconds: 30 } as any,
        { index: 1, status: 'ready', start_seconds: 30, end_seconds: 60 } as any,
      ],
    };
    const metrics = calculateProgressMetrics(mockJob as LiveJob, 15, [0]);
    expect(metrics.totalDuration).toBe(60);
    expect(metrics.playedPercent).toBe(25);
  });

  it('normalizes derived duration and frontiers when the first chunk starts after zero', () => {
    const mockJob: Partial<LiveJob> = {
      video_duration: undefined,
      chunks: [
        { index: 0, status: 'ready', start_seconds: 8, end_seconds: 18 } as any,
        { index: 1, status: 'ready', start_seconds: 18, end_seconds: 28 } as any,
      ],
    };
    const metrics = calculateProgressMetrics(mockJob as LiveJob, 4, [0]);
    expect(metrics.totalDuration).toBe(20);
    expect(metrics.bufferedFrontier).toBe(10);
    expect(metrics.processedFrontier).toBe(20);
    expect(metrics.playedPercent).toBe(20);
  });

  it('calculates processed frontier from chunks with status === ready', () => {
    const mockJob: Partial<LiveJob> = {
      video_duration: 100,
      chunks: [
        { index: 0, status: 'ready', start_seconds: 0, end_seconds: 30 } as any,
        { index: 1, status: 'processing', start_seconds: 30, end_seconds: 60 } as any,
        { index: 2, status: 'ready', start_seconds: 60, end_seconds: 90 } as any,
      ],
    };
    const metrics = calculateProgressMetrics(mockJob as LiveJob, 0, []);
    expect(metrics.processedFrontier).toBe(90);
    expect(metrics.processedPercent).toBe(90);
  });

  it('calculates buffered frontier from chunks in bufferedChunks', () => {
    const mockJob: Partial<LiveJob> = {
      video_duration: 100,
      chunks: [
        { index: 0, status: 'ready', start_seconds: 0, end_seconds: 30 } as any,
        { index: 1, status: 'ready', start_seconds: 30, end_seconds: 60 } as any,
        { index: 2, status: 'ready', start_seconds: 60, end_seconds: 90 } as any,
      ],
    };
    const metrics = calculateProgressMetrics(mockJob as LiveJob, 0, [0, 2]); // chunk 1 is not buffered
    expect(metrics.bufferedFrontier).toBe(90); // max end_seconds among index 0 and 2
    expect(metrics.bufferedPercent).toBe(90);
  });

  it('clamps all percentages to 0..100', () => {
    const mockJob: Partial<LiveJob> = {
      video_duration: 100,
      chunks: [
        { index: 0, status: 'ready', start_seconds: 0, end_seconds: 120 } as any, // chunk ends past duration
      ],
    };
    // Playhead is past duration
    const metrics = calculateProgressMetrics(mockJob as LiveJob, 150, [0]);
    expect(metrics.playedPercent).toBe(100);
    expect(metrics.processedPercent).toBe(100);
    expect(metrics.bufferedPercent).toBe(100);
  });
});
