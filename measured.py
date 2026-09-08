"""Rebuild the MEASURED rows in index.html from a MASTER_SPEC.json.

    python measured.py [path/to/MASTER_SPEC.json]

Reads the club-master column (the one whose key contains "CLUB") for the
loudness, peak, spectrum and tempo figures, and the stems block for the sub,
kick, mode and sidechain figures. Values are printed to two decimals except
where the sleeve shows more.
"""
import json
import re
import sys

SPEC = sys.argv[1] if len(sys.argv) > 1 else "../MASTER_SPEC.json"
PAGE = "index.html"

j = json.load(open(SPEC, encoding="utf-8"))
club = next(v for k, v in j["also"].items() if "CLUB" in k)
stems = j["master"]["stems"]

L, lv, S, t = club["loudness"], club["level"], club["spectrum"]["energy_share"], club["tempo"]
f = club["file"]
sub = stems["sub_stem"]["fundamental"]
kick = stems["kick_stem"]
mode = stems["mode"]["bassline (main bass + reese)"]
side = stems["sidechain"]["master"]
sublayer = stems["sub_layer"]


def n(x, d=2):
    s = f"{x:.{d}f}"
    return s.replace("-", "−")  # true minus sign


rows = [
    ("Integrated loudness", f"{n(L['integrated_lufs'])} LUFS"),
    ("True peak", f"{n(lv['true_peak_dbtp'])} dBTP"),
    ("Loudness range", f"{n(L['loudness_range_lu'])} LU"),
    ("Crest factor", f"{n(lv['crest_factor_db'])} dB"),
    ("Energy below 150 Hz", f"{n(S['below_150hz_pct'])} %"),
    ("Energy below 60 Hz", f"{n(S['below_60hz_pct'])} %"),
    ("Sub layer below 90 Hz", f"{n(sublayer['share_below_pct'], 3)} %"),
    ("Master energy below 90 Hz", f"{n(sublayer['master_share_below_90hz_pct'])} %"),
    ("Sub fundamental", f"{n(sub['hz'])} Hz · {sub['note']}"),
    ("Kick fundamental", f"{n(kick['fundamental_hz'])} Hz · {kick['fundamental_note']}"),
    ("Mode", f"D natural minor · {n(mode['in_D_natural_minor_pct'])} %"),
    ("Sidechain depth", f"{n(side['median_db'])} dB median"),
    ("Tempo", f"{n(t['bpm_beat_lag'])} BPM · nominal {int(t['nominal_bpm'])}"),
    ("Clipped samples", str(club["clipping"]["samples_at_full_scale"])),
    ("Format", f"{f['sample_rate'] // 1000} kHz · {f['bit_depth']}-bit · stereo"),
]

html = '  <dl class="measured label">\n' + "".join(
    f"    <div><dt>{k}</dt><dd>{v}</dd></div>\n" for k, v in rows
) + "  </dl>"

page = open(PAGE, encoding="utf-8").read()
page, count = re.subn(r'  <dl class="measured label">.*?</dl>', html, page, flags=re.S)
assert count == 1, "measured block not found"
open(PAGE, "w", encoding="utf-8", newline="\n").write(page)
for k, v in rows:
    print(f"{k:28} {v}")
