#!/usr/bin/env python3
"""Invoke a provider-neutral raster image command through a JSON stdin contract."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path


OUTPUT_FORMATS = {
    ".jpeg": "jpeg",
    ".jpg": "jpeg",
    ".png": "png",
    ".webp": "webp",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", help="Complete style-locked prompt")
    prompt_group.add_argument("--prompt-file", help="UTF-8 file containing the prompt")
    parser.add_argument("--output", required=True, help="PNG, JPEG, or WebP output path")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing regular output file",
    )
    parser.add_argument(
        "provider_command",
        nargs=argparse.REMAINDER,
        help="Provider executable and arguments after --",
    )
    args = parser.parse_args()
    if args.provider_command and args.provider_command[0] == "--":
        args.provider_command = args.provider_command[1:]
    if not args.provider_command:
        parser.error("a provider command is required after --")
    return args


def load_prompt(args: argparse.Namespace) -> str:
    prompt = (
        Path(args.prompt_file).expanduser().read_text(encoding="utf-8")
        if args.prompt_file
        else args.prompt
    )
    clean_prompt = prompt.strip()
    if not clean_prompt:
        raise ValueError("prompt must not be empty")
    return clean_prompt


def validate_output(output: Path, *, force: bool) -> str:
    output_format = OUTPUT_FORMATS.get(output.suffix.lower())
    if output_format is None:
        raise ValueError("--output must end in .png, .jpg, .jpeg, or .webp")
    if output.is_symlink():
        raise ValueError(f"output is a symbolic link: {output}")
    if output.exists() and not output.is_file():
        raise ValueError(f"output is not a regular file: {output}")
    if output.exists() and not force:
        raise FileExistsError(f"refusing to overwrite existing output: {output}")

    parent = output.parent
    while not parent.exists():
        if parent.is_symlink():
            raise ValueError(f"output parent is a symbolic link: {parent}")
        parent = parent.parent
    if parent.is_symlink() or not parent.is_dir():
        raise ValueError(f"output parent is unsafe: {parent}")
    return output_format


def has_raster_signature(path: Path, output_format: str) -> bool:
    contents = path.read_bytes()
    if output_format == "png":
        return contents.startswith(b"\x89PNG\r\n\x1a\n")
    if output_format == "jpeg":
        return contents.startswith(b"\xff\xd8\xff")
    if output_format == "webp":
        return (
            len(contents) >= 12
            and contents.startswith(b"RIFF")
            and contents[8:12] == b"WEBP"
        )
    return False


def invoke(
    *,
    provider_command: list[str],
    prompt: str,
    output: Path,
    output_format: str,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output.name}.",
        suffix=f".{output_format}",
        dir=output.parent,
    )
    os.close(file_descriptor)
    temporary_path = Path(temporary_name)
    temporary_path.unlink()
    request = json.dumps(
        {
            "prompt": prompt,
            "output": str(temporary_path.resolve()),
            "format": output_format,
        }
    )
    try:
        result = subprocess.run(
            provider_command,
            input=request,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"provider command failed with exit code {result.returncode}"
            )
        if not temporary_path.is_file() or temporary_path.is_symlink():
            raise RuntimeError("provider command did not create a regular output file")
        if not has_raster_signature(temporary_path, output_format):
            raise RuntimeError(
                f"provider command did not create a valid {output_format} raster"
            )
        os.replace(temporary_path, output)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def main() -> None:
    args = parse_args()
    output = Path(args.output).expanduser().absolute()
    try:
        prompt = load_prompt(args)
        output_format = validate_output(output, force=args.force)
        invoke(
            provider_command=args.provider_command,
            prompt=prompt,
            output=output,
            output_format=output_format,
        )
    except (FileExistsError, OSError, RuntimeError, ValueError) as error:
        print(f"Image provider invocation failed: {error}")
        raise SystemExit(1) from error

    print(f"Saved generated image: {output.resolve()}")


if __name__ == "__main__":
    main()
