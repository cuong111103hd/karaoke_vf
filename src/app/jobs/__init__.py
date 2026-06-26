from app.jobs.live_manager import LiveJobManager

# Export a shared singleton live job manager instance
live_job_manager = LiveJobManager()

__all__ = ["LiveJobManager", "live_job_manager"]
