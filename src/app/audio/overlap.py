def build_acrossfade_filter(num_files: int, overlap_seconds: float) -> str:
    """
    Constructs the acrossfade complex filter graph string for N input audio streams.
    Example for 3 inputs:
    "[0:a][1:a]acrossfade=d=5:c1=tri:c2=tri[a1];[a1][2:a]acrossfade=d=5:c1=tri:c2=tri"
    """
    if num_files <= 1:
        return ""
        
    filter_parts = []
    # First join between stream 0 and stream 1
    filter_parts.append(f"[0:a][1:a]acrossfade=d={overlap_seconds}:c1=tri:c2=tri[a1]")
    
    # Chain subsequent joins
    for i in range(2, num_files):
        prev_label = f"[a{i-1}]"
        next_label = f"[a{i}]"
        filter_parts.append(f"{prev_label}[{i}:a]acrossfade=d={overlap_seconds}:c1=tri:c2=tri{next_label}")
        
    return ";".join(filter_parts)
