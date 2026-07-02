import React from 'react';
import type { LiveJob } from '../types/liveJob';
import { calculateProgressMetrics } from '../audio/progressMath';

interface PlaybackProgressBarProps {
  job: LiveJob | null;
  playheadSeconds: number;
  bufferedChunks: number[];
}

const formatTime = (seconds: number): string => {
  if (isNaN(seconds) || seconds < 0) return '0:00';
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

export const PlaybackProgressBar: React.FC<PlaybackProgressBarProps> = ({
  job,
  playheadSeconds,
  bufferedChunks,
}) => {
  if (!job) {
    return null;
  }

  const {
    totalDuration,
    processedFrontier,
    bufferedFrontier,
    playedPercent,
    bufferedPercent,
    processedPercent,
  } = calculateProgressMetrics(job, playheadSeconds, bufferedChunks);

  return (
    <div className="playback-progress-container">
      <div className="progress-summary">
        <div>
          <span className="progress-label">Played</span>
          <strong>{formatTime(playheadSeconds)}</strong>
        </div>
        <div>
          <span className="progress-label">Buffered</span>
          <strong>{formatTime(bufferedFrontier)}</strong>
        </div>
        <div>
          <span className="progress-label">Processed</span>
          <strong>{formatTime(processedFrontier)}</strong>
        </div>
      </div>

      <div 
        className="progress-rail" 
        role="progressbar" 
        aria-valuenow={playheadSeconds} 
        aria-valuemin={0} 
        aria-valuemax={totalDuration}
        aria-label="Playback progress"
      >
        <div 
          className="track-processed" 
          style={{ width: `${processedPercent}%` }}
        />

        <div 
          className="track-buffered" 
          style={{ width: `${bufferedPercent}%` }}
        />

        <div 
          className="track-played" 
          style={{ width: `${playedPercent}%` }}
        />
      </div>

      <div className="progress-labels">
        <span className="time-played">
          Song time: {formatTime(playheadSeconds)} / {formatTime(totalDuration)}
        </span>
        <span className="time-buffered">
          Buffered to {formatTime(bufferedFrontier)}
          {processedFrontier !== bufferedFrontier && `, processed to ${formatTime(processedFrontier)}`}
        </span>
      </div>
    </div>
  );
};
