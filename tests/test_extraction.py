
import pytest
import requests

from src.data.extraction import ExtractionError, download_file


class FakeResponse:
    def __init__(self, chunks, status=200):
        self.chunks = chunks
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def raise_for_status(self):
        if self.status >= 400:
            raise requests.HTTPError(str(self.status))

    def iter_content(self, chunk_size):
        yield from self.chunks


class FakeSession:
    def __init__(self, response):
        self.response = response

    def get(self, *args, **kwargs):
        return self.response


def test_download_writes_exact_bytes(runtime_path):
    target = runtime_path / "sample.bin"
    download_file("https://example.test/file", target, session=FakeSession(FakeResponse([b"abc", b"123"])))
    assert target.read_bytes() == b"abc123"


def test_empty_download_fails(runtime_path):
    with pytest.raises(ExtractionError, match="Empty response"):
        download_file(
            "https://example.test/empty",
            runtime_path / "empty",
            retries=1,
            session=FakeSession(FakeResponse([])),
        )
