import { useState, useCallback, useEffect, useRef } from 'react';
import type { LiveJob } from './types/liveJob';
import { createLiveJob, getLiveJob, listLiveJobs } from './api/liveJobsApi';
import { LiveJobForm } from './components/LiveJobForm';
import { LiveJobStatus } from './components/LiveJobStatus';
import { LivePlaybackPanel } from './components/LivePlaybackPanel';
import { ChunkTimeline } from './components/ChunkTimeline';
import { LiveJobList } from './components/LiveJobList';
import './styles/app.css';

function App() {
  const [jobs, setJobs] = useState<LiveJob[]>([]);
  const [selectedJob, setSelectedJob] = useState<LiveJob | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const pollIntervalRef = useRef<number | null>(null);

  const stopPolling = useCallback(() => {
    if (pollIntervalRef.current !== null) {
      clearInterval(pollIntervalRef.current);
      pollIntervalRef.current = null;
    }
  }, []);

  const fetchJobs = useCallback(async () => {
    try {
      const allJobs = await listLiveJobs();
      setJobs(allJobs);
      return allJobs;
    } catch (err: unknown) {
      console.error('Error fetching jobs:', err);
      return [];
    }
  }, []);

  const startPolling = useCallback((jobId: string) => {
    stopPolling();
    pollIntervalRef.current = window.setInterval(async () => {
      try {
        const jobDetails = await getLiveJob(jobId);
        setSelectedJob(jobDetails);
        setLastUpdated(new Date());

        // Update in the main list too
        setJobs((prevJobs) =>
          prevJobs.map((j) => (j.job_id === jobId ? jobDetails : j))
        );

        // Stop polling if we reached terminal state
        if (jobDetails.status === 'completed' || jobDetails.status === 'failed') {
          stopPolling();
          fetchJobs(); // Refresh full list
        }
      } catch (err: unknown) {
        console.error('Error polling job status:', err);
      }
    }, 2000);
  }, [fetchJobs, stopPolling]);

  const handleSelectJob = useCallback(async (jobId: string) => {
    stopPolling();
    setError(null);
    try {
      const jobDetails = await getLiveJob(jobId);
      setSelectedJob(jobDetails);
      setLastUpdated(new Date());

      // If active or starting, start polling
      if (jobDetails.status === 'starting' || jobDetails.status === 'active') {
        startPolling(jobId);
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to load job details');
    }
  }, [startPolling, stopPolling]);

  // Load all jobs on mount
  useEffect(() => {
    let isMounted = true;

    fetchJobs().then((allJobs) => {
      if (isMounted && allJobs.length > 0) {
        handleSelectJob(allJobs[allJobs.length - 1].job_id);
      }
    });

    return () => {
      isMounted = false;
      stopPolling();
    };
  }, [fetchJobs, handleSelectJob, stopPolling]);

  const handleCreateJob = async (data: {
    youtube_url: string;
    chunk_duration: number;
    overlap: number;
    max_chunks?: number;
    model_name?: string;
    output_format: string;
  }) => {
    setIsLoading(true);
    setError(null);
    try {
      const newJob = await createLiveJob(data);
      setJobs((prevJobs) => [...prevJobs, newJob]);
      setSelectedJob(newJob);
      setLastUpdated(new Date());
      startPolling(newJob.job_id);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to start live separation job');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-layout">
      <header className="app-header">
        <h1 className="app-title-gradient">Karaoke Live Separation Dashboard</h1>
        <p className="app-subtitle">
          Monitor YouTube-to-karaoke audio slicing and isolated instrumental progress in real-time.
        </p>
      </header>

      <main className="dashboard-grid">
        <section className="sidebar-column">
          <LiveJobForm onSubmit={handleCreateJob} isLoading={isLoading} error={error} />
          <LiveJobList
            jobs={jobs}
            selectedJobId={selectedJob?.job_id || null}
            onSelectJob={handleSelectJob}
          />
        </section>

        <section className="main-column">
          {selectedJob ? (
            <>
              <LiveJobStatus job={selectedJob} lastUpdated={lastUpdated} />
              <LivePlaybackPanel job={selectedJob} />
              <ChunkTimeline chunks={selectedJob.chunks} />
            </>
          ) : (
            <div className="glass-card empty-dashboard">
              <h2 className="section-title">Select a Session</h2>
              <p className="no-chunks-text">
                Start a new live separation session from the form, or select an active session from the sidebar to inspect progress.
              </p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
