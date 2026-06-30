import React from 'react';
import type { LiveJob } from '../types/liveJob';
import { StatusBadge } from './StatusBadge';

interface LiveJobStatusProps {
  job: LiveJob;
  lastUpdated: Date | null;
}

export const LiveJobStatus: React.FC<LiveJobStatusProps> = ({ job, lastUpdated }) => {
  const formatSeconds = (secs?: number) => {
    if (secs === undefined) return '-';
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <div className="live-job-status glass-card">
      <div className="status-header">
        <h2 className="section-title">Job Details</h2>
        <StatusBadge status={job.status} />
      </div>

      <div className="status-grid">
        <div className="status-item full-width">
          <span className="label">YouTube URL</span>
          <span className="value truncate">
            <a href={job.youtube_url} target="_blank" rel="noopener noreferrer">
              {job.youtube_url}
            </a>
          </span>
        </div>

        {job.video_title && (
          <div className="status-item full-width">
            <span className="label">Video Title</span>
            <span className="value title-value">{job.video_title}</span>
          </div>
        )}

        {job.video_duration !== undefined && (
          <div className="status-item">
            <span className="label">Video Length</span>
            <span className="value">{formatSeconds(job.video_duration)}</span>
          </div>
        )}

        <div className="status-item">
          <span className="label">Job ID</span>
          <span className="value code-text">{job.job_id}</span>
        </div>

        <div className="status-item">
          <span className="label">Chunk Duration</span>
          <span className="value">{job.chunk_duration}s</span>
        </div>

        <div className="status-item">
          <span className="label">Overlap</span>
          <span className="value">{job.overlap}s</span>
        </div>

        <div className="status-item">
          <span className="label">Max Chunks</span>
          <span className="value">{job.max_chunks || 'No limit'}</span>
        </div>

        <div className="status-item">
          <span className="label">Separator</span>
          <span className="value">{job.separator_engine || 'demucs'}</span>
        </div>

        <div className="status-item">
          <span className="label">Model</span>
          <span className="value">{job.model_name || 'htdemucs'}</span>
        </div>

        <div className="status-item">
          <span className="label">Format</span>
          <span className="value">{job.output_format.toUpperCase()}</span>
        </div>
      </div>

      {job.error_message && (
        <div className="alert alert-error job-error">
          <strong>Job Error:</strong> {job.error_message}
        </div>
      )}

      {lastUpdated && (
        <div className="last-updated">
          Last refreshed: {lastUpdated.toLocaleTimeString()}
        </div>
      )}
    </div>
  );
};
