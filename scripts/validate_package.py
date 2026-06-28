#!/usr/bin/env python3
"""validate_package.py — Validate a packaged skill zip."""
import json, sys, hashlib, argparse, zipfile
from datetime import datetime, timezone
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_path")
    parser.add_argument("--json-out", default=None)
    args = parser.parse_args()
    zp = Path(args.zip_path)
    issues = []
    files = []
    if zp.exists():
        try:
            with zipfile.ZipFile(zp) as zf:
                bad = zf.testzip()
                if bad: issues.append(f"Corrupted: {bad}")
                files = zf.namelist()
        except zipfile.BadZipFile:
            issues.append("Invalid zip")
    else:
        issues.append(f"Not found: {zp}")
    sha = hashlib.sha256(zp.read_bytes()).hexdigest() if zp.exists() else ""
    out = {"tool":"validate_package","zip_path":str(zp),"sha256":sha,"file_count":len(files),"issues":issues,"overall_pass":len(issues)==0,"checks_run":["zip_integrity","sha256"],"generated_at_utc":datetime.now(timezone.utc).isoformat()}
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(out,indent=2))
    else:
        print(json.dumps(out,indent=2))
    return 0 if not issues else 1

if __name__ == "__main__":
    sys.exit(main())
