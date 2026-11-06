"""Remake current character faces from the native print template."""
import runpy
from pathlib import Path
module=runpy.run_path(str(Path(__file__).resolve().parents[1]/"print-and-play/build_current.py"))
module["remake_characters"]()
import json, hashlib
from reportlab.pdfgen import canvas
import pypdfium2 as pdfium
root=Path(__file__).resolve().parents[1]
out=root/'public/cards'
manifest={}
def face(identifier, data, renderer, width=180, height=252):
    import io
    buffer=io.BytesIO()
    c=canvas.Canvas(buffer,pagesize=(width,height))
    renderer(c,data,width,height);c.save()
    doc=pdfium.PdfDocument(buffer.getvalue())
    doc[0].render(scale=3).to_pil().save(out/(identifier+'.png'))
    manifest[identifier]={'face':'./cards/'+identifier+'.png','width':width,'height':height,'label':data.get('Name',data.get('id',identifier)),'text':data.get('Card text',''),'sha256':hashlib.sha256((out/(identifier+'.png')).read_bytes()).hexdigest()}
for row in module['rows']('Tactics'):face(row['ID'],row,module['tactic'])
for row in module['rows']('Equipment'):face('equipment-'+row['ID'],row,module['equipment'],180,144)
for side in ['Concord','Wildmoon']:face('recruit-'+side.lower(),{'id':side},module['recruit'])
for key,name,cost,stat in [('boots','Boots',2,'Move'),('shield','Shields',3,'Defense'),('weapon','Weapons',3,'Attack')]:
    face('recruit-'+key,{'ID':'recruit-'+key,'Name':'Recruit '+name,'Copies / cost':str(cost)+' PP','Card text':'All friendly Recruits gain +1 '+stat+'.'},module['equipment'],180,144)
for row in module['HEROES']:
    identifier=row['ID'];manifest[identifier]={'face':'./cards/'+identifier+'.png','width':180,'height':252,'label':row['Name'],'text':row['Ability effect'],'sha256':hashlib.sha256((out/(identifier+'.png')).read_bytes()).hexdigest()}
for i,row in enumerate(module['rows']('Objectives')):face('objective-'+str(i),dict(row,index=i),module['objective'])
for identifier,card in manifest.items():
    from PIL import Image
    card['pixelWidth'],card['pixelHeight']=Image.open(out/(identifier+'.png')).size
(out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print('Generated',len(manifest),'complete card faces')

# Release provenance is recomputed from current inputs, independently of image hashes.
inputs=['src/data/hero-snapshot.json','print-and-play/source-snapshot.json','print-and-play/build_current.py','scripts/build-card-faces.py']
inputs += [str(p.relative_to(root)).replace('\\','/') for p in sorted((root/'assets/print/icons').glob('*'))]
provenance={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in inputs}
(out/'sources.json').write_text(json.dumps(provenance,indent=2),encoding='utf8')
