from __future__ import annotations

import re
from collections.abc import Mapping
from os import PathLike
from pathlib import Path
from urllib.parse import unquote

from attrs import frozen


@frozen(slots=True)
class FileDownload:
    """A downloaded API attachment kept in memory."""

    content: bytes
    filename: str
    content_type: str

    @classmethod
    def from_response(cls, content: bytes, headers: Mapping[str, str]) -> FileDownload:
        lowered = {key.lower(): value for key, value in headers.items()}
        content_type = lowered.get("content-type", "application/octet-stream").split(";", 1)[0]
        filename = _filename(lowered.get("content-disposition", ""))
        return cls(content=content, filename=filename, content_type=content_type)

    def save(self, path: str | PathLike[str], *, overwrite: bool = False) -> Path:
        """Save the attachment and return its final path."""

        destination = Path(path)
        if destination.is_dir():
            destination /= self.filename
        mode = "wb" if overwrite else "xb"
        with destination.open(mode) as output:
            output.write(self.content)
        return destination


def _filename(content_disposition: str) -> str:
    encoded = re.search(r"filename\*=UTF-8''([^;]+)", content_disposition, flags=re.IGNORECASE)
    quoted = re.search(r'filename="([^"]+)"', content_disposition, flags=re.IGNORECASE)
    plain = re.search(r"filename=([^;]+)", content_disposition, flags=re.IGNORECASE)
    candidate = (
        unquote(encoded.group(1))
        if encoded
        else quoted.group(1)
        if quoted
        else plain.group(1).strip()
        if plain
        else "download.bin"
    )
    safe = Path(candidate).name.replace("\x00", "").strip()
    return safe or "download.bin"
