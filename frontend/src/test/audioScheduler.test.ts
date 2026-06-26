import { describe, it, expect } from 'vitest';
import { determineNextAction } from '../audio/audioScheduler';
import { calculateCrossfadePlan } from '../audio/crossfade';

describe('determineNextAction', () => {
  const decodedChunks = new Map<number, { duration: number }>();
  decodedChunks.set(0, { duration: 10 });
  decodedChunks.set(1, { duration: 10 });

  it('handles job failures immediately', () => {
    const decision = determineNextAction({
      nextIndex: 0,
      audioContextTime: 0.0,
      lastChunkEndTime: null,
      decodedChunks,
      overlap: 1.0,
      jobStatus: 'failed',
      hasMoreChunks: true,
      lookahead: 0.1,
    });
    expect(decision.action).toBe('error');
    expect(decision.reason).toContain('failed');
  });

  it('enters waiting state if the next chunk is not ready/decoded', () => {
    const decision = determineNextAction({
      nextIndex: 2, // not in decodedChunks
      audioContextTime: 5.0,
      lastChunkEndTime: 10.0,
      decodedChunks,
      overlap: 1.0,
      jobStatus: 'active',
      hasMoreChunks: true,
      lookahead: 0.1,
    });
    expect(decision.action).toBe('wait');
    expect(decision.chunkIndex).toBe(2);
  });

  it('completes playback when no more chunks are expected and current chunk not available', () => {
    const decision = determineNextAction({
      nextIndex: 2, // not in decodedChunks
      audioContextTime: 12.0,
      lastChunkEndTime: 10.0,
      decodedChunks,
      overlap: 1.0,
      jobStatus: 'completed',
      hasMoreChunks: false,
      lookahead: 0.1,
    });
    expect(decision.action).toBe('complete');
  });

  it('schedules chunk 0 at start time with lookahead', () => {
    const decision = determineNextAction({
      nextIndex: 0,
      audioContextTime: 0.0,
      lastChunkEndTime: null,
      decodedChunks,
      overlap: 1.0,
      jobStatus: 'active',
      hasMoreChunks: true,
      lookahead: 0.1,
    });
    expect(decision.action).toBe('schedule');
    expect(decision.chunkIndex).toBe(0);
    expect(decision.scheduledStartTime).toBe(0.1);
  });

  it('schedules chunk 1 with overlap crossfade timing', () => {
    // chunk 0 ended at 10.1, next starts at 10.1 - 1.0 = 9.1
    const decision = determineNextAction({
      nextIndex: 1,
      audioContextTime: 5.0,
      lastChunkEndTime: 10.1,
      decodedChunks,
      overlap: 1.0,
      jobStatus: 'active',
      hasMoreChunks: true,
      lookahead: 0.1,
    });
    expect(decision.action).toBe('schedule');
    expect(decision.chunkIndex).toBe(1);
    expect(decision.scheduledStartTime).toBe(9.1);
  });

  it('handles late scheduling and recovers with lookahead if too late', () => {
    // chunk 0 ended at 10.1, expected start is 9.1. But current time is 9.5.
    // It should schedule at 9.5 + 0.1 = 9.6
    const decision = determineNextAction({
      nextIndex: 1,
      audioContextTime: 9.5,
      lastChunkEndTime: 10.1,
      decodedChunks,
      overlap: 1.0,
      jobStatus: 'active',
      hasMoreChunks: true,
      lookahead: 0.1,
    });
    expect(decision.action).toBe('schedule');
    expect(decision.chunkIndex).toBe(1);
    expect(decision.scheduledStartTime).toBe(9.6);
  });
});

describe('calculateCrossfadePlan', () => {
  it('calculates plan with no overlap', () => {
    const plan = calculateCrossfadePlan({
      startTime: 5.0,
      duration: 10.0,
      overlap: 0.0,
      isFirst: true,
      hasNext: true,
    });
    expect(plan.playStartTime).toBe(5.0);
    expect(plan.playDuration).toBe(10.0);
    expect(plan.fadeInEnd).toBe(5.0);
    expect(plan.fadeOutStart).toBe(15.0);
  });

  it('calculates plan with one-second overlap for chunk 0', () => {
    const plan = calculateCrossfadePlan({
      startTime: 0.0,
      duration: 10.0,
      overlap: 1.0,
      isFirst: true,
      hasNext: true,
    });
    // Chunk 0 has no preceding chunk, so fadeInEnd equals startTime (no fade in)
    expect(plan.fadeInEnd).toBe(0.0);
    // Since hasNext is true, it fades out in the last second
    expect(plan.fadeOutStart).toBe(9.0);
    expect(plan.fadeOutEnd).toBe(10.0);
  });

  it('calculates plan with one-second overlap for subsequent chunk', () => {
    const plan = calculateCrossfadePlan({
      startTime: 9.0,
      duration: 10.0,
      overlap: 1.0,
      isFirst: false,
      hasNext: false,
    });
    // Subsequent chunk fades in over overlap window
    expect(plan.fadeInStart).toBe(9.0);
    expect(plan.fadeInEnd).toBe(10.0);
    // Since hasNext is false, no fade out at end
    expect(plan.fadeOutStart).toBe(19.0);
    expect(plan.fadeOutEnd).toBe(19.0);
  });
});
