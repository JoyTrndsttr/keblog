import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'server'))
from server import append_paper_entry, atomic_write, learning_metadata, safe_learning_slug, safe_name


class ServerTests(unittest.TestCase):
    def test_safe_name_rejects_traversal(self):
        with self.assertRaises(ValueError):
            safe_name('../paperpool.md', {'.md'})

    def test_learning_slug_and_metadata(self):
        slug = safe_learning_slug('260909-KeWang-ReCoReBench')
        metadata = learning_metadata(
            slug,
            '# 中文标题\n\n> 论文：*Code Refinement with Repository Context: How Far are We?*  \n> DOI：10.1145/3820059\n',
            '2026-09-09T00:00:00+00:00',
        )
        self.assertEqual(metadata['date'], '2026-09-09')
        self.assertEqual(metadata['author'], 'KeWang')
        self.assertEqual(metadata['title'], 'Code Refinement with Repository Context: How Far are We?')
        with self.assertRaises(ValueError):
            safe_learning_slug('../260909-KeWang-Paper')

    def test_append_entry_and_deduplicate(self):
        entry = {'date': '2026-09-09', 'title': 'A Causal Paper', 'authors': 'A; B', 'venue': 'ICSE 2027', 'link': 'https://doi.org/10.1000/test', 'topics': 'causality', 'value': 'useful'}
        updated = append_paper_entry('# Paper Pool\n', entry)
        self.assertIn('A Causal Paper', updated)
        with self.assertRaises(FileExistsError):
            append_paper_entry(updated, entry)

    def test_atomic_write_creates_backup(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / 'paperpool.md'
            backup = root / 'backups'
            atomic_write(target, b'one', backup)
            atomic_write(target, b'two', backup)
            self.assertEqual(target.read_bytes(), b'two')
            self.assertEqual(len(list(backup.iterdir())), 1)


if __name__ == '__main__':
    unittest.main()
