# AI-Assisted Git Workflow and Python Data Parsing

Student name: Leinna Sophia B. Malay
Section: TN35

## Project purpose

This repository combines Git version control with XML, JSON, and YAML parsing by creating branches for making changes to certain features. For example, the `feature/data-parsers` branch was used for staging the `parser_template.py` file used for XML, JSON, and YAML parsing, and incrementally committing the changes added to it before merging it with the files in the `main` branch. This keeps the working process organized, since changes are not immediately seen in `main`; instead, changes are first localized to a dedicated branch, which helps avoid introducing major mistakes into `main`. Errors can be resolved in the `feature/data-parsers` branch first before it is merged with `main`. In the event of a conflict, I can also resolve it by editing the conflicted file in vim.

## How to run

I used my Windows Subsystem for Linux (WSL) terminal to complete this activity. This brief how-to-run guide uses Linux commands, so it is recommended that readers do the same. If they do not use a Linux OS, they may use a virtual machine such as the DEVASC VM instead.

The commands to use are:

```bash
cd [path to it0123-module3-ai-git-parsing/starter]
python3 parser_template.py
python3 -m unittest -v
```

## Git workflow summary

The branches I created are seen in the output of the `git branch` command:

```text
leinna_sophia@Sophie-Laptop:~/it0123-module3-ai-git-parsing$ git branch
  docs/ai-note
  feature/data-parsers
* main
```

The major commits I made are visible using the `git log --oneline --graph --decorate --all` command:

```text
leinna_sophia@Sophie-Laptop:~/it0123-module3-ai-git-parsing$ git log --oneline --graph --decorate --all
*   374138c (HEAD -> main) merge: reconcile AI and test validation notes
|\
| * c114b35 (docs/ai-note) docs: record AI review status
* | 9e278fb docs: record test validation status
|/
* 5fdd541 (feature/data-parsers) Completed build summary by returning the return values of the functions parse_xml, parse_json, and parse_yaml after passing their path
* 304709e feat: implement verified data parsers
* 0c0ace2 feat: implement verified data parsers
* 6340919 feat: implement verified data parsers
* e23a24c chore: add parser lab starter files
```

For the merge conflict between `main` and `docs/ai-note`, I opened `AI_USAGE_LOG.md` in vim while on the `main` branch. Inside the text editor, I removed the conflict markers and edited the file so that it read `Validation status: AI reviewed and tests passed`. After this, I was able to stage and commit the file to finish the merge.

## Parser results

My updated `parser_template.py` file was validated using the `test_parser.py` file. The verified XML, JSON, and YAML values are:

For XML:

- `"default-operation"`: `"merge"`
- `"test_option"`: `"test-then-set"`

For JSON:

- `"site"`: `"FEU-Tech-Lab"`
- `"device_count"`: `3`
- `"enabled_devices"`: `["R1", "SW1"]`
- `"roles"`: `["router", "switch", "wireless-ap"]`

For YAML:

- `"name"`: `"Saturday-Lab"`
- `"approved"`: `true`
- `"duration"`: `90`
- `"devices"`: `["R1", "SW1"]`
- `"action"`: `"validate configuration"`

The validation results are:

```text
leinna_sophia@Sophie-Laptop:~/it0123-module3-ai-git-parsing$ python3 -m unittest -v
test_combined_summary (test_parser.ParserTests.test_combined_summary) ... ok
test_json_device_count (test_parser.ParserTests.test_json_device_count) ... ok
test_json_enabled_devices (test_parser.ParserTests.test_json_enabled_devices) ... ok
test_json_roles (test_parser.ParserTests.test_json_roles) ... ok
test_xml_default_operation (test_parser.ParserTests.test_xml_default_operation) ... ok
test_xml_test_option (test_parser.ParserTests.test_xml_test_option) ... ok
test_yaml_window (test_parser.ParserTests.test_yaml_window) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.006s

OK
```

## AI disclosure

I used DeepSeek to generate reference implementations for all three parsers. For `parse_xml`, I modified the AI's approach by using `re` to extract the namespace URI from `root.tag` instead of hardcoding it and building a prefix map, which makes the code work with any namespace rather than just the one in the stub. For `parse_json`, I rejected the AI's interpretation of `enabled_devices` as a count and instead returned a list of hostnames, since the docstring did not specify a count; the passing test `test_json_enabled_devices` confirmed my reading was correct. For `parse_yaml`, I kept the same parsing logic but dropped the `__future__` import, the `encoding="utf-8"` argument, and the intermediate `window` variable, using direct indexing in the return block instead. I validated all three parsers by running `python3 -m unittest -v` from the starter directory, which ran all seven tests and returned `OK`, confirming that my modifications produce the expected outputs.

## Safety statement

I only submitted the function stubs and the fictional data to DeepSeek. I did not include any personal or institutional credentials.