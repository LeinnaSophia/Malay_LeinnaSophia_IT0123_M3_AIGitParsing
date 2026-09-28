"""Automated checks for the Module 3 combined lab."""

import unittest
from pathlib import Path

from parser_template import build_summary, parse_json, parse_xml, parse_yaml


BASE = Path(__file__).resolve().parent


class ParserTests(unittest.TestCase):
    def test_xml_default_operation(self):
        self.assertEqual(parse_xml(BASE / "network_config.xml")["default_operation"], "merge")

    def test_xml_test_option(self):
        self.assertEqual(parse_xml(BASE / "network_config.xml")["test_option"], "test-then-set")

    def test_json_device_count(self):
        self.assertEqual(parse_json(BASE / "devices.json")["device_count"], 3)

    def test_json_enabled_devices(self):
        self.assertEqual(parse_json(BASE / "devices.json")["enabled_devices"], ["R1", "SW1"])

    def test_json_roles(self):
        self.assertEqual(parse_json(BASE / "devices.json")["roles"], ["router", "switch", "wireless-ap"])

    def test_yaml_window(self):
        result = parse_yaml(BASE / "maintenance.yaml")
        self.assertEqual((result["name"], result["approved"], result["duration_minutes"]), ("Saturday-Lab", True, 90))

    def test_combined_summary(self):
        result = build_summary(
            BASE / "network_config.xml",
            BASE / "devices.json",
            BASE / "maintenance.yaml",
        )
        self.assertEqual(set(result), {"xml", "json", "yaml"})
        self.assertEqual(result["yaml"]["devices"], ["R1", "SW1"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
