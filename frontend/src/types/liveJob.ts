export interface LiveChunk {
  index: number;
  status: 'pending' | 'processing' | 'ready' | 'failed';
  start_seconds: number;
  end_seconds: number;
  instrumental_path?: string;
  instrumental_url?: string;
  processing_seconds?: number;
  error_message?: string;
}

export interface LiveJob {
  job_id: string;
  youtube_url: string;
  status: 'starting' | 'queued' | 'active' | 'completed' | 'failed';
  created_at: string;
  manifest_path?: string;
  chunk_duration: number;
  overlap: number;
  max_chunks?: number;
  separator_engine?: 'demucs' | 'mdx_onnx';
  model_name?: string;
  output_format: string;
  source_mode?: 'download' | 'streaming';
  initial_buffer_seconds?: number;
  video_title?: string;
  video_duration?: number;
  error_message?: string;
  chunks: LiveChunk[];
}
