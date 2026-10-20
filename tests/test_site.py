"""Smoke tests for the static MAV Transport Solutions website."""

from __future__ import annotations

import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "services.html", "story.html", "contact.html")


class PageParser(HTMLParser):
    """Collect page IDs, anchors, navigation links, and images."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.navigation_links: list[str] = []
        self.images: list[str] = []
        self.image_alts: list[str | None] = []
        self.in_navigation = False
        self.in_footer = False
        self.footer_links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if element_id := attributes.get("id"):
            self.ids.add(element_id)
        if tag == "nav":
            self.in_navigation = True
        if tag == "footer":
            self.in_footer = True
        if tag == "a" and (href := attributes.get("href")):
            self.links.append(href)
            if self.in_navigation:
                self.navigation_links.append(href)
            if self.in_footer:
                self.footer_links.append(href)
        if tag == "img" and (src := attributes.get("src")):
            self.images.append(src)
            self.image_alts.append(attributes.get("alt"))

    def handle_endtag(self, tag: str) -> None:
        if tag == "nav":
            self.in_navigation = False
        if tag == "footer":
            self.in_footer = False


def parse_page(page_name: str) -> PageParser:
    parser = PageParser()
    parser.feed((ROOT / page_name).read_text(encoding="utf-8"))
    return parser


class StaticWebsiteTests(unittest.TestCase):
    def test_all_expected_pages_exist(self) -> None:
        for page in PAGES:
            with self.subTest(page=page):
                self.assertTrue((ROOT / page).is_file(), f"Missing page: {page}")

    def test_navigation_links_to_all_pages_without_fleet_link(self) -> None:
        for page in PAGES:
            with self.subTest(page=page):
                parser = parse_page(page)
                destinations = {
                    (urlsplit(link).path or page)
                    for link in parser.navigation_links
                }
                self.assertTrue(
                    set(PAGES).issubset(destinations),
                    f"Navigation in {page} should link to every page; got {destinations}",
                )
                self.assertFalse(
                    any("fleet" in link.lower() for link in parser.navigation_links),
                    f"Navigation in {page} should not contain a Fleet link",
                )

    def test_local_links_and_fragments_resolve(self) -> None:
        for page in PAGES:
            parser = parse_page(page)
            for href in parser.links:
                with self.subTest(page=page, href=href):
                    parts = urlsplit(href)
                    if parts.scheme or href.startswith("//"):
                        continue
                    target_path = ROOT / unquote(parts.path) if parts.path else ROOT / page
                    self.assertTrue(target_path.is_file(), f"Broken local link: {href} in {page}")
                    if parts.fragment and target_path.suffix.lower() == ".html":
                        target_parser = parser if target_path.name == page else parse_page(target_path.name)
                        self.assertIn(
                            unquote(parts.fragment),
                            target_parser.ids,
                            f"Broken fragment #{parts.fragment} in {href} on {page}",
                        )

    def test_footer_has_shared_brand_and_all_page_links(self) -> None:
        for page in PAGES:
            content = (ROOT / page).read_text(encoding="utf-8")
            with self.subTest(page=page):
                self.assertIn('class="brand-logo footer-brand"', content, "Footer should use the shared logo")
                self.assertIn("MAV Transport Solutions", content)
                parser = parse_page(page)
                destinations = {Path(urlsplit(link).path).name for link in parser.footer_links if urlsplit(link).path}
                if page == "index.html":
                    destinations.add(page)
                for destination in PAGES:
                    self.assertIn(destination, destinations, f"Footer in {page} should link to {destination}")

    def test_local_image_assets_exist_and_have_alt_text(self) -> None:
        for page in PAGES:
            parser = parse_page(page)
            self.assertIn("mav-logo.svg", parser.images, f"{page} should display the shared logo")
            for src in parser.images:
                parts = urlsplit(src)
                if not parts.scheme and not parts.netloc:
                    with self.subTest(page=page, src=src):
                        self.assertTrue((ROOT / unquote(parts.path)).is_file(), f"Missing image asset: {src}")
            for alt in parser.image_alts:
                self.assertTrue(alt and alt.strip(), f"Images in {page} should have descriptive alt text")

    def test_footer_links_to_all_pages_without_fleet_link(self) -> None:
        for page in PAGES:
            parser = parse_page(page)
            footer_destinations = {link.lower() for link in parser.footer_links}
            with self.subTest(page=page):
                self.assertFalse(
                    any("fleet" in link for link in footer_destinations),
                    f"Footer in {page} should not contain a Fleet link",
                )

    def test_homepage_has_required_enquiry_form(self) -> None:
        content = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="booking-form"', content)
        for field in ("name", "email", "phone", "service", "date", "vehicle"):
            with self.subTest(field=field):
                self.assertIn(f'name="{field}"', content)
        self.assertIn("mailto:info@mavtransport.co.za", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
