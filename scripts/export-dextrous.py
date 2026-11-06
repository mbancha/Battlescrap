from pathlib import Path
import json,csv,re
root=Path('.')
s=json.loads((root/'print-and-play/source-snapshot.json').read_text(encoding='utf8'))
out=root/'assets/dextrous';out.mkdir(exist_ok=True)
for name,rows in s['sheets'].items():
 if not rows:continue
 headers=rows[0]
 with (out/(name.lower().replace(' ','-')+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
  writer=csv.writer(f);writer.writerow(['Nickname','Copies']+headers)
  for row in rows[1:]:
   d=dict(zip(headers,row))
   if name=='Heroes' and d.get('Availability')!='Starter':continue
   def fmt(v):
    v=re.sub(r'\{hex:(\d+)\}',r'$mt_distance[\1]',str(v))
    for token,asset in [('Ranged Attack','ranged'),('attack','melee'),('ranged attack','ranged'),('defense','defense')]:v=v.replace('['+token+']','{Moonfall/icons/'+asset+'.webp}')
    return v
   writer.writerow([d.get('ID',name+'-'+str(rows.index(row))),d.get('Copies',1)]+[fmt(x) for x in row])
(out/'variables.csv').write_text('Project variables,Project variables text\n$mt_distance,${1} hex\n',encoding='utf8')
(out/'README.md').write_text('Generated imports from the committed source snapshot. Numeric engine fields remain typed in JSON. Import family CSV files into Dextrous and install variables.csv; icon library paths require uploading assets/print/icons under Moonfall/icons. A real Dextrous template/style pilot and linked-sheet refresh remain unverified. Do not treat these exports as independently authored data.\n',encoding='utf8')
