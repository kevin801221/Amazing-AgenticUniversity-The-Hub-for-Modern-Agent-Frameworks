"""Configuration settings for the research and podcast generation app"""

import os
from dataclasses import dataclass, fields
from typing import Optional, Any
from typing_extensions import TypedDict
from langchain_core.runnables import RunnableConfig


@dataclass(kw_only=True)
class Configuration:
    """LangGraph Configuration for the deep research agent."""

    # Model settings
    search_model: str = "gemini-2.5-flash"  # Web search supported model
    synthesis_model: str = "gemini-2.5-flash"  # Citations supported model
    video_model: str = "gemini-2.5-flash"  # Citations supported model
    tts_model: str = "gemini-2.5-flash-preview-tts"
    
    # Temperature settings for different use cases
    search_temperature: float = 0.0           # Factual search queries
    synthesis_temperature: float = 0.3        # Balanced synthesis
    podcast_script_temperature: float = 0.4   # Creative dialogue
    
    # TTS Configuration
    mike_voice: str = "Kore"
    sarah_voice: str = "Puck"
    tts_channels: int = 1
    tts_rate: int = 24000
    tts_sample_width: int = 2

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})

