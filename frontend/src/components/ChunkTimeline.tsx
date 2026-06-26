import React from 'react';
import type { LiveChunk } from '../types/liveJob';
import { StatusBadge } from './StatusBadge';

interface ChunkTimelineProps {
  chunks: LiveChunk[];
}

export const ChunkTimeline: React.FC<ChunkTimelineProps> = ({ chunks }) => {
  if (chunks.length === 0) {
    return (
      <div className="chunk-timeline empty glass-card">
        <h2 className="section-title">Separated Chunks</h2>
        <p className="no-chunks-text">Waiting for the first chunk to be planned...</p>
      </div>
    );
  }

  return (
    <div className="chunk-timeline glass-card">
      <h2 className="section-title">Separated Chunks ({chunks.length})</h2>
      
      <div className="table-container">
        <table className="timeline-table">
          <thead>
            <tr>
              <th>Index</th>
              <th>Time Range</th>
              <th>Status</th>
              <th>Processing Time</th>
              <th>Notes / Errors</th>
            </tr>
          </thead>
          <tbody>
            {chunks.map((chunk) => (
              <tr key={chunk.index} className={`chunk-row row-${chunk.status}`}>
                <td className="chunk-index font-semibold">#{chunk.index}</td>
                <td className="chunk-time">
                  {chunk.start_seconds.toFixed(1)}s - {chunk.end_seconds.toFixed(1)}s
                </td>
                <td>
                  <StatusBadge status={chunk.status} />
                </td>
                <td className="chunk-duration">
                  {chunk.processing_seconds !== undefined && chunk.processing_seconds !== null
                    ? `${chunk.processing_seconds.toFixed(2)}s`
                    : '-'}
                </td>
                <td className="chunk-notes">
                  {chunk.status === 'ready' && (
                    <span className="text-success truncate-path">
                      Ready: {chunk.instrumental_path ? chunk.instrumental_path.split('/').pop() : 'WAV stem'}
                    </span>
                  )}
                  {chunk.status === 'failed' && (
                    <span className="text-danger error-detail">
                      Error: {chunk.error_message}
                    </span>
                  )}
                  {chunk.status === 'processing' && (
                    <span className="text-processing animate-pulse">Running Demucs...</span>
                  )}
                  {chunk.status === 'pending' && (
                    <span className="text-pending">Queued</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
