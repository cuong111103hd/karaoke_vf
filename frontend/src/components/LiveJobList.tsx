import React from 'react';
import type { LiveJob } from '../types/liveJob';
import { StatusBadge } from './StatusBadge';

interface LiveJobListProps {
  jobs: LiveJob[];
  selectedJobId: string | null;
  onSelectJob: (jobId: string) => void;
}

export const LiveJobList: React.FC<LiveJobListProps> = ({ jobs, selectedJobId, onSelectJob }) => {
  if (jobs.length === 0) {
    return (
      <div className="live-job-list empty glass-card">
        <h2 className="section-title">Active Sessions</h2>
        <p className="no-jobs-text">No active sessions found.</p>
      </div>
    );
  }

  return (
    <div className="live-job-list glass-card">
      <h2 className="section-title">Active Sessions ({jobs.length})</h2>
      <div className="jobs-container">
        {jobs.map((job) => (
          <div
            key={job.job_id}
            className={`job-item-card ${selectedJobId === job.job_id ? 'active-selected' : ''}`}
            onClick={() => onSelectJob(job.job_id)}
          >
            <div className="job-item-meta">
              <span className="job-item-title truncate">
                {job.video_title || job.youtube_url}
              </span>
              <span className="job-item-id">ID: {job.job_id.substring(0, 8)}...</span>
            </div>
            <StatusBadge status={job.status} />
          </div>
        ))}
      </div>
    </div>
  );
};
