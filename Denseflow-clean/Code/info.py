import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SPARTAN_DIR = REPO_ROOT / "spartan2-master"
if SPARTAN_DIR.exists() and str(SPARTAN_DIR) not in sys.path:
    sys.path.append(str(SPARTAN_DIR))

CASES = [
    'AlphaHomora',
    'CryptopiaHacker',
    'PlusTokenPonzi',
]

saddset = {}
saddset['AlphaHomora'] = ['0x905315602ed9a854e325f692ff82f58799beab57']
saddset['CryptopiaHacker'] = [
    '0xc8b759860149542a98a3eb57c14aadf59d6d89b9',
    '0xaa923cd02364bb8a4c3d6f894178d2e12231655c',
    '0x9007a0421145b06a0345d55a8c0f0327f62a2224',
]
saddset['PlusTokenPonzi'] = ['0x997114ca0830e9bee7443368fa27f4af2d4e55a6']
