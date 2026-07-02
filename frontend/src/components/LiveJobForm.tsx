import React, { useState } from 'react';

interface LiveJobFormProps {
  onSubmit: (data: {
    youtube_url: string;
    chunk_duration: number;
    overlap: number;
    max_chunks?: number;
    separator_engine?: string;
    model_name?: string;
    output_format: string;
  }) => void;
  isLoading: boolean;
  error: string | null;
}

function validateYouTubeUrl(rawUrl: string): string | null {
  const trimmedUrl = rawUrl.trim();

  if (!trimmedUrl) {
    return 'YouTube URL is required';
  }

  if (trimmedUrl.includes('<') || trimmedUrl.includes('>')) {
    return 'Paste a YouTube URL, not HTML or page markup.';
  }

  try {
    const parsedUrl = new URL(trimmedUrl);
    const hostname = parsedUrl.hostname.replace(/^www\./, '').toLowerCase();
    const isYouTubeHost =
      hostname === 'youtube.com' ||
      hostname === 'm.youtube.com' ||
      hostname === 'music.youtube.com' ||
      hostname === 'youtu.be';

    if (!isYouTubeHost) {
      return 'Enter a valid YouTube URL.';
    }
  } catch {
    return 'Enter a valid YouTube URL.';
  }

  return null;
}

export const LiveJobForm: React.FC<LiveJobFormProps> = ({ onSubmit, isLoading, error }) => {
  const [url, setUrl] = useState('');
  const [chunkDuration, setChunkDuration] = useState(30.0);
  const [overlap, setOverlap] = useState(0.0);
  const [maxChunks, setMaxChunks] = useState('');
  const [engine, setEngine] = useState<'demucs' | 'mdx_onnx'>('demucs');
  const [model, setModel] = useState('htdemucs');
  const [format, setFormat] = useState('wav');
  const [validationError, setValidationError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setValidationError(null);

    const urlError = validateYouTubeUrl(url);
    if (urlError) {
      setValidationError(urlError);
      return;
    }

    if (overlap >= chunkDuration) {
      setValidationError('Overlap must be strictly smaller than chunk duration');
      return;
    }

    if (!model.trim()) {
      setValidationError('Model is required');
      return;
    }

    onSubmit({
      youtube_url: url.trim(),
      chunk_duration: chunkDuration,
      overlap: overlap,
      max_chunks: maxChunks ? parseInt(maxChunks, 10) : undefined,
      separator_engine: engine,
      model_name: model || undefined,
      output_format: format,
    });
  };

  const handleEngineChange = (nextEngine: 'demucs' | 'mdx_onnx') => {
    setEngine(nextEngine);
    setModel(nextEngine === 'demucs' ? 'htdemucs' : 'UVR_MDXNET_KARA_2.onnx');
  };

  return (
    <form className="live-job-form glass-card" onSubmit={handleSubmit}>
      <h2 className="section-title">New Live Separation</h2>
      
      {(error || validationError) && (
        <div className="alert alert-error">
          {validationError || error}
        </div>
      )}

      <div className="form-group">
        <label htmlFor="youtube_url">YouTube URL</label>
        <input
          id="youtube_url"
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://www.youtube.com/watch?v=..."
          disabled={isLoading}
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="chunk_duration">Chunk Duration (seconds)</label>
          <input
            id="chunk_duration"
            type="number"
            step="0.5"
            min="1"
            value={chunkDuration}
            onChange={(e) => setChunkDuration(parseFloat(e.target.value))}
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="overlap">Overlap (seconds)</label>
          <input
            id="overlap"
            type="number"
            step="0.5"
            min="0"
            value={overlap}
            onChange={(e) => setOverlap(parseFloat(e.target.value))}
            disabled={isLoading}
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="max_chunks">Max Chunks (optional)</label>
          <input
            id="max_chunks"
            type="number"
            min="1"
            value={maxChunks}
            onChange={(e) => setMaxChunks(e.target.value)}
            placeholder="No limit"
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="separator_engine">Separator</label>
          <select
            id="separator_engine"
            value={engine}
            onChange={(e) => handleEngineChange(e.target.value as 'demucs' | 'mdx_onnx')}
            disabled={isLoading}
          >
            <option value="demucs">Demucs</option>
            <option value="mdx_onnx">MDX ONNX</option>
          </select>
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="model_name">Model</label>
          {engine === 'demucs' ? (
            <select
              id="model_name"
              value={model}
              onChange={(e) => setModel(e.target.value)}
              disabled={isLoading}
            >
              <option value="htdemucs">htdemucs (recommended)</option>
              <option value="htdemucs_ft">htdemucs_ft</option>
              <option value="htdemucs_6s">htdemucs_6s</option>
            </select>
          ) : (
            <input
              id="model_name"
              type="text"
              value={model}
              onChange={(e) => setModel(e.target.value)}
              placeholder="UVR_MDXNET_KARA_2.onnx"
              disabled={isLoading}
            />
          )}
        </div>

        <div className="form-group">
          <label htmlFor="output_format">Output Format</label>
          <select
            id="output_format"
            value={format}
            onChange={(e) => setFormat(e.target.value)}
            disabled={isLoading}
          >
            <option value="wav">WAV (lossless)</option>
            <option value="mp3">MP3</option>
          </select>
        </div>
      </div>

      <button type="submit" className="btn btn-primary" disabled={isLoading}>
        {isLoading ? 'Starting separation...' : 'Start separation'}
      </button>
    </form>
  );
};
