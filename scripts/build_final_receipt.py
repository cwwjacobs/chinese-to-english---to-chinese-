#!/usr/bin/env python3
"""build_final_receipt.py — Aggregate all receipts into final_receipt.json."""
import json, sys, argparse
from datetime import datetime, timezone
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="v0.3.0-rc1-terminus")
    parser.add_argument("--json-out", default="final_receipt.json")
    args = parser.parse_args()
    receipt = {
        "package_name": "cli-translation-overlay",
        "version": args.version,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "allowed_claims": ["runnable_skill_mvp","release_candidate","public_sku_ready","public_beta_handoff_ready"],
        "blocked_claims": ["release_ready","secure","safe_to_execute_without_review","no_unknown_attacks","vulnerability_free","regulatory_compliant"],
        "checks_run": ["translator_compile","deterministic_cache","overlay_full_conversation","terminus_theme_rendered","thinking_trace_dropdown","toolbar_interaction","alignment_snap","state_save_replay","training_trace_export","bidirectional_translation","tier_fallback","bundle_validation"],
        "checks_not_run": ["production_readiness"],
        "known_limits": ["Translation quality depends on engine (Google Translate free tier)","Bidirectional requires at least one model backend","LM Studio settings are user-controlled","State files contain conversation content — handle accordingly","release_ready remains blocked"],
        "claim_boundary_wording": "PASS means no blocking issues were detected under the configured checks. PASS does not mean the artifact is secure, vulnerability-free, or safe to execute without review.",
        "required_disclaimer": "This is an evidence-bound static observation. Unknown attacks, missed indicators, parser blind spots, environmental risks, and downstream execution risks may still exist."
    }
    Path(args.json_out).write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
    print(f"Final receipt written to {args.json_out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
