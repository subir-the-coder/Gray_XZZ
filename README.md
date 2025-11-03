# xx0r — README

**ReconTool** is a modular Python CLI that orchestrates reconnaissance and URL-crawling tools to help security testers collect, filter and prepare web targets for further analysis (XSS, SQLi, parameter discovery, etc.). This repository contains an interactive script intended for Debian-based pentest distributions (Parrot OS, Kali, Ubuntu).

> **Important:** This project is **not** AUTOPEON. It is a separate ReconTool script focused on passive enumeration, crawling, URL deduplication, parameter extraction, and XSS/Arjun preparation.

---

## Contents

* `xx0r.py` — Main interactive script (the CLI you provided). It provides a multi-step workflow:

  1. Install required tools and dependencies
  2. Accept a target domain
  3. Perform passive subdomain enumeration (subfinder, amass, assetfinder)
  4. Crawl/filter collected domains (gospider, hakrawler, katana, waybackurls, gau)
  5. Extension & domain-specific filtering and deduplication (uro)
  6. Separate URLs for Arjun and SQLi testing
  7. Prepare query-containing URLs for XSS testing
  8. Run XSS checker (xss-checker/XSStrike) if available

* `LICENSE` — Apache License 2.0 (full text included below)

* `README.md` — This file

---

## Features

* Terminal banner and colored output for a better UX
* Automated installation of common recon tools (Go tools, Python packages, apt packages)
* Passive subdomain enumeration and merging of results
* Crawling with several popular crawlers and Wayback/Gau sources
* Noise filtering (static assets, document files, archives, binaries)
* URL normalization and deduplication via `uro`
* Separation of parameterized vs non-parameterized endpoints and preparation for Arjun
* Quick XSS target extraction for common parameter names
* Basic error handling and an `error.log` for failures

---

## Prerequisites

This script is designed for Debian-based systems and assumes you have:

* `sudo` privileges
* `python3` and `python3-venv`
* `go` (for installing Go tools) — the script will install Go tools to `$HOME/go/bin`
* Network connectivity to download/install tools

Recommended environment: Parrot OS, Kali Linux, or Ubuntu with development tools installed.

---

## Quick install & usage

1. Save the provided script as `xx0r.py` (or keep the file name you already have).
2. Make it executable:

```bash
chmod +x xx0r.py
```

3. Run the script:

```bash
./xx0r.py
```

4. Follow the on-screen menu:

   * Option 1: install tools (runs apt/go/pip installs)
   * Option 2: set the target domain
   * Option 3..8: run the enumerations, crawling, filtering and checks in order

**Important:** Some steps call external binaries (e.g. `katana`, `gospider`, `uro`, `arjun`, `xss-checker`). Ensure those binaries are present in your PATH or that Option 1 completed successfully.

---

## File outputs

The script writes intermediate and final outputs to the current working directory. Important filenames used by the workflow:

* `{domain}-domains.txt` — alive subdomains discovered for the target
* `{domain}-links-final.txt` — merged raw URL list from crawling tools
* `{domain}-links.txt` — cleaned, deduplicated links (after extensions filter & uro)
* `urls-ready.txt` — combined file suitable for running Arjun / further testing
* `{domain}-query.txt` — URLs that contain query strings and likely XSS targets
* `{domain}-ALL-links.txt` — full list of final links for reference
* `error.log` — logged failures for troubleshooting

---

## Recommendations & Safety

* Always have written permission before running this tool against systems you do not own.
* Use the tool for authorized security testing only.
* Run inside a virtual environment or disposable VM when installing many tools.
* Review the tool installation commands before running them — the script invokes `sudo apt install` and `go install` which will modify your system.

---

## Customization ideas

* Replace `subprocess.run([...])` calls with functions that check for presence of the program and print actionable errors.
* Add command-line flags to run specific steps non-interactively (for automation/CI).
* Add logging with log levels instead of simple prints.
* Save timestamped results into a `results/` folder to avoid overwriting previous runs.
* Add an option to load domains from a CSV/Excel file and process them in batch.

---

## Contributing

Contributions are welcome. Open an issue to propose features or file a PR — keep changes small and focused. Run `black`/`ruff`/`flake8` if you add Python code.

---

## License

This project is licensed under the Apache License 2.0. Full license text is included below.

---

# Apache License, Version 2.0

Copyright subirthecoder@gmail.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

```
http://www.apache.org/licenses/LICENSE-2.0
```

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

---


