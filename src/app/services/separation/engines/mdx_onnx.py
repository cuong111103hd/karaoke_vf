import logging
import threading
from pathlib import Path
from app.services.errors import SeparatorStageError
from app.services.separation.contracts import Separator, SeparationOutput

logger = logging.getLogger(__name__)

class MdxOnnxEngine(Separator):
    engine_name = "mdx_onnx"

    def __init__(
        self,
        model_name: str,
        model_dir: Path,
        segment_size: int = 256,
        overlap: float = 0.25,
        batch_size: int = 1
    ):
        self.model_name = model_name
        self.model_dir = model_dir
        self.segment_size = segment_size
        self.overlap = overlap
        self.batch_size = batch_size
        
        self.separator = None
        self._model_loaded = False
        self._lock = threading.Lock()

    def load_model(self) -> None:
        """
        Lazily and concurrency-safely loads the MDX ONNX model.
        """
        with self._lock:
            if self._model_loaded:
                return
            
            try:
                from audio_separator.separator import Separator as AudioSeparator
                
                # Make sure the model directory exists
                self.model_dir.mkdir(parents=True, exist_ok=True)
                
                # Initialize Separator with CPU/safe options
                self.separator = AudioSeparator(
                    log_level=logging.INFO,
                    model_file_dir=str(self.model_dir),
                    output_dir=None,  # will be set dynamically per separate call
                    output_format="WAV",
                    use_soundfile=False,
                    use_autocast=False,
                    use_directml=False,
                    mdx_params={
                        'hop_length': 1024,
                        'segment_size': self.segment_size,
                        'overlap': self.overlap,
                        'batch_size': self.batch_size,
                        'enable_denoise': False
                    }
                )
                logger.info(f"Loading MDX ONNX model: {self.model_name} from {self.model_dir}...")
                self.separator.load_model(self.model_name)
                self._model_loaded = True
                logger.info(f"Successfully loaded MDX ONNX model: {self.model_name}")
            except Exception as e:
                raise SeparatorStageError(
                    engine="mdx_onnx",
                    model=self.model_name,
                    message=f"Failed to load model: {str(e)}",
                    original_error=e
                )

    def separate(self, input_path: Path, output_dir: Path) -> SeparationOutput:
        """
        Runs MDX ONNX separation on the input file and returns SeparationOutput.
        """
        # Ensure model is loaded (lazy loading)
        self.load_model()
        
        # Ensure only one separation runs at a time (prevent state/directory collisions)
        with self._lock:
            try:
                # Prepare output directory
                output_dir.mkdir(parents=True, exist_ok=True)
                
                # Set output directory dynamically
                self.separator.output_dir = str(output_dir)
                if hasattr(self.separator, "model_instance") and self.separator.model_instance:
                    self.separator.model_instance.output_dir = str(output_dir)
                
                logger.info(f"Starting MDX ONNX separation for {input_path.name}...")
                output_files = self.separator.separate(str(input_path))
                logger.info(f"Completed MDX ONNX separation. Outputs: {output_files}")
            except Exception as e:
                raise SeparatorStageError(
                    engine="mdx_onnx",
                    model=self.model_name,
                    message=f"Separation failed: {str(e)}",
                    original_error=e
                )

        if not isinstance(output_files, (list, tuple)):
            raise SeparatorStageError(
                engine="mdx_onnx",
                model=self.model_name,
                message=f"Separator returned an invalid output list: {output_files!r}",
            )

        # Map returned filenames to SeparationOutput
        instrumental_path = None
        vocals_path = None

        for file_path_str in output_files:
            # Map path within target output directory
            path = Path(output_dir) / Path(file_path_str).name
            name_lower = path.name.lower()
            if "instrumental" in name_lower or "accompaniment" in name_lower:
                instrumental_path = path
            elif "vocals" in name_lower:
                vocals_path = path

        if not instrumental_path or not instrumental_path.exists():
            raise SeparatorStageError(
                engine="mdx_onnx",
                model=self.model_name,
                message=f"Separation succeeded but instrumental file was not found under {output_dir}. Returned files: {output_files}"
            )

        return SeparationOutput(
            instrumental_path=instrumental_path,
            vocals_path=vocals_path if vocals_path and vocals_path.exists() else None
        )
