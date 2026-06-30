import sys
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def test_acrossfade_filter_construction() -> None:
    from app.services.audio.overlap import build_acrossfade_filter
    
    assert build_acrossfade_filter(1, 5.0) == ""
    assert build_acrossfade_filter(2, 5.0) == "[0:a][1:a]acrossfade=d=5.0:c1=tri:c2=tri[a1]"
    assert build_acrossfade_filter(3, 3.5) == "[0:a][1:a]acrossfade=d=3.5:c1=tri:c2=tri[a1];[a1][2:a]acrossfade=d=3.5:c1=tri:c2=tri[a2]"
