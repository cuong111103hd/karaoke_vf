import type { LiveJob } from '../types/liveJob';

const API_BASE = '/api';

export async function createLiveJob(data: {
  youtube_url: string;
  chunk_duration: number;
  overlap: number;
  max_chunks?: number;
  separator_engine?: string;
  model_name?: string;
  output_format: string;
  source_mode?: 'download' | 'streaming';
  initial_buffer_seconds?: number;
}): Promise<LiveJob> {
  const response = await fetch(`${API_BASE}/live-jobs`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    throw new Error(errData.detail || 'Failed to create live job');
  }

  return response.json();
}

export async function getLiveJob(jobId: string): Promise<LiveJob> {
  const response = await fetch(`${API_BASE}/live-jobs/${jobId}`);

  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    throw new Error(errData.detail || `Failed to fetch job ${jobId}`);
  }

  return response.json();
}

export async function listLiveJobs(): Promise<LiveJob[]> {
  const response = await fetch(`${API_BASE}/live-jobs`);

  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    throw new Error(errData.detail || 'Failed to list live jobs');
  }

  return response.json();
}
