from pathlib import Path
import fitz, hashlib
src=Path('/tmp/oktavian-tbr.txt'); data=src.read_bytes(); lines=data.decode().expandtabs(8).splitlines()
doc=fitz.open()
for start in range(0,len(lines),65):
 page=doc.new_page(width=1000,height=842)
 for j,line in enumerate(lines[start:start+65]):
  page.insert_text((20,35+j*12),line,fontsize=7,fontname='cour')
doc.set_metadata({'title':'Faithful text rendering of IAEA OKTAVIAN TBR readme; not original pagination','subject':'https://www-nds.iaea.org/fendl2/validation/benchmarks/jaerim94014/oktavian/tbr/readme.txt SHA256 '+hashlib.sha256(data).hexdigest()})
doc.save('/tmp/oktavian-tbr-rendered.pdf')
p=Path('work/orchestration/goals/computed-tritium-breeding/evidence/round2/oktavian-rendering-provenance.md')
p.write_text('# Text rendering provenance\n\nThe native extractor rejects text/plain. This PDF is a mechanical monospaced rendering of every original text line, 65 lines per page; it is not original publication pagination. It retains no missing figure. Original IAEA URL: https://www-nds.iaea.org/fendl2/validation/benchmarks/jaerim94014/oktavian/tbr/readme.txt. Original byte SHA256: `'+hashlib.sha256(data).hexdigest()+'`. Text and renderer are retained beside this note. No data correction, interpretation or omission was made.\n')
base=p.parent
(base/'oktavian-readme-original.txt').write_bytes(data)
(base/'render_oktavian_text.py').write_text(Path(__file__).read_text())
