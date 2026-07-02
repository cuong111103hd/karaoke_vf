import { useState, useEffect, useRef, useCallback } from 'react';
import type { LiveJob } from '../types/liveJob';
import type { PlaybackState, DecodedChunk, ScheduledChunk, PlayerError } from './playbackTypes';
import { fetchChunkAudio } from './chunkFetcher';
import { decodeAudio } from './audioDecoder';
import { calculateCrossfadePlan, applyGainPlan } from './crossfade';
import { determineNextAction } from './audioScheduler';

export function useLivePlayback(job: LiveJob | null) {
  const [playbackState, setPlaybackState] = useState<PlaybackState>('idle');
  const [error, setError] = useState<PlayerError | null>(null);
  const [currentChunkIndex, setCurrentChunkIndex] = useState<number | null>(null);
  const [bufferedChunks, setBufferedChunks] = useState<number[]>([]);
  const [playheadSeconds, setPlayheadSeconds] = useState<number>(0);

  // WebAudio references
  const audioContextRef = useRef<AudioContext | null>(null);
  const scheduledChunksRef = useRef<Map<number, ScheduledChunk>>(new Map());
  const decodedChunksRef = useRef<Map<number, DecodedChunk>>(new Map());

  // Scheduler state references
  const isArmedRef = useRef<boolean>(false);
  const nextIndexRef = useRef<number>(0);
  const lastChunkEndTimeRef = useRef<number | null>(null);
  const lastDisplayEndTimeRef = useRef<number | null>(null);
  const playbackClockStartTimeRef = useRef<number | null>(null);
  const activeChunkIndexRef = useRef<number | null>(null);

  // Keep track of which indices we're currently fetching to avoid duplicates
  const fetchingIndicesRef = useRef<Set<number>>(new Set());
  const animationFrameIdRef = useRef<number | null>(null);

  // Keep track of active timeouts for UI updates & completion
  const timeoutsRef = useRef<number[]>([]);

  const addTimeout = useCallback((cb: () => void, delayMs: number) => {
    const id = window.setTimeout(cb, delayMs);
    timeoutsRef.current.push(id);
    return id;
  }, []);

  const clearAllTimeouts = useCallback(() => {
    timeoutsRef.current.forEach((id) => clearTimeout(id));
    timeoutsRef.current = [];
  }, []);

  const cancelAnimation = useCallback(() => {
    if (animationFrameIdRef.current !== null) {
      cancelAnimationFrame(animationFrameIdRef.current);
      animationFrameIdRef.current = null;
    }
  }, []);

  // Stop playback and release resources
  const stop = useCallback(() => {
    isArmedRef.current = false;
    clearAllTimeouts();
    cancelAnimation();
    setPlayheadSeconds(0);

    // Stop all scheduled WebAudio nodes
    scheduledChunksRef.current.forEach((sc) => {
      try {
        sc.sourceNode.stop();
        sc.sourceNode.disconnect();
        sc.gainNode.disconnect();
      } catch {
        // Source node might not have started or already stopped
      }
    });
    scheduledChunksRef.current.clear();

    // Reset scheduling refs
    nextIndexRef.current = 0;
    lastChunkEndTimeRef.current = null;
    lastDisplayEndTimeRef.current = null;
    playbackClockStartTimeRef.current = null;
    activeChunkIndexRef.current = null;

    // Transition state
    setPlaybackState('stopped');
    setCurrentChunkIndex(null);
  }, [clearAllTimeouts, cancelAnimation]);

  // Completely reset the cache (when selecting a new job)
  const resetCache = useCallback(() => {
    stop();
    decodedChunksRef.current.clear();
    fetchingIndicesRef.current.clear();
    setBufferedChunks([]);
    setError(null);
    setPlayheadSeconds(0);
    setPlaybackState('idle');
  }, [stop]);

  // Main scheduler execution step
  const runSchedulerTick = useCallback(() => {
    if (!audioContextRef.current) return;
    if (playbackState === 'error') return;

    // If the player isn't armed (i.e. user has not clicked Play), do not schedule
    if (!isArmedRef.current) return;

    const audioContext = audioContextRef.current;
    const now = audioContext.currentTime;

    // Ensure audio context is running
    if (audioContext.state === 'suspended') {
      audioContext.resume().catch((err) => {
        console.error('Failed to resume AudioContext:', err);
      });
    }

    let loop = true;
    while (loop) {
      const currentNextIndex = nextIndexRef.current;
      const lastEndTime = lastChunkEndTimeRef.current;

      // Determine if there are more chunks expected in the future
      let hasMoreChunks = false;
      if (job) {
        if (job.status !== 'completed' && job.status !== 'failed') {
          hasMoreChunks = true;
        } else {
          hasMoreChunks = currentNextIndex < job.chunks.length;
        }
      }

      const decision = determineNextAction({
        nextIndex: currentNextIndex,
        audioContextTime: now,
        lastChunkEndTime: lastEndTime,
        decodedChunks: decodedChunksRef.current,
        overlap: job?.overlap || 0,
        jobStatus: job?.status || 'idle',
        hasMoreChunks,
        lookahead: 0.1, // 100ms lookahead
      });

      if (decision.action === 'schedule') {
        const chunkIndex = decision.chunkIndex!;
        const startTime = decision.scheduledStartTime!;
        const decodedChunk = decodedChunksRef.current.get(chunkIndex)!;

        // Determine if there will be a next chunk to fade out towards
        let hasNext = false;
        if (job) {
          if (job.status !== 'completed') {
            hasNext = true;
          } else {
            hasNext = chunkIndex < job.chunks.length - 1;
          }
        }

        // Calculate crossfade plans
        const plan = calculateCrossfadePlan({
          startTime,
          duration: decodedChunk.duration,
          overlap: job?.overlap || 0,
          isFirst: chunkIndex === 0,
          hasNext,
        });
        const displayStartTime =
          lastDisplayEndTimeRef.current === null
            ? 0
            : Math.max(0, lastDisplayEndTimeRef.current - (job?.overlap || 0));
        const displayEndTime = displayStartTime + plan.playDuration;
        if (playbackClockStartTimeRef.current === null) {
          playbackClockStartTimeRef.current = plan.playStartTime;
          setPlayheadSeconds(0);
        }

        // Create WebAudio Nodes
        const sourceNode = audioContext.createBufferSource();
        sourceNode.buffer = decodedChunk.buffer;

        const gainNode = audioContext.createGain();
        applyGainPlan(gainNode, plan, now);

        // Connect nodes
        sourceNode.connect(gainNode);
        gainNode.connect(audioContext.destination);

        // Start playback
        sourceNode.start(plan.playStartTime);

        // Save scheduled node
        scheduledChunksRef.current.set(chunkIndex, {
          index: chunkIndex,
          sourceNode,
          gainNode,
          scheduledStartTime: plan.playStartTime,
          scheduledEndTime: plan.playStartTime + plan.playDuration,
          displayStartTime,
          displayEndTime,
          duration: plan.playDuration,
        });

        // Update schedule metrics
        lastChunkEndTimeRef.current = plan.playStartTime + plan.playDuration;
        lastDisplayEndTimeRef.current = displayEndTime;
        nextIndexRef.current = chunkIndex + 1;

        // Transition states
        setPlaybackState('playing');

        // Schedule UI update for when this chunk starts playing
        const timeToStartMs = Math.max(0, (plan.playStartTime - now) * 1000);
        addTimeout(() => {
          activeChunkIndexRef.current = chunkIndex;
          setCurrentChunkIndex(chunkIndex);
        }, timeToStartMs);

        // Schedule check to update to 'completed' if this is the last chunk
        if (!hasNext) {
          const timeToEndMs = Math.max(0, (plan.playStartTime + plan.playDuration - now) * 1000);
          addTimeout(() => {
            activeChunkIndexRef.current = null;
            setPlayheadSeconds(displayEndTime);
            setPlaybackState('completed');
            isArmedRef.current = false;
          }, timeToEndMs);
        }
      } else if (decision.action === 'wait') {
        // Transition to wait state depending on which chunk we need
        if (decision.chunkIndex === 0) {
          setPlaybackState('waiting_chunk_0');
        } else {
          setPlaybackState('waiting_next_chunk');
        }
        loop = false; // exit scheduling loop to wait for buffer/decode
      } else if (decision.action === 'complete') {
        // Wait, if we are completed, but we still have scheduled chunks playing, we shouldn't immediately trigger completed state.
        // The last chunk's timeout handler will trigger 'completed'.
        // If there are no scheduled chunks at all, set completed.
        if (scheduledChunksRef.current.size === 0) {
          setPlaybackState('completed');
          isArmedRef.current = false;
        }
        loop = false;
      } else if (decision.action === 'error') {
        setPlaybackState('error');
        setError({
          message: decision.reason || 'An error occurred during playback scheduling.',
        });
        stop();
        loop = false;
      }
    }
  }, [job, playbackState, stop, addTimeout]);

  // Function to initialize AudioContext and trigger play
  const play = useCallback(() => {
    if (!job) return;

    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
    }

    const audioContext = audioContextRef.current;
    if (audioContext.state === 'suspended') {
      audioContext.resume().catch((err) => {
        console.error('Failed to resume AudioContext:', err);
      });
    }

    isArmedRef.current = true;
    setError(null);

    // Run scheduling immediately
    runSchedulerTick();
  }, [job, runSchedulerTick]);

  // Fetch and decode chunks as they become ready
  useEffect(() => {
    if (!job) {
      resetCache();
      return;
    }

    // Check if the job status has failed
    if (job.status === 'failed') {
      setPlaybackState('error');
      setError({
        message: job.error_message || 'The live job failed.',
      });
      stop();
      return;
    }

    // Scan for ready chunks and fetch them
    job.chunks.forEach((chunk) => {
      if (chunk.status === 'ready' && chunk.instrumental_url) {
        const index = chunk.index;
        // Check if we already have it decoded or if it's currently fetching
        if (!decodedChunksRef.current.has(index) && !fetchingIndicesRef.current.has(index)) {
          fetchingIndicesRef.current.add(index);

          // Trigger fetch and decode
          fetchChunkAudio(chunk.instrumental_url)
            .then(async (arrayBuffer) => {
              if (!audioContextRef.current) {
                // Initialize if not already initialized
                audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
              }
              const buffer = await decodeAudio(audioContextRef.current, arrayBuffer);
              return buffer;
            })
            .then((audioBuffer) => {
              // Store decoded chunk
              decodedChunksRef.current.set(index, {
                index,
                buffer: audioBuffer,
                duration: audioBuffer.duration,
                startSeconds: chunk.start_seconds,
                endSeconds: chunk.end_seconds,
              });

              // Update buffered list state
              setBufferedChunks((prev) => {
                const nextBuffered = [...prev, index].sort((a, b) => a - b);
                return nextBuffered;
              });

              // Run scheduler check in case we were waiting for this chunk
              runSchedulerTick();
            })
            .catch((err) => {
              console.error(`Failed to load chunk ${index}:`, err);
              setError({
                message: `Failed to fetch/decode chunk ${index}.`,
                chunkIndex: index,
                details: err instanceof Error ? err.message : String(err),
              });
              setPlaybackState('error');
              stop();
            })
            .finally(() => {
              fetchingIndicesRef.current.delete(index);
            });
        }
      }
    });
  }, [job, runSchedulerTick, resetCache, stop]);

  // Animation frame loop for smooth playhead updates
  useEffect(() => {
    const canTrackPlayhead =
      playbackState === 'playing' ||
      playbackState === 'waiting_next_chunk' ||
      playbackState === 'buffering';

    if (!canTrackPlayhead || !audioContextRef.current || !isArmedRef.current) {
      cancelAnimation();
      return;
    }

    const updatePlayhead = () => {
      const audioContext = audioContextRef.current;
      if (audioContext && isArmedRef.current) {
        const now = audioContext.currentTime;
        const clockStartTime = playbackClockStartTimeRef.current;
        if (clockStartTime !== null) {
          const maxKnownEnd = lastDisplayEndTimeRef.current ?? Number.POSITIVE_INFINITY;
          const elapsedFromFirstScheduledChunk = Math.max(0, now - clockStartTime);
          setPlayheadSeconds(Math.min(maxKnownEnd, elapsedFromFirstScheduledChunk));
        }

        let activeScheduled: ScheduledChunk | null = null;

        const activeIndex = activeChunkIndexRef.current;
        if (activeIndex !== null) {
          const scheduled = scheduledChunksRef.current.get(activeIndex);
          if (scheduled && now >= scheduled.scheduledStartTime && now <= scheduled.scheduledEndTime) {
            activeScheduled = scheduled;
          }
        }

        if (!activeScheduled) {
          // Find the active scheduled chunk, preferring higher index during crossfades.
          const entries = Array.from(scheduledChunksRef.current.entries()).sort((a, b) => b[0] - a[0]);
          for (const [, sc] of entries) {
            if (now >= sc.scheduledStartTime && now <= sc.scheduledEndTime) {
              activeScheduled = sc;
              activeChunkIndexRef.current = sc.index;
              break;
            }
          }
        }

        if (activeScheduled) {
          const elapsed = now - activeScheduled.scheduledStartTime;
          const calculated = activeScheduled.displayStartTime + elapsed;
          const clamped = Math.max(
            activeScheduled.displayStartTime,
            Math.min(activeScheduled.displayEndTime, calculated)
          );
          setPlayheadSeconds(clamped);
        }
      }
      animationFrameIdRef.current = requestAnimationFrame(updatePlayhead);
    };

    animationFrameIdRef.current = requestAnimationFrame(updatePlayhead);
    return () => cancelAnimation();
  }, [playbackState, cancelAnimation]);

  // Clean up on unmount
  useEffect(() => {
    return () => {
      stop();
      cancelAnimation();
      if (audioContextRef.current) {
        audioContextRef.current.close().catch((err) => {
          console.error('Error closing AudioContext on unmount:', err);
        });
        audioContextRef.current = null;
      }
    };
  }, [stop, cancelAnimation]);

  return {
    playbackState,
    error,
    currentChunkIndex,
    bufferedChunks,
    playheadSeconds,
    play,
    stop,
  };
}
