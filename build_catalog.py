import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CATEGORIES = ('Particles', 'Flipbooks', 'Beams', 'Trails')
EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp'}


def main():
    catalog_path = ROOT / 'textures.json'
    previous = json.loads(catalog_path.read_text(encoding='utf-8')) if catalog_path.exists() else {}
    previous_by_path = {item.get('source'): item for item in previous.get('textures', []) if isinstance(item, dict)}
    entries = []
    for category in CATEGORIES:
        folder = ROOT / 'textures' / category
        if not folder.exists():
            continue
        for path in sorted(folder.rglob('*')):
            if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
                continue
            relative = path.relative_to(ROOT).as_posix()
            old = previous_by_path.get(relative, {})
            entry = dict(old)
            entry.update({'name': old.get('name') or path.stem.replace('_', ' ').replace('-', ' '),
                          'category': category,
                          'source': relative,
                          'assetId': old.get('assetId', '')})
            entries.append(entry)
    result = {'version': 1, 'textures': entries}
    catalog_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'Cataloged {len(entries)} texture(s).')


if __name__ == '__main__':
    main()
