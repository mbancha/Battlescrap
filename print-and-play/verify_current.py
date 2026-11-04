"""Validate the current mixed-orientation kit, quantities and print geometry."""
from pathlib import Path
import json, hashlib
from collections import Counter
import pdfplumber
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'current'
m=json.loads((OUT/'manifest.json').read_text())
checks=[]
def check(name,ok):
    assert ok,name
    checks.append(name)
def text(file):return '\n'.join(p.extract_text() or '' for p in PdfReader(OUT/file).pages)
check('19-page current kit',len(PdfReader(OUT/'Moonfall-Tactics-print-and-play.pdf').pages)==m['pages']==19)
check('Verified source hash',hashlib.sha256((ROOT/'source-snapshot.json').read_bytes()).hexdigest()==m['source_sha256'])
check('Two starting tactics; one objective tactic',m['starting_tactics']==2 and m['objective_tactics']==1)
with pdfplumber.open(OUT/'06-action-queue.pdf') as d:
    p=d.pages[0]
    check('One landscape Letter track sheet',len(d.pages)==1 and p.width==792 and p.height==612)
    strips=[r for r in p.rects if abs(r['width']-720)<.01 and abs(r['height']-72)<.01]
    check('Both tracks exactly ten by one inches',len(strips)==2)
    for y,n in [(408,3),(246,4)]:
        values=m['queue_ap_rap'][str(n)]
        sw=720/len(values)
        for i,(ap,rap) in enumerate(values):
            x=36+i*sw
            s=p.crop((x,612-y-72,x+sw,612-y)).extract_text()
            check(f'{n}-hero slot {i}: {ap} AP / {rap} RAP',f'{ap} AP' in s and f'{rap} RAP' in s)
    check('Six and eight sections',len(m['queue_ap_rap']['3'])==6 and len(m['queue_ap_rap']['4'])==8)
    check('Intentional top RAP drop retained',all(v[-2][1]==3 and v[-1]==[5,2] for v in m['queue_ap_rap'].values()))
placements=m['placements']
tc=Counter(p['id'] for p in placements if p['file']=='03-tactics.pdf')
check('36 tactics / 9 per element',sum(tc.values())==36 and all(sum(v for k,v in tc.items() if k.startswith(e+'-'))==9 for e in ['Fire','Water','Earth','Wind']))
check('Two Attack and damage; other effects single',all(v==(2 if k.split('-')[1] in ['attack','damage'] else 1) for k,v in tc.items()))
check('All four Cancel faces use combat-only rule',text('03-tactics.pdf').count('During combat')==4 and 'activate a hero' not in text('03-tactics.pdf'))
check('Six objective reward labels',text('07-objectives.pdf').count('1 VP + 1 tactic')==6)
check('Ten stable starter identities, Bisti not Kalawi',len(m['heroes'])==10 and 'h01' in m['heroes'] and 'h15' not in m['heroes'])
check('Queue portraits fit smallest slot',all(p['width']==90 and p['height']==126 for p in placements if p['file']=='02-portrait-cards.pdf'))
check('Eight faction/element badges',sum(p['file']=='05-ownership-holders.pdf' for p in placements)==8)
check('14 equipment / upgrade reminders on one sheet',sum(p['file']=='09-equipment.pdf' for p in placements)==14 and len(PdfReader(OUT/'09-equipment.pdf').pages)==1)
tok=text('04-tokens.pdf')
check('Ten of all five statuses',all(tok.count(s)==10 for s in ['Focus','Enraged','Fortified','Dazed','Poison']))
check('Four traps, seventeen stones and eight ability markers',tok.count('Trap')==4 and tok.count('Moonstone')==17 and tok.count('Ability')==8)
rules=text('00-rules-and-legend.pdf')
check('Current rules economics and hero-only pickup','draw 2 tactics' in rules and '1 VP + 3 tactics' not in rules and '1 Focus' in rules and 'never Recruits' in rules)
check('Two map halves',len(PdfReader(OUT/'10-map.pdf').pages)==2)
for p in placements:
    check(f"In bounds: {p['file']} / {p['id']} / page {p['page']}",0<=p['x'] and 0<=p['y'] and p['x']+p['width']<=612 and p['y']+p['height']<=792)
with pdfplumber.open(OUT/'Moonfall-Tactics-print-and-play.pdf') as doc:
    for i,p in enumerate(doc.pages):
        check(f'Page {i+1} is US Letter',sorted([p.width,p.height])==[612,792])
        check(f'Page {i+1} vector text in bounds',all(-.1<=w['x0']<=w['x1']<=p.width+.1 and -.1<=w['top']<=w['bottom']<=p.height+.1 for w in p.extract_words()))
check('GitHub-compatible combined PDF size',(OUT/'Moonfall-Tactics-print-and-play.pdf').stat().st_size<50_000_000)
(OUT/'verification.json').write_text(json.dumps({'checks_passed':len(checks),'checks':checks,'scope':'PDF geometry, quantities and text; raster card faces visually reviewed. Not runtime or balance certification.'},indent=2))
print(len(checks),'checks passed')
