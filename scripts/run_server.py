#!/usr/bin/env python
import sys
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import uvicorn
from app.config.settings import settings

def main() -> None:
    print(f"Starting Karaoke Separation Server on http://{settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "app.api.app:create_app",
        host=settings.HOST,
        port=settings.PORT,
        factory=True,
        reload=True
    )

if __name__ == "__main__":
    main()
