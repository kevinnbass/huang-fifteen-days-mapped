"""Render the map figure (figures/nv8-fifteen-days-mapped.html, .png, .jpg) from the tables in research/ and the rows in scripts/.
Run: python3 scripts/build_nv8.py
Needs Python 3.10 or later, playwright with its chromium browser (pip install playwright; playwright install chromium),
pillow, and the Liberation Sans fonts (the script measures text with them)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fig_map, nv8_status

if __name__ == '__main__':
    fig_map.fig_web(nv8_status.KICKER, nv8_status.STATUS)
