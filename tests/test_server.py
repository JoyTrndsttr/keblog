import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'server'))
from content_server import RESEARCH_DOCUMENT, learning_metadata, safe_learning_slug


class ServerTests(unittest.TestCase):
    def test_only_research_log_is_public(self):
        self.assertEqual(RESEARCH_DOCUMENT, ('研究记录.md', '研究记录'))

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

if __name__ == '__main__':
    unittest.main()
