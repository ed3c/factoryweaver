"""Course catalog structural coverage. This does not certify slide or model reading."""
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1] / "docs/courses/cs329z-fall-2026"

class CourseCollectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads((ROOT/"course-manifest.json").read_text(encoding="utf-8"))
    def test_all_weeks_have_source_class_cardboxes(self):
        cs=self.manifest["chapters"]
        self.assertEqual([c["week"] for c in cs],list(range(1,12)))
        for c in cs:
            p=ROOT/"chapters"/c["slug"]
            for part in ["README.md","cards.md","slides/cards.md","readings/cards.md","homework/cards.md"]:
                with self.subTest(week=c["week"],part=part):
                    self.assertTrue((p/part).is_file())
    def test_source_catalog_no_fake_extraction(self):
        cs=self.manifest["chapters"]
        self.assertEqual(sum(bool(l["slides_url"]) for c in cs for l in c["lectures"]),5)
        self.assertEqual(sum(len(c["readings"]) for c in cs),50)
        for c in cs:
            for l in c["lectures"]:
                self.assertIn(l["slides_status"],("LISTED_PDF_BODY_NOT_REVIEWED","NOT_LISTED"))
            for r in c["readings"]:
                self.assertEqual(r["content_status"],"TITLE_AND_LINK_ONLY")
    def test_master_integrates_every_chapter(self):
        master=(ROOT/"MASTER-CARD-BOX.md").read_text()
        for c in self.manifest["chapters"]:
            self.assertIn("chapters/"+c["slug"]+"/cards.md",master)
        for target in ["HW1.md","HW2.md","FINAL-PROJECT.md","K-slides","K-readings"]:
            self.assertIn(target,master)
    def test_homework_release_and_recess_honesty(self):
        self.assertIn("NOT_PUBLISHED",self.manifest["homework"][1]["status"])
        self.assertIsNone(self.manifest["homework"][1]["url"])
        self.assertFalse(self.manifest["chapters"][9]["has_teaching"])
        self.assertIn("NOOP",(ROOT/"chapters"/self.manifest["chapters"][9]["slug"]/"cards.md").read_text())
