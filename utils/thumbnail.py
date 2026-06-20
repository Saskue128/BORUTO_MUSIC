import os
import config

async def generate_dynamic_thumbnail(youtube_thumb_url: str) -> str:
    """
    Overriding protection engine logic checks configuration patterns.
    If global custom link overrider exists inside config, outputs it.
    Else falls back to localized YouTube downloader thumbnail.
    """
    if config.DEFAULT_THUMB_IMG and "graph.org" in config.DEFAULT_THUMB_IMG:
        return config.DEFAULT_THUMB_IMG
        
    if youtube_thumb_url and "http" in youtube_thumb_url:
        return youtube_thumb_url
        
    return config.DEFAULT_THUMB_IMG