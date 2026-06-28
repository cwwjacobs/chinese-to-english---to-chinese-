#!/usr/bin/env python3
"""
overlay.py — Real-Time CLI Translation Overlay (HUD mode).

Requires: Python 3.10+, Tkinter, requests (for LM Studio/Ollama), deep-translator
Theme: Terminus Protocol — hot pink #ff6b9d / purple #9b59f0 / cyan #40d8e0 /
       gold #ffb347 / void #0a0a0f / chrome #e8e6e3
"""

import sys
import os
import json
import time
import uuid
import threading
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import tkinter as tk
from tkinter import ttk

# ── Theme ──────────────────────────────────────────────────────────────────

THEME = {
    "void": "#0a0a0f",
    "deep_purple": "#1a0f2e",
    "pink": "#ff6b9d",
    "purple": "#9b59f0",
    "cyan": "#40d8e0",
    "gold": "#ffb347",
    "chrome": "#e8e6e3",
    "surface": "#111118",
    "border": "#252535",
    "text_dim": "#5e5e74",
    "danger": "#e04048",
}

STATE_DIR = Path.home() / ".cli-overlay"
CONFIG_FILE = STATE_DIR / "config.json"
FIFO_PATH = "/tmp/trans_fifo"
OP_FIFO_PATH = "/tmp/op_trans_fifo"
DEFAULT_ALPHA = 0.85
MAX_MESSAGES = 200
ENTRY_FADE_ZONE = 50

# ── Config ─────────────────────────────────────────────────────────────────

def load_config():
    defaults = {
        "x": 100, "y": 100,
        "width": 700, "height": 500,
        "alpha": DEFAULT_ALPHA,
        "fifo_path": FIFO_PATH,
        "lm_studio_port": 1234,
    }
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text())
            defaults.update(data)
        except (json.JSONDecodeError, OSError):
            pass
    return defaults


def save_config(cfg):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = str(CONFIG_FILE) + ".tmp"
    Path(tmp).write_text(json.dumps(cfg, indent=2))
    os.replace(tmp, CONFIG_FILE)


# ── I7: Bidirectional Translation Client ────────────────────────────────────

class TranslationClient:
    """Tiered translation: LM Studio → Ollama → Google Translate."""

    TIER_LM_STUDIO = "lm_studio"
    TIER_OLLAMA = "ollama"
    TIER_GOOGLE = "google_translate"
    TIMEOUT = 15

    def __init__(self, lm_studio_port=1234):
        self.port = lm_studio_port
        self.current_tier = self.TIER_LM_STUDIO
        self._warm()

    def _post(self, url, payload):
        try:
            import requests
            return requests.post(url, json=payload, timeout=self.TIMEOUT)
        except ImportError:
            return None

    def _warm(self):
        """Pre-warm the translation pipeline."""
        self.translate("ping")

    def translate(self, text: str) -> tuple[str | None, str]:
        """Returns (translated_text, tier_used)."""
        if not text.strip():
            return "", self.current_tier

        prompt = (
            "You are a precise English-to-Chinese translator. "
            "Translate the following to natural, idiomatic Chinese. "
            "Output ONLY the Chinese translation. No explanation, no pinyin, no notes.\n\n"
            f"{text}"
        )

        # Tier 1: LM Studio
        try:
            resp = self._post(
                f"http://localhost:{self.port}/v1/chat/completions",
                {
                    "model": "local-model",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 2048,
                    "stream": False,
                },
            )
            if resp and resp.status_code == 200:
                result = resp.json()["choices"][0]["message"]["content"].strip()
                self.current_tier = self.TIER_LM_STUDIO
                return result, self.TIER_LM_STUDIO
        except Exception:
            pass

        # Tier 2: Ollama
        try:
            resp = self._post(
                "http://localhost:11434/api/generate",
                {
                    "model": "deepseek-r1:1.5b",
                    "prompt": prompt,
                    "stream": False,
                },
            )
            if resp and resp.status_code == 200:
                result = resp.json()["response"].strip()
                self.current_tier = self.TIER_OLLAMA
                return result, self.TIER_OLLAMA
        except Exception:
            pass

        # Tier 3: Google Translate
        try:
            from deep_translator import GoogleTranslator
            result = GoogleTranslator(source="en", target="zh-CN").translate(text)
            self.current_tier = self.TIER_GOOGLE
            return result, self.TIER_GOOGLE
        except Exception:
            pass

        return None, "none"

    def tier_label(self):
        return {
            self.TIER_LM_STUDIO: "🟢 LM Studio",
            self.TIER_OLLAMA: "🟡 Ollama 1.5B",
            self.TIER_GOOGLE: "🟠 Google Translate",
        }.get(self.current_tier, "🔴 Offline")


# ── I5: State Manager ──────────────────────────────────────────────────────

class StateManager:
    def __init__(self):
        self.session_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S-") + uuid.uuid4().hex[:6]
        self.state_file = STATE_DIR / f"state-{self.session_id}.json"
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        self._fh = open(self.state_file, "a", encoding="utf-8")
        self.msg_count = 0
        self._write_line({"event": "session_start", "session_id": self.session_id, "timestamp": datetime.now(timezone.utc).isoformat()})

    def _write_line(self, obj):
        self._fh.write(json.dumps(obj, ensure_ascii=False) + "\n")
        self._fh.flush()

    def save_message(self, msg: dict):
        self.msg_count += 1
        self._write_line(msg)

    def close(self):
        self._write_line({"event": "session_end", "message_count": self.msg_count, "timestamp": datetime.now(timezone.utc).isoformat()})
        self._fh.close()


# ── I2 + I3 + I7: Main Overlay ─────────────────────────────────────────────

class Overlay:
    def __init__(self):
        self.cfg = load_config()
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title("")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", self.cfg["alpha"])
        self.root.configure(bg=THEME["void"])
        self.root.geometry(f'{self.cfg["width"]}x{self.cfg["height"]}+{self.cfg["x"]}+{self.cfg["y"]}')
        self.root.minsize(400, 200)

        # ── Window Icon ──
        icon_paths = [
            Path(__file__).parent / "icons" / "cli-translation-overlay.png",
            Path(os.environ.get("ICON_PATH", "")),
            Path(os.path.expanduser("~/.local/share/icons/hicolor/256x256/apps/cli-translation-overlay.png")),
        ]
        for ip in icon_paths:
            if ip.exists():
                try:
                    icon_img = tk.PhotoImage(file=str(ip))
                    self.root.iconphoto(True, icon_img)
                    self._icon_ref = icon_img  # prevent GC
                    break
                except Exception:
                    pass

        self.state = StateManager()
        self.translator = TranslationClient(self.cfg.get("lm_studio_port", 1234))
        self.show_bounds = False
        self.toolbar_visible = False
        self.thinking_blocks = {}

        self._build_ui()
        self._start_fifo_reader()
        self.root.after(100, self._on_show)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_ui(self):
        # ── Main Text Area ──
        frame = tk.Frame(self.root, bg=THEME["void"])
        frame.pack(fill=tk.BOTH, expand=True)

        self.text = tk.Text(
            frame,
            bg=THEME["void"],
            fg=THEME["chrome"],
            insertbackground=THEME["gold"],
            font=("DejaVu Sans Mono", 11),
            wrap=tk.WORD,
            state=tk.DISABLED,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            padx=10,
            pady=8,
        )
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.pack(fill=tk.BOTH, expand=True)

        self.text.tag_configure("operator", foreground=THEME["pink"], font=("DejaVu Sans Mono", 11, "bold"))
        self.text.tag_configure("assistant", foreground=THEME["chrome"], lmargin1=20, lmargin2=20)
        self.text.tag_configure("thinking_toggle", foreground=THEME["cyan"], underline=True)
        self.text.tag_configure("thinking_body", foreground=THEME["text_dim"], lmargin1=30, lmargin2=30, font=("DejaVu Sans Mono", 10))
        self.text.tag_configure("tool_label", foreground=THEME["purple"], font=("DejaVu Sans Mono", 9))
        self.text.tag_configure("error", foreground=THEME["danger"])
        self.text.tag_configure("gold", foreground=THEME["gold"])

        # ── Toolbar (hidden) ──
        self.toolbar = tk.Frame(self.root, bg=THEME["deep_purple"], highlightbackground=THEME["pink"], highlightthickness=1, height=32)
        self.toolbar.pack_propagate(False)

        # Drag handle
        self.drag_lbl = tk.Label(self.toolbar, text="≡", fg=THEME["gold"], bg=THEME["deep_purple"], cursor="fleur", font=("DejaVu Sans Mono", 12))
        self.drag_lbl.pack(side=tk.LEFT, padx=(8, 4))
        self.drag_lbl.bind("<Button-1>", self._drag_start)
        self.drag_lbl.bind("<B1-Motion>", self._drag_move)

        # Opacity slider
        tk.Label(self.toolbar, text="Opacity", fg=THEME["chrome"], bg=THEME["deep_purple"], font=("DejaVu Sans Mono", 9)).pack(side=tk.LEFT, padx=(8, 2))
        self.opacity_var = tk.DoubleVar(value=self.cfg["alpha"])
        scale = tk.Scale(
            self.toolbar, from_=0.2, to=1.0, resolution=0.05, orient=tk.HORIZONTAL,
            variable=self.opacity_var, command=self._on_opacity,
            bg=THEME["deep_purple"], fg=THEME["chrome"], troughcolor=THEME["border"],
            highlightthickness=0, length=100, font=("DejaVu Sans Mono", 8),
        )
        scale.pack(side=tk.LEFT, padx=4)

        # Show Bounds
        self.bounds_btn = tk.Label(self.toolbar, text="☐ Bounds", fg=THEME["cyan"], bg=THEME["deep_purple"], cursor="hand2", font=("DejaVu Sans Mono", 9))
        self.bounds_btn.pack(side=tk.LEFT, padx=8)
        self.bounds_btn.bind("<Button-1>", lambda e: self._toggle_bounds())

        # Snap Align
        snap_btn = tk.Label(self.toolbar, text="↹ Snap", fg=THEME["purple"], bg=THEME["deep_purple"], cursor="hand2", font=("DejaVu Sans Mono", 9))
        snap_btn.pack(side=tk.LEFT, padx=4)
        snap_btn.bind("<Button-1>", lambda e: self._snap_align())

        # Tier indicator
        self.tier_lbl = tk.Label(self.toolbar, text="", fg=THEME["text_dim"], bg=THEME["deep_purple"], font=("DejaVu Sans Mono", 8))
        self.tier_lbl.pack(side=tk.LEFT, padx=12)
        self._update_tier_label()

        # Close
        close_btn = tk.Label(self.toolbar, text="×", fg=THEME["pink"], bg=THEME["deep_purple"], cursor="hand2", font=("DejaVu Sans Mono", 14, "bold"))
        close_btn.pack(side=tk.RIGHT, padx=8)
        close_btn.bind("<Button-1>", lambda e: self.on_close())

        # ── Bounds Canvas ──
        self.canvas = tk.Canvas(self.root, bg=THEME["void"], highlightthickness=0, bd=0)
        self.bounds_rect = None

        # ── I7: Bidirectional Entry ──
        self.entry_frame = tk.Frame(self.root, bg=THEME["void"])
        self.entry = tk.Entry(
            self.entry_frame,
            bg=THEME["surface"],
            fg=THEME["chrome"],
            insertbackground=THEME["gold"],
            highlightcolor=THEME["gold"],
            highlightbackground=THEME["border"],
            highlightthickness=1,
            font=("DejaVu Sans Mono", 11),
            relief=tk.FLAT,
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        self.entry.bind("<Return>", self._on_send_prompt)
        send_btn = tk.Label(self.entry_frame, text="→", fg=THEME["gold"], bg=THEME["void"], cursor="hand2", font=("DejaVu Sans Mono", 14, "bold"))
        send_btn.pack(side=tk.RIGHT)
        send_btn.bind("<Button-1>", lambda e: self._on_send_prompt(None))

        # Hover bindings
        self.root.bind("<Enter>", lambda e: self._show_toolbar())
        self.root.bind("<Motion>", self._on_motion)
        self.root.bind("<Leave>", lambda e: self._hide_toolbar_delayed())
        self._entry_fade_timer = None

    # ── Toolbar ──────────────────────────────────────────────────────────

    def _show_toolbar(self):
        if not self.toolbar_visible:
            self.toolbar.pack(side=tk.TOP, fill=tk.X, before=self.text.master)
            self.toolbar_visible = True

    def _hide_toolbar_delayed(self):
        self.root.after(800, self._hide_toolbar)

    def _hide_toolbar(self):
        ptr = self.root.winfo_pointerxy()
        wx = self.root.winfo_rootx()
        wy = self.root.winfo_rooty()
        ww = self.root.winfo_width()
        wh = self.root.winfo_height()
        if wx <= ptr[0] <= wx + ww and wy <= ptr[1] <= wy + wh:
            self.root.after(800, self._hide_toolbar)
            return
        if self.toolbar_visible:
            self.toolbar.pack_forget()
            self.toolbar_visible = False

    def _on_opacity(self, val):
        self.root.attributes("-alpha", float(val))
        self.cfg["alpha"] = float(val)

    def _toggle_bounds(self):
        self.show_bounds = not self.show_bounds
        self.bounds_btn.configure(text="☒ Bounds" if self.show_bounds else "☐ Bounds")
        if self.show_bounds:
            self._draw_bounds()
        else:
            self._hide_bounds()

    def _draw_bounds(self):
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        self.canvas.place(x=0, y=0, width=w, height=h)
        self.bounds_rect = self.canvas.create_rectangle(
            2, 2, w - 2, h - 2,
            outline=THEME["pink"], width=2, dash=(6, 4), fill="",
        )

    def _hide_bounds(self):
        if self.bounds_rect:
            self.canvas.delete(self.bounds_rect)
        self.canvas.place_forget()

    def _snap_align(self):
        try:
            wid = subprocess.check_output(
                ["xdotool", "search", "--name", "DeepSeek|deepseek|terminal|LM Studio"],
                text=True,
            ).strip().split("\n")[0]
            geo = subprocess.check_output(["xdotool", "getwindowgeometry", wid], text=True)
            import re
            m = re.search(r"Position: (\d+),(\d+).*Geometry: (\d+)x(\d+)", geo, re.DOTALL)
            if m:
                x, y, w, h = int(m[1]), int(m[2]), int(m[3]), int(m[4])
                self.root.geometry(f"{w}x{h}+{x}+{y}")
                self.cfg.update(x=x, y=y, width=w, height=h)
            if not self.show_bounds:
                self._toggle_bounds()
                self.root.after(2000, self._toggle_bounds)
        except Exception:
            self._append_message({
                "role": "assistant",
                "original": "[snap failed]",
                "translation": "Auto-snap failed. Drag the overlay manually or check that xdotool is installed.",
            })

    # ── Entry (I7) ───────────────────────────────────────────────────────

    def _on_motion(self, event):
        h = self.root.winfo_height()
        if h - event.y < ENTRY_FADE_ZONE:
            self._show_entry()
        else:
            self._hide_entry_delayed()

    def _show_entry(self):
        if not self.entry_frame.winfo_ismapped():
            self.entry_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=8, pady=(0, 6))
            self.entry.focus_set()
        if self._entry_fade_timer:
            self.root.after_cancel(self._entry_fade_timer)
            self._entry_fade_timer = None

    def _hide_entry_delayed(self):
        if self._entry_fade_timer:
            self.root.after_cancel(self._entry_fade_timer)
        self._entry_fade_timer = self.root.after(3000, self._hide_entry)

    def _hide_entry(self):
        if self.entry_frame.winfo_ismapped():
            self.entry_frame.pack_forget()

    def _on_send_prompt(self, event):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, tk.END)

        chinese, tier = self.translator.translate(text)
        if chinese is None:
            self._append_message({
                "role": "assistant",
                "original": "[translation failed]",
                "translation": "All translation tiers failed. Check LM Studio or Ollama.",
            })
            self._update_tier_label()
            return

        self._update_tier_label()

        operator_msg = {
            "session_id": self.state.session_id,
            "role": "operator",
            "original": text,
            "translation": chinese,
            "thinking": None,
            "translation_source": tier,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._append_message(operator_msg)
        self.state.save_message(operator_msg)

        try:
            Path(OP_FIFO_PATH).parent.mkdir(parents=True, exist_ok=True)
            if not os.path.exists(OP_FIFO_PATH):
                os.mkfifo(OP_FIFO_PATH)
            with open(OP_FIFO_PATH, "w") as f:
                f.write(chinese + "\n")
        except OSError:
            pass

    def _update_tier_label(self):
        self.tier_lbl.configure(text=self.translator.tier_label())

    # ── FIFO Reader ──────────────────────────────────────────────────────

    def _start_fifo_reader(self):
        t = threading.Thread(target=self._read_fifo, daemon=True)
        t.start()

    def _read_fifo(self):
        fifo_path = self.cfg.get("fifo_path", FIFO_PATH)
        Path(fifo_path).parent.mkdir(parents=True, exist_ok=True)
        if not os.path.exists(fifo_path):
            os.mkfifo(fifo_path)
        while True:
            try:
                with open(fifo_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            msg = json.loads(line)
                        except json.JSONDecodeError:
                            msg = {"role": "assistant", "original": line, "translation": line}
                        self.root.after(0, lambda m=msg: self._append_message(m))
                        self.state.save_message(msg)
            except (OSError, IOError):
                time.sleep(3)

    # ── Message Display ──────────────────────────────────────────────────

    def _append_message(self, msg: dict):
        self.text.configure(state=tk.NORMAL)

        role = msg.get("role", "assistant")
        original = msg.get("original", "")
        translation = msg.get("translation", original)
        thinking = msg.get("thinking")
        translation_source = msg.get("translation_source", "")

        if role == "operator":
            prefix = "▸ "
            tag = "operator"
        else:
            prefix = "▣ "
            tag = "assistant"

        self.text.insert(tk.END, f"{prefix}", tag)
        self.text.insert(tk.END, f"{translation}\n", tag)

        if original and original != translation:
            self.text.insert(tk.END, f"  ── {original[:120]}{'...' if len(original) > 120 else ''}\n", "thinking_body")

        if translation_source:
            self.text.insert(tk.END, f"  via {translation_source}\n", "tool_label")

        if thinking:
            block_id = f"think_{uuid.uuid4().hex[:8]}"
            self.thinking_blocks[block_id] = thinking
            self.text.insert(tk.END, "🧠 Show reasoning\n", ("thinking_toggle", block_id))
            self.text.tag_bind(block_id, "<Button-1>", lambda e, bid=block_id: self._toggle_thinking(bid))

        if msg.get("translation_error"):
            self.text.insert(tk.END, f"  ⚠ {translation}\n", "error")

        self.text.insert(tk.END, "\n")

        # Limit messages
        lines = int(self.text.index("end-1c").split(".")[0])
        if lines > MAX_MESSAGES * 4:
            self.text.delete("1.0", f"{lines - MAX_MESSAGES * 3}.0")

        self.text.configure(state=tk.DISABLED)
        self.text.see(tk.END)

    def _toggle_thinking(self, block_id):
        thinking_text = self.thinking_blocks.get(block_id)
        if not thinking_text:
            return
        self.text.configure(state=tk.NORMAL)
        self.text.insert(tk.END, f"  {thinking_text[:2000]}{'...' if len(thinking_text) > 2000 else ''}\n", "thinking_body")
        self.text.configure(state=tk.DISABLED)
        self.text.see(tk.END)
        del self.thinking_blocks[block_id]

    # ── Drag ─────────────────────────────────────────────────────────────

    def _drag_start(self, event):
        self._drag_x = event.x_root - self.root.winfo_x()
        self._drag_y = event.y_root - self.root.winfo_y()

    def _drag_move(self, event):
        x = event.x_root - self._drag_x
        y = event.y_root - self._drag_y
        self.root.geometry(f"+{x}+{y}")
        self.cfg["x"] = x
        self.cfg["y"] = y

    # ── Lifecycle ────────────────────────────────────────────────────────

    def _on_show(self):
        self.root.deiconify()

    def on_close(self):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        self.cfg.update(x=x, y=y, width=w, height=h)
        save_config(self.cfg)
        self.state.close()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def main():
    Overlay().run()


if __name__ == "__main__":
    main()
