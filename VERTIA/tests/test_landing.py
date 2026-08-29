from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class LandingTests(unittest.TestCase):
    def setUp(self):
        self.index = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        self.config = (ROOT / "netlify.toml").read_text(encoding="utf-8")

    def test_netlify_publish_directory(self):
        self.assertIn('publish = "site"', self.config)

    def test_netlify_deployment_files_exist(self):
        self.assertTrue((ROOT / ".env.netlify.example").is_file())
        self.assertTrue((ROOT / "scripts" / "netlify_deploy.ps1").is_file())
        self.assertTrue((ROOT / "scripts" / "netlify_api.py").is_file())

    def test_netlify_form_is_configured(self):
        self.assertIn('data-netlify="true"', self.index)
        self.assertIn('name="form-name" value="interet-vertia"', self.index)
        self.assertIn('data-netlify-honeypot="website"', self.index)

    def test_required_fields_are_present(self):
        self.assertIn('name="email" type="email"', self.index)
        self.assertIn('id="consent" name="consent" type="checkbox" required', self.index)

    def test_values_are_present(self):
        self.assertIn("Écoresponsabilité", self.index)
        self.assertIn("Éthique", self.index)
        self.assertIn("Durabilité", self.index)
        self.assertIn("l'IA assiste le jugement humain", self.index)

    def test_legal_and_confirmation_pages_exist(self):
        self.assertTrue((ROOT / "site" / "merci" / "index.html").is_file())
        self.assertTrue((ROOT / "site" / "confidentialite.html").is_file())


if __name__ == "__main__":
    unittest.main()
