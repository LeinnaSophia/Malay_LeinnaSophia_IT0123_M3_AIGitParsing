"""Module 3 combined lab starter.

Complete each function with help from an approved AI tool, then verify every
claim and code change using the supplied unit tests. The files contain only
fictional classroom data.
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml


def parse_xml(path: str | Path) -> dict:
    """Return default_operation and test_option from the NETCONF-style XML."""
    # TODO: parse the XML, handle its default namespace, and return two strings.
    raise NotImplementedError("Complete parse_xml")


def parse_json(path: str | Path) -> dict:
    """Return site, device_count, enabled_devices, and roles from the JSON."""
    # TODO: use json.load and derive the requested summary values.
    raise NotImplementedError("Complete parse_json")


def parse_yaml(path: str | Path) -> dict:
    """Return name, approved, duration_minutes, devices, and action from YAML."""
    # TODO: use yaml.safe_load and return the normalized maintenance summary.
    raise NotImplementedError("Complete parse_yaml")


def build_summary(xml_path: str | Path, json_path: str | Path, yaml_path: str | Path) -> dict:
    """Combine the three parser results into one dictionary."""
    # TODO: call the three parser functions and preserve the keys below.
    raise NotImplementedError("Complete build_summary")


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    summary = build_summary(
        base / "network_config.xml",
        base / "devices.json",
        base / "maintenance.yaml",
    )
    print(json.dumps(summary, indent=2))
