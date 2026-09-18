"""Independent research verification; run with .codex-test/run python this_file [PDF].

Requires PyMuPDF and g++. The PDF must match the registered original digest.
Extracts appendix B.7 directly, compares all arrays, compiles its original loops,
and compares five source-domain cases. This does not validate transport physics.
"""
import ctypes
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys
import tempfile

import fitz

pdf = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/breeding-hcll-thesis.pdf")
digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
assert digest == "0fd38e685a68e751f8d21f0b3248cb4ac3b1d406d8b1d22ea8229b0689102abc"
with fitz.open(pdf) as document:
    pages = [document[index].get_text() for index in (134, 135, 136)]
# Exclude page headers, leaving printed code, including its own indexing loops.
code = (pages[0][pages[0].index("#define"):] +
        pages[1][pages[1].index("0.8116"):] +
        pages[2][pages[2].index("  }"):])
code = code[:code.rfind("}") + 1]
probe = runpy.run_path(str(Path(__file__).with_name("hcll_surrogate_probe.py")))
counts = {}
for suffix, key in (("minInput", "MININPUT"), ("maxInput", "MAXINPUT"),
                    ("minOuput", "MINOUPUT"), ("maxOuput", "MAXOUPUT"),
                    ("valW", "VALW")):
    body = re.search(r"FctTBR_Total_Rn_9_0_" + suffix +
                     r"\[\]\s*=\s*\{([^}]+)\}", code).group(1)
    values = [float(value.strip()) for value in body.split(",") if value.strip()]
    assert values == probe[key], key
    counts[key] = len(values)
code = '#include <cmath>\n' + code.replace(
    "void FctTBR_Total_Rn_9_0", 'extern "C" void FctTBR_Total_Rn_9_0')
points = [("reference", probe["REFERENCE"])]
for index, value in ((9, .7), (9, .8), (4, 35), (4, 55)):
    point = probe["REFERENCE"].copy()
    point[index] = value
    points.append((f"input_{index}={value}", point))
rows = []
with tempfile.TemporaryDirectory(prefix="hcll-review-") as directory:
    source = Path(directory) / "network.cpp"
    library = Path(directory) / "network.so"
    source.write_text(code)
    subprocess.run(["g++", "-shared", "-fPIC", str(source), "-o", str(library)],
                   check=True, capture_output=True, text=True)
    function = ctypes.CDLL(str(library)).FctTBR_Total_Rn_9_0
    function.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
    function.restype = None
    for name, point in points:
        output = ctypes.c_double()
        function((ctypes.c_double * 26)(*point), ctypes.byref(output))
        python_value = probe["evaluate"](point)
        delta = output.value - python_value
        assert abs(delta) < 1e-14
        rows.append(dict(case=name, original_cpp=output.value,
                         python=python_value, difference=delta))
print(json.dumps(dict(source_sha256=digest, array_exact_matches=counts, cases=rows,
    scope="Appendix example execution only; final-module statistics and stellarator applicability unvalidated."), indent=2))
