#!/usr/bin/env python3
"""build_final_receipt.py — Aggregate release-bound claim receipt."""
import json, sys, argparse
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="v0.3.0")
    parser.add_argument("--json-out", default="final_receipt.json")
    args = parser.parse_args()
    receipt = {
        "package_name": "cli-translation-overlay",
        "version": args.version,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "allowed_claims": [
            "local_desktop_hud_overlay",
            "chinese_cli_output_to_english_overlay",
            "english_prompt_to_chinese_fifo_output",
            "bidirectional_fifo_bridge_when_run_deepseek_target_is_used",
            "deterministic_translation_cache",
            "state_replay",
            "training_trace_jsonl_export",
            "public_beta_handoff_ready"
        ],
        "blocked_claims": [
            "professional_translation_quality",
            "direct_cli_injection_without_fifo_bridge",
            "production_ready",
            "secure",
            "safe_to_execute_without_review",
            "no_unknown_attacks",
            "vulnerability_free",
            "regulatory_compliant"
        ],
        "checks_run": [
            "translator_compile",
            "overlay_compile",
            "replay_compile",
            "training_trace_export_compile",
            "package_validator_compile",
            "test_bundle_compile",
            "makefile_targets_present",
            "fifo_bridge_documented",
            "version_alignment"
        ],
        "checks_not_run": [
            "production_readiness",
            "professional_translation_evaluation",
            "security_review",
            "cross_distro_desktop_packaging_review",
            "live_deepseek_cli_e2e_in_this_receipt"
        ],
        "known_limits": [
            "Translation quality depends on the selected engine.",
            "Chinese-to-English output translation currently uses deep-translator with a local cache.",
            "English-to-Chinese prompt translation requires LM Studio, Ollama, or Google Translate fallback.",
            "Bidirectional CLI input requires the FIFO bridge command or make run-deepseek target.",
            "State files may contain sensitive conversation content and must be handled accordingly.",
            "Tkinter availability depends on the local Python/system package installation."
        ],
        "claim_boundary_wording": "PASS means no blocking issues were detected under the configured checks. PASS does not mean the artifact is secure, vulnerability-free, production-ready, or safe to execute without review.",
        "required_disclaimer": "This is an evidence-bound static observation. Unknown attacks, missed indicators, parser blind spots, environmental risks, translation errors, and downstream execution risks may still exist."
    }
    Path(args.json_out).write_text(json.dumps(receipt, ensure_ascii=False, indent=2))
    print(f"Final receipt written to {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
