import type { PlaybackState } from '../audio/playbackTypes';

interface PlaybackControlsProps {
  playbackState: PlaybackState;
  onPlay: () => void;
  onStop: () => void;
  disabled: boolean;
}

export function PlaybackControls({
  playbackState,
  onPlay,
  onStop,
  disabled,
}: PlaybackControlsProps) {
  const isPlaying = playbackState === 'playing';
  const isWaiting =
    playbackState === 'waiting_chunk_0' ||
    playbackState === 'waiting_next_chunk' ||
    playbackState === 'buffering';

  return (
    <div className="playback-controls-wrapper">
      <button
        onClick={onPlay}
        disabled={disabled || isPlaying}
        className={`btn-play-premium ${isPlaying ? 'active' : ''} ${isWaiting ? 'pulse-light' : ''}`}
        aria-label="Start Playback"
      >
        <span className="btn-icon">
          {isPlaying ? (
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z" />
            </svg>
          ) : (
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M8 5v14l11-7z" />
            </svg>
          )}
        </span>
        <span className="btn-text">
          {isPlaying ? 'Playing Live' : isWaiting ? 'Connecting...' : 'Start Playback'}
        </span>
      </button>

      <button
        onClick={onStop}
        disabled={disabled || playbackState === 'idle' || playbackState === 'stopped'}
        className="btn-stop-premium"
        aria-label="Stop Playback"
      >
        <span className="btn-icon">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M6 6h12v12H6z" />
          </svg>
        </span>
        <span className="btn-text">Stop</span>
      </button>
    </div>
  );
}
