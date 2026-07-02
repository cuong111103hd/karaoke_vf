import type { LiveJob } from '../types/liveJob';
import { useLivePlayback } from '../audio/livePlaybackController';
import { PlaybackControls } from './PlaybackControls';
import { PlaybackBufferStatus } from './PlaybackBufferStatus';
import { PlaybackProgressBar } from './PlaybackProgressBar';

interface LivePlaybackPanelProps {
  job: LiveJob | null;
}

export function LivePlaybackPanel({ job }: LivePlaybackPanelProps) {
  const {
    playbackState,
    error,
    currentChunkIndex,
    bufferedChunks,
    playheadSeconds,
    play,
    stop,
  } = useLivePlayback(job);

  const disabled = !job;

  return (
    <div className="glass-card live-playback-panel-card">
      <h2 className="section-title">
        <span className="accent-icon" aria-hidden="true" /> Live Audio Playback
      </h2>
      <p className="section-desc">
        Play ready instrumental tracks continuously using the WebAudio API.
        Overlap segments will be crossfaded automatically.
      </p>

      <PlaybackProgressBar
        job={job}
        playheadSeconds={playheadSeconds}
        bufferedChunks={bufferedChunks}
      />

      <div className="playback-panel-layout">
        <PlaybackControls
          playbackState={playbackState}
          onPlay={play}
          onStop={stop}
          disabled={disabled}
        />

        <PlaybackBufferStatus
          playbackState={playbackState}
          error={error}
          currentChunkIndex={currentChunkIndex}
          bufferedChunks={bufferedChunks}
          allChunks={job ? job.chunks : []}
        />
      </div>
    </div>
  );
}
