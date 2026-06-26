import type { PlaybackState, PlayerError } from '../audio/playbackTypes';
import type { LiveChunk } from '../types/liveJob';

interface PlaybackBufferStatusProps {
  playbackState: PlaybackState;
  error: PlayerError | null;
  currentChunkIndex: number | null;
  bufferedChunks: number[];
  allChunks: LiveChunk[];
}

export function PlaybackBufferStatus({
  playbackState,
  error,
  currentChunkIndex,
  bufferedChunks,
  allChunks,
}: PlaybackBufferStatusProps) {
  // Helper to translate status to user friendly badges
  const getStatusBadge = () => {
    switch (playbackState) {
      case 'idle':
        return { label: 'Ready', class: 'badge-idle' };
      case 'waiting_chunk_0':
        return { label: 'Waiting for Chunk 0', class: 'badge-waiting pulse' };
      case 'buffering':
        return { label: 'Buffering', class: 'badge-waiting pulse' };
      case 'playing':
        return { label: 'Playing', class: 'badge-playing' };
      case 'waiting_next_chunk':
        return { label: 'Stalled (Waiting for Next Chunk)', class: 'badge-waiting pulse' };
      case 'stopped':
        return { label: 'Stopped', class: 'badge-stopped' };
      case 'completed':
        return { label: 'Finished', class: 'badge-completed' };
      case 'error':
        return { label: 'Error', class: 'badge-error' };
      default:
        return { label: 'Unknown', class: 'badge-idle' };
    }
  };

  const badge = getStatusBadge();

  return (
    <div className="playback-status-card">
      <div className="status-header">
        <span className="status-label">Player State:</span>
        <span className={`status-badge ${badge.class}`}>{badge.label}</span>
      </div>

      {playbackState === 'error' && error && (
        <div className="player-error-box">
          <p className="error-message">{error.message}</p>
          {error.details && <pre className="error-details">{error.details}</pre>}
        </div>
      )}

      <div className="status-details">
        <div className="detail-row">
          <span>Active Chunk Index:</span>
          <strong>{currentChunkIndex !== null ? `#${currentChunkIndex}` : 'None'}</strong>
        </div>
        <div className="detail-row">
          <span>Buffered Chunks:</span>
          <strong>
            {bufferedChunks.length} / {allChunks.length}
          </strong>
        </div>
        <div className="detail-row">
          <span>Next Expected Chunk:</span>
          <strong>
            {currentChunkIndex !== null
              ? `#${currentChunkIndex + 1}`
              : allChunks.length > 0
                ? '#0'
                : 'None'}
          </strong>
        </div>
      </div>

      {/* Visual Chunk Cache Grid */}
      {allChunks.length > 0 && (
        <div className="chunk-buffer-map">
          <h4 className="buffer-map-title">Cache Status Matrix</h4>
          <div className="buffer-cells-grid">
            {allChunks.map((chunk, idx) => {
              const isDecoded = bufferedChunks.includes(idx);
              const isPlaying = currentChunkIndex === idx;

              let cellClass = 'cell-pending';
              if (isPlaying) {
                cellClass = 'cell-playing-active';
              } else if (isDecoded) {
                cellClass = 'cell-decoded-buffered';
              } else if (chunk.status === 'processing') {
                cellClass = 'cell-processing-backend';
              } else if (chunk.status === 'failed') {
                cellClass = 'cell-failed-backend';
              }

              return (
                <div
                  key={idx}
                  className={`buffer-cell ${cellClass}`}
                  title={`Chunk ${idx}: Backend=${chunk.status}, Decoded=${isDecoded ? 'Yes' : 'No'}`}
                >
                  <span className="cell-num">{idx}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
