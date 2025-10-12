"""Tests for nitpick.load_token module."""

from pathlib import Path
from unittest.mock import patch

import pytest

from nitpick import load_token


class TestLoad:
    """Tests for load function."""

    def test_load_success(self, tmp_path: Path) -> None:
        """Test successful token loading."""
        token_file = tmp_path / "token.txt"
        test_token = "test_token_value"
        token_file.write_text(test_token)

        with patch.object(load_token, "LOADING_FILE_ORDER", [str(token_file)]):
            result = load_token.load()
            assert result == test_token

    def test_load_with_whitespace(self, tmp_path: Path) -> None:
        """Test token loading with surrounding whitespace."""
        token_file = tmp_path / "token.txt"
        test_token = "token_with_spaces"
        token_file.write_text(f"  {test_token}  \n")

        with patch.object(load_token, "LOADING_FILE_ORDER", [str(token_file)]):
            result = load_token.load()
            assert result == test_token

    def test_load_empty_token(self, tmp_path: Path) -> None:
        """Test TokenLoadError when token is empty."""
        token_file = tmp_path / "token.txt"
        token_file.write_text("")

        with (
            patch.object(load_token, "LOADING_FILE_ORDER", [str(token_file)]),
            pytest.raises(load_token.TokenLoadError, match="Token is empty in file"),
        ):
            load_token.load()

    def test_load_whitespace_only_token(self, tmp_path: Path) -> None:
        """Test TokenLoadError when token contains only whitespace."""
        token_file = tmp_path / "token.txt"
        token_file.write_text("   \n")

        with (
            patch.object(load_token, "LOADING_FILE_ORDER", [str(token_file)]),
            pytest.raises(load_token.TokenLoadError, match="Token is empty in file"),
        ):
            load_token.load()

    def test_load_multiline_file(self, tmp_path: Path) -> None:
        """Test that only first line is read from multiline file."""
        token_file = tmp_path / "token.txt"
        test_token = "first_line_token"
        token_file.write_text(f"{test_token}\nsecond_line\nthird_line")

        with patch.object(load_token, "LOADING_FILE_ORDER", [str(token_file)]):
            result = load_token.load()
            assert result == test_token

    def test_load_file_not_found(self, tmp_path: Path) -> None:
        """Test FileNotFoundError when no token file exists."""
        nonexistent_path = tmp_path / "nonexistent.txt"

        with (
            patch.object(load_token, "LOADING_FILE_ORDER", [str(nonexistent_path)]),
            pytest.raises(FileNotFoundError),
        ):
            load_token.load()

    def test_load_finds_second_file_when_first_missing(self, tmp_path: Path) -> None:
        """Test that load finds second file when first doesn't exist."""
        first_path = tmp_path / "nonexistent.txt"
        second_path = tmp_path / "token.txt"
        test_token = "second_file_token"
        second_path.write_text(test_token)

        with patch.object(load_token, "LOADING_FILE_ORDER", [str(first_path), str(second_path)]):
            result = load_token.load()
            assert result == test_token

    def test_load_skips_directory(self, tmp_path: Path) -> None:
        """Test that load skips directories and finds actual file."""
        directory = tmp_path / "token_dir"
        directory.mkdir()
        token_file = tmp_path / "token.txt"
        test_token = "directory_skip_token"
        token_file.write_text(test_token)

        with patch.object(load_token, "LOADING_FILE_ORDER", [str(directory), str(token_file)]):
            result = load_token.load()
            assert result == test_token


class TestTokenLoadError:
    """Tests for TokenLoadError exception."""

    def test_token_load_error_inheritance(self) -> None:
        """Test that TokenLoadError inherits from Exception."""
        error = load_token.TokenLoadError("test error")
        assert isinstance(error, Exception)

    def test_token_load_error_message(self) -> None:
        """Test TokenLoadError with custom message."""
        message = "Custom error message"
        error = load_token.TokenLoadError(message)
        assert str(error) == message
