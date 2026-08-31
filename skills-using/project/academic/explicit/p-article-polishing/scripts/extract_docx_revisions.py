#!/usr/bin/env python3
"""Print author-tagged DOCX revisions and comments without modifying the file."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
CP = "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}"
DC = "{http://purl.org/dc/elements/1.1/}"


def get_clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def get_text(node: ET.Element, version: str) -> str:
    if node.tag == W + "ins" and version == "before":
        return ""
    if node.tag == W + "del" and version == "after":
        return ""
    if node.tag in {W + "t", W + "delText"}:
        return node.text or ""
    if node.tag in {W + "tab", W + "br", W + "cr"}:
        return " "
    return "".join(get_text(child, version) for child in node)


def get_authors(node: ET.Element) -> list[str]:
    return sorted(
        {
            child.attrib.get(W + "author", "?")
            for child in node.iter()
            if child.tag in {W + "ins", W + "del"}
        }
    )


def check_author_match(lauthor: list[str], wanted: str | None) -> bool:
    return not wanted or any(wanted.casefold() in author.casefold() for author in lauthor)


def get_clipped_text(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def inspect_docx(
    path_docx: Path,
    wanted_author: str | None,
    max_chars: int,
    show_revisions: bool,
    show_comments: bool,
) -> None:
    with ZipFile(path_docx) as archive:
        set_names = set(archive.namelist())
        document = ET.fromstring(archive.read("word/document.xml"))

        print(f"# {path_docx.name}\n")
        if "docProps/core.xml" in set_names:
            core = ET.fromstring(archive.read("docProps/core.xml"))
            creator = core.findtext(DC + "creator", "")
            modified_by = core.findtext(CP + "lastModifiedBy", "")
            print(f"- Creator: {creator or '?'}")
            print(f"- Last modified by: {modified_by or '?'}\n")

        if show_revisions:
            print("## Tracked revisions\n")
            count = 0
            for index, paragraph in enumerate(document.iter(W + "p"), 1):
                before = get_clean_text(get_text(paragraph, "before"))
                after = get_clean_text(get_text(paragraph, "after"))
                lauthor = get_authors(paragraph)
                if before == after or not check_author_match(lauthor, wanted_author):
                    continue
                count += 1
                print(f"### Paragraph {index} - {', '.join(lauthor)}\n")
                print(f"Before: {get_clipped_text(before, max_chars) or '[empty]'}\n")
                print(f"After: {get_clipped_text(after, max_chars) or '[empty]'}\n")
            if not count:
                print("No matching text revisions.\n")

        if show_comments:
            print("## Comments\n")
            if "word/comments.xml" not in set_names:
                print("No comments.\n")
                return

            dict_anchor: dict[str, str] = {}
            for paragraph in document.iter(W + "p"):
                lcomment_id = [
                    node.attrib.get(W + "id", "")
                    for node in paragraph.iter()
                    if node.tag in {W + "commentRangeStart", W + "commentReference"}
                ]
                for comment_id in lcomment_id:
                    dict_anchor.setdefault(
                        comment_id, get_clean_text(get_text(paragraph, "after"))
                    )

            count = 0
            comments = ET.fromstring(archive.read("word/comments.xml"))
            for comment in comments.iter(W + "comment"):
                author = comment.attrib.get(W + "author", "?")
                if not check_author_match([author], wanted_author):
                    continue
                count += 1
                comment_id = comment.attrib.get(W + "id", "?")
                body = get_clean_text(get_text(comment, "after"))
                anchor = dict_anchor.get(comment_id, "")
                print(f"### Comment {comment_id} - {author}\n")
                print(f"{get_clipped_text(body, max_chars) or '[empty]'}\n")
                print(f"Anchor: {get_clipped_text(anchor, max_chars) or '[not found]'}\n")
            if not count:
                print("No matching comments.\n")


def run_selftest() -> None:
    paragraph = ET.fromstring(
        f"""
        <w:p xmlns:w="{W[1:-1]}">
          <w:r><w:t>A </w:t></w:r>
          <w:del w:author="Mentor"><w:r><w:delText>old</w:delText></w:r></w:del>
          <w:ins w:author="Mentor"><w:r><w:t>new</w:t></w:r></w:ins>
          <w:r><w:t> B</w:t></w:r>
        </w:p>
        """
    )
    assert get_clean_text(get_text(paragraph, "before")) == "A old B"
    assert get_clean_text(get_text(paragraph, "after")) == "A new B"
    assert get_authors(paragraph) == ["Mentor"]
    print("selftest: ok")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", nargs="*", type=Path)
    parser.add_argument("-author", help="case-insensitive author substring")
    parser.add_argument("-max_chars", type=int, default=1200)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-comments_only", action="store_true")
    mode.add_argument("-revisions_only", action="store_true")
    parser.add_argument("-selftest", action="store_true")
    args = parser.parse_args()
    if not args.selftest and not args.docx:
        parser.error("provide at least one DOCX or use -selftest")
    return args


def prepare_output() -> None:
    # Word manuscripts routinely contain Unicode symbols that Windows GBK cannot encode.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
        sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)


def main() -> int:
    prepare_output()
    args = parse_args()
    if args.selftest:
        run_selftest()
        return 0

    lpath_docx = args.docx
    for path_docx in lpath_docx:
        try:
            inspect_docx(
                path_docx.resolve(),
                args.author,
                max(80, args.max_chars),
                not args.comments_only,
                not args.revisions_only,
            )
        except (FileNotFoundError, BadZipFile, KeyError, ET.ParseError) as error:
            print(f"{path_docx}: {error}", file=sys.stderr)
            return 1
    print(f"📊 summary: processed {len(lpath_docx)} DOCX file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
