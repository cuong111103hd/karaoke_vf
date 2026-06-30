from typing import Dict, Optional, Tuple
from app.config.settings import settings
from app.services.separation.contracts import Separator
from app.services.separation.engines.demucs import DemucsEngine

# Process-scoped cache for separator instances
_instances: Dict[Tuple[str, str], Separator] = {}

def get_separation_engine(
    model_name: Optional[str] = None,
    engine_name: Optional[str] = None,
) -> Separator:
    """
    Return the configured separation engine instance.

    The optional model name supports per-job model selection for both Demucs
    and MDX ONNX. Instances are cached by engine and effective model.
    """
    engine_type = (engine_name or settings.SEPARATION_ENGINE).lower()

    if engine_type not in ("demucs", "mdx_onnx"):
        raise ValueError(f"Invalid SEPARATION_ENGINE: {engine_type}. Must be 'demucs' or 'mdx_onnx'.")

    if engine_type == "demucs":
        effective_model = model_name or settings.SEPARATION_MODEL or settings.DEMUCS_MODEL_NAME or "htdemucs"
        cache_key = (engine_type, effective_model)
        if cache_key in _instances:
            return _instances[cache_key]
        engine = DemucsEngine(model_name=effective_model)
        _instances[cache_key] = engine
        return engine
    elif engine_type == "mdx_onnx":
        # Import lazily to defer audio-separator/onnx dependencies
        from app.services.separation.engines.mdx_onnx import MdxOnnxEngine
        effective_model = model_name or settings.SEPARATION_MODEL or "UVR_MDXNET_KARA_2.onnx"
        cache_key = (engine_type, effective_model)
        if cache_key in _instances:
            return _instances[cache_key]
        engine = MdxOnnxEngine(
            model_name=effective_model,
            model_dir=settings.SEPARATION_MODEL_DIR,
            segment_size=settings.MDX_SEGMENT_SIZE,
            overlap=settings.MDX_OVERLAP,
            batch_size=settings.MDX_BATCH_SIZE
        )
        _instances[cache_key] = engine
        return engine

def clear_factory_cache() -> None:
    """Clears the cached engine instances. Useful for testing."""
    _instances.clear()
