"""Validate Elementor elements (including HTML tables) and package a copy-only HTML helper."""
import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse


def validate(elements):
    if not isinstance(elements, list) or not elements:
        raise ValueError('Expected a non-empty elements array, not a template export')
    seen = set()

    def walk(items):
        for item in items:
            if not isinstance(item, dict):
                raise ValueError('Each element must be an object')
            ident = item.get('id', '')
            if not isinstance(ident, str) or not re.fullmatch(r'[0-9a-fA-F]{7,8}', ident) or ident in seen:
                raise ValueError(f'Invalid or duplicate element id: {ident}')
            seen.add(ident)
            kind = item.get('elType')
            if kind not in ('container', 'widget'):
                raise ValueError(f'Unsupported element type: {kind}')
            settings = item.get('settings')
            if not isinstance(settings, dict) or not re.search(r'[\u4e00-\u9fff]', str(settings.get('_title', ''))):
                raise ValueError(f'Chinese navigator name missing: {ident}')
            if not isinstance(item.get('isInner'), bool):
                raise ValueError(f'isInner must be boolean: {ident}')
            children = item.get('elements')
            if not isinstance(children, list):
                raise ValueError(f'elements must be an array: {ident}')
            if kind == 'widget':
                widget = item.get('widgetType')
                if not isinstance(widget, str) or not widget or widget.startswith('e-'):
                    raise ValueError(f'Forbidden or missing widget type: {widget}')
                if widget == 'html':
                    markup = settings.get('html')
                    if not isinstance(markup, str) or not re.search(r'<table\b[^>]*>.*?</table\s*>', markup, re.I | re.S):
                        raise ValueError(f'HTML widget must contain table markup in settings.html: {ident}')
            walk(children)
    walk(elements)
    return len(seen)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--elements', required=True, type=Path)
    parser.add_argument('--siteurl', required=True)
    parser.add_argument('--title', default='复制 Elementor 模块')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    url = urlparse(args.siteurl)
    if url.scheme not in ('https', 'http') or not url.netloc or url.username or url.password:
        raise ValueError('siteurl must be an HTTP(S) REST root URL without credentials')
    if args.output.suffix.lower() != '.html':
        raise ValueError('Output must be a copy-helper .html file')
    elements = json.loads(args.elements.read_text(encoding='utf-8-sig'))
    count = validate(elements)
    payload = {'type': 'elementor', 'siteurl': args.siteurl, 'elements': elements}
    encoded = json.dumps(payload, ensure_ascii=False, separators=(',', ':'), allow_nan=False).replace('<', '\\u003c')
    template = (Path(__file__).resolve().parents[1] / 'assets/copy-page.html').read_text(encoding='utf-8')
    page = template.replace('__PAGE_TITLE__', html.escape(args.title)).replace('__ELEMENTOR_PAYLOAD__', encoded)
    embedded = re.search(r'<script id="payload" type="application/json">(.*?)</script>', page, re.S)
    if not embedded or json.loads(embedded[1]) != payload:
        raise ValueError('Embedded payload round-trip failed')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as output:
        output.write(page)
    print(f'Validated {count} elements; created {args.output}')


if __name__ == '__main__':
    main()
