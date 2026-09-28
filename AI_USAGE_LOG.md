# AI Usage and Validation Log

Student name: Leinna Sophia B. Malay
Section: TN32
AI tool used: DeepSeek

## Predictions before using AI
# Entry 1 - XML parsing
- The line <rpc message-id=”101” xmlns=”urn:ietf:params:xml:ns:netconf:base:1.0”> defines the NETCONF namespace as an attribute of xmlns.
- The edit config elements are the code lines enclosed between the <edit-config> and the </edit-config> tags.
- The default operation, enclosed in between <default-operation> and </default-operation> is “merge.” 
- The test option, enclosed in between <test-option> and </test-option> is “test-then-set.” 

# Entry 2 - JSON parsing
- The top-level keys are "site" and "devices".
The value of "devices" is a list; each member of the list is an object (dictionary) whose keys are "hostname", "management_ip", "role", and "enabled".
- The only boolean field is "enabled", which is either true or false.
- The fields most useful for the summary are "hostname", "role", and "enabled.” The fields "hostname" and "role" identify the device, while "enabled" reveals its status, making problems easy to spot in the report. - This also highlights why the device's role matters as the importance of whether a device is enabled or not depends on context of what the device is supposed to do. "management_ip" may be included, but it is less important compared to the others; it only tells you the device's address and location, and gives no useful signal for error or bug diagnostics.

# Entry 3 - YAML parsing and integration
- The following code block contains the nested mapping containing the window’s fields 
window:
	  name: Saturday-Lab  #this is the window’s name
	  approved: true #this holds the boolean value of true
	  duration_minutes: 90 #this holds the duration_minutes of 90
- The list of devices contains R1 and SW1
- The action is “validate-configuration.”

## Entry 1 - XML parsing

Prompt: 
I am completing an authorized classroom Python lab.
Review this function stub and the supplied fictional XML structure.
Recommend an implementation that returns exactly the keys described in the docstring.
Explain namespace handling, data types, error risks, and each library function used.
Do not invent files, credentials, network calls, or expected test results.
I will validate your recommendation using unit tests and Git diffs.

Function stub:
def parse_xml(path: str | Path) -> dict:
    """Return default_operation and test_option from the NETCONF-style XML."""
    # TODO: parse the XML, handle its default namespace, and return two strings.
    raise NotImplementedError("Complete parse_xml")

Relevant fictional data: 
<?xml version="1.0" encoding="UTF-8"?>
<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"> 
  <edit-config>  
    <target>
      <candidate />
    </target>
    <default-operation>merge</default-operation>
    <test-option>test-then-set</test-option> 
    <config>
      <interface xmlns="urn:example:network">
        <name>GigabitEthernet1</name>
        <enabled>true</enabled>
      </interface>
    </config>
  </edit-config>
</rpc>


AI recommendation summary:
Suggested code: 
from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET


def parse_xml(path: str | Path) -> dict:
    """Return default_operation and test_option from the NETCONF-style XML."""
    root = ET.parse(str(path)).getroot()

    # Root element declares the default namespace via xmlns="urn:ietf:params:xml:ns:netconf:base:1.0".
    # ElementTree expands that into a Clark notation URI on every tag in that namespace.
    # The nested <interface> redeclares xmlns="urn:example:network", so its tags
    # live in a different namespace. We only need the NETCONF-namespaced elements.
    netconf_ns = "urn:ietf:params:xml:ns:netconf:base:1.0"
    ns = {"nc": netconf_ns}

    default_operation = root.findtext(
        "nc:edit-config/nc:default-operation", namespaces=ns
    )
    test_option = root.findtext(
        "nc:edit-config/nc:test-option", namespaces=ns
    )

    return {
        "default_operation": default_operation,
        "test_option": test_option,
    }

The AI's recommendation included using the xml.etree.ElementTree for parsing and pathlib.Path for the type hint. It uses the parse_xml(path) function to open an XML file. The AI's suggested code hard codes the URI as a literal string using the lines netconf_ns = "urn:ietf:params:xml:ns:netconf:base:1.0" and ns = {"nc": netconf_ns}. The AI's suggestion for finding elements was done in path style, using prefix notation and namespaces= mapping. This method would end up having only one traversal per value, looking up the target once directly using findtext. It also uses from __future__ import annotations for importing and str(path) for parsing.


Decision: modified
My code:
def parse_xml(path: str | Path) -> dict:
    """Return default_operation and test_option from the NETCONF-style XML."""
    # TODO: parse the XML, handle its default namespace, and return two strings.
    import re 

    xml = ET.parse(path)
    root = xml.getroot()

    ns = re.match(r'\{(.*)\}', root.tag).group(1)
    editconf = root.find("{{{}}}edit-config".format(ns))

    default_operation = editconf.find("{{{}}}default-operation".format(ns))
    test_option = editconf.find("{{{}}}test-option".format(ns))

    return {
        "default_operation": default_operation.text,
        "test_option": test_option.text 
    }


My code was modeled after what was taught in the "Parse Different Data Types with Python" lab. Instead of using the NETCONF URI directly and building a prefix map, I used the re library to extract the URI out of the root.tag with regex. In my case, it captures the string inside the {}, since Python reads the XML file as {URI}edit-config (for example) when it looks up the URI in the tags. This approach can be applied to any namespace. I used the same string formatting notation from the other lab, but mine uses {{{}}} instead of just {}. The outer {{ }} produces literal braces, while the inner {} inserts the extracted URI (used with .format(ns)). This leads to two child lookups. I used find instead of findtext to locate the needed text. I also removed the raise NotImplementedError at the end.

Validation evidence:  
leinna_sophia@Sophie-Laptop:~/it0123-module3-ai-git-parsing$ python3 -m unittest -v
test_combined_summary (test_parser.ParserTests.test_combined_summary) ... ERROR
test_json_device_count (test_parser.ParserTests.test_json_device_count) ... ERROR
test_json_enabled_devices (test_parser.ParserTests.test_json_enabled_devices) ... ERROR
test_json_roles (test_parser.ParserTests.test_json_roles) ... ERROR
test_xml_default_operation (test_parser.ParserTests.test_xml_default_operation) ... ok
test_xml_test_option (test_parser.ParserTests.test_xml_test_option) ... ok
test_yaml_window (test_parser.ParserTests.test_yaml_window) ... ERROR

## Entry 2 - JSON parsing

Prompt:
I am completing an authorized classroom Python lab.
Review this function stub and the supplied fictional JSON structure.
Recommend an implementation that returns exactly the keys described in the docstring.
Explain namespace handling, data types, error risks, and each library function used.
Do not invent files, credentials, network calls, or expected test results.
I will validate your recommendation using unit tests and Git diffs.

Function stub:
def parse_json(path: str | Path) -> dict:
    """Return site, device_count, enabled_devices, and roles from the JSON."""
    # TODO: use json.load and derive the requested summary values.
    raise NotImplementedError("Complete parse_json")

Relevant fictional data: 
{
  "site": "FEU-Tech-Lab",
  "devices": [  
    {
      "hostname": "R1",
      "management_ip": "192.0.2.10",
      "role": "router",
      "enabled": true
    },
    {
      "hostname": "SW1",
      "management_ip": "192.0.2.20",
      "role": "switch",
      "enabled": true
    },
    {
      "hostname": "AP1",
      "management_ip": "192.0.2.30",
      "role": "wireless-ap",
      "enabled": false
    }
  ]
}

AI recommendation summary:
Suggested code:
from __future__ import annotations

from pathlib import Path
import json


def parse_json(path: str | Path) -> dict:
    """Return site, device_count, enabled_devices, and roles from the JSON."""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    devices = data["devices"]

    return {
        "site": data["site"],
        "device_count": len(devices),
        "enabled_devices": sum(1 for d in devices if d["enabled"]),
        "roles": [d["role"] for d in devices],
    }

This code used the annotations module from the __future__ library and the Path module from the pathlib library. It uses the open function and json.load() to open the JSON file in read mode and then load it, and includes encoding="utf-8" to provide a defined encoding format rather than relying on the OS locale, which might otherwise need adjusting. It also stores data["devices"] in the variable devices for more efficient access. It returns the site, the device count using the length of the devices array, and for enabled_devices, it counts the number of devices with the "enabled" field set to True. The code also uses d as an alias for each device in the iteration. For roles, it uses a list comprehension to return a list of the role of each device.

Decision: modified
My code:
def parse_json(path: str | Path) -> dict:
    """Return site, device_count, enabled_devices, and roles from the JSON."""
    # TODO: use json.load and derive the requested summary values.

    with open(path, "r") as json_file:
        data = json.load(json_file)

    return {
        "site": data["site"],
        "device_count": len(data["devices"]),
        "enabled_devices": [device["hostname"] for device in data["devices"] if device["enabled"]],
        "roles": [device["role"] for device in data["devices"]]
    }

I also used the method taught in the "Parse Different Data Types with Python" lab for this, and I found it to be a simpler and more straightforward implementation than what the AI suggested. It looks the same, but with minor differences. First, I used different variable names. Second, I did not store data["devices"] in another variable and instead accessed its contents directly in my return block. For enabled_devices, since the docstring in the function stub did not explicitly say that I should count the number of enabled devices, I returned a list of their hostnames instead.

Validation evidence:
leinna_sophia@Sophie-Laptop:~/it0123-module3-ai-git-parsing$ python3 -m unittest -v
test_combined_summary (test_parser.ParserTests.test_combined_summary) ... ERROR
test_json_device_count (test_parser.ParserTests.test_json_device_count) ... ok
test_json_enabled_devices (test_parser.ParserTests.test_json_enabled_devices) ... ok
test_json_roles (test_parser.ParserTests.test_json_roles) ... ok
test_xml_default_operation (test_parser.ParserTests.test_xml_default_operation) ... ok
test_xml_test_option (test_parser.ParserTests.test_xml_test_option) ... ok
test_yaml_window (test_parser.ParserTests.test_yaml_window) ... ERROR

## Entry 3 - YAML parsing and integration

Prompt:
I am completing an authorized classroom Python lab.
Review this function stub and the supplied fictional YAML structure.
Recommend an implementation that returns exactly the keys described in the docstring.
Explain namespace handling, data types, error risks, and each library function used.
Do not invent files, credentials, network calls, or expected test results.
I will validate your recommendation using unit tests and Git diffs.

Function stub:
def parse_yaml(path: str | Path) -> dict:
    """Return name, approved, duration_minutes, devices, and action from YAML."""
    # TODO: use yaml.safe_load and return the normalized maintenance summary.
    raise NotImplementedError("Complete parse_yaml")


Relevant fictional data: 
window:  
  name: Saturday-Lab 
  approved: true  
  duration_minutes: 90  
devices: 
  - R1
  - SW1
action: validate-configuration  

AI recommendation summary:
Suggested Code:
from __future__ import annotations

from pathlib import Path
import yaml


def parse_yaml(path: str | Path) -> dict:
    """Return name, approved, duration_minutes, devices, and action from YAML."""
    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    window = data["window"]

    return {
        "name": window["name"],
        "approved": window["approved"],
        "duration_minutes": window["duration_minutes"],
        "devices": data["devices"],
        "action": data["action"],
    }

The AI suggested using __future__, pathlib, and yaml. It opened the YAML file in read mode using with encoding="utf-8" and loaded it using yaml.safe_load() so the file does not depend on the OS default encoding. It also stored data["window"] in a variable called window so the return block would not have to repeat the nested lookup three times for efficient data retrieval. The rest of the return dict pulls devices and action straight from the top level.

Decision: modified
My Code:
def parse_yaml(path: str | Path) -> dict:
    """Return name, approved, duration_minutes, devices, and action from YAML."""
    # TODO: use yaml.safe_load and return the normalized maintenance summary.

    with open(path, "r") as yaml_file:
        data = yaml.safe_load(yaml_file)

    return {
        "name": data["window"]["name"],
        "approved": data["window"]["approved"],
        "duration_minutes": data["window"]["duration_minutes"],
        "devices": data["devices"],
        "action": data["action"]
    }

Mine returns the same dict as the AI's version for this data, so the parsing logic is the same. Like in my previous codes, I used the method from the "Parse Different Data Types with Python" lab. The differences are that I did not use the __future__ import, I did not add encoding="utf-8" to open, and I did not store data["window"] in a variable and instead used direct indexing in the return block. The missing encoding is the one that could matter if the file ever has non-ASCII text, since it would then fall back to the OS default.

Validation evidence:
leinna_sophia@Sophie-Laptop:~/it0123-module3-ai-git-parsing$ python3 -m unittest -v
test_combined_summary (test_parser.ParserTests.test_combined_summary) ... ERROR
test_json_device_count (test_parser.ParserTests.test_json_device_count) ... ok
test_json_enabled_devices (test_parser.ParserTests.test_json_enabled_devices) ... ok
test_json_roles (test_parser.ParserTests.test_json_roles) ... ok
test_xml_default_operation (test_parser.ParserTests.test_xml_default_operation) ... ok
test_xml_test_option (test_parser.ParserTests.test_xml_test_option) ... ok
test_yaml_window (test_parser.ParserTests.test_yaml_window) ... ok

## Controlled merge-conflict line

Validation status: Tests passed 

## Final reflection

Describe one AI suggestion that you changed or rejected and explain the evidence that guided your decision.
