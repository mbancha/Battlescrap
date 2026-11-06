import {existsSync,readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const manifest=JSON.parse(readFileSync('public/cards/manifest.json','utf8'));
for(const [id,card] of Object.entries(manifest)){
 const path='public/'+card.face.replace('./','');
 if(!existsSync(path))throw Error('Missing card face: '+id);
 if(createHash('sha256').update(readFileSync(path)).digest('hex')!==card.sha256)throw Error('Card face changed: '+id);
}
for(const name of ['fire','water','earth','wind'])if(!existsSync('assets/print/icons/'+name+'.png'))throw Error('Missing element '+name);
if(!existsSync('public/scenario-1.png'))throw Error('Missing scenario map');
console.log('Verified '+Object.keys(manifest).length+' complete card faces, current element masters and map.');

const provenance=JSON.parse(readFileSync('public/cards/sources.json','utf8'));
for(const [path,digest] of Object.entries(provenance))if(createHash('sha256').update(readFileSync(path)).digest('hex')!==digest)throw Error('Stale card source: '+path);
const runtime=JSON.parse(readFileSync('src/data/hero-snapshot.json','utf8')).sheets.find(s=>s.name==='Heroes').rows;
const print=JSON.parse(readFileSync('print-and-play/source-snapshot.json','utf8')).sheets.Heroes;
if(JSON.stringify(runtime)!==JSON.stringify(print))throw Error('Runtime/print hero source drift');
const headers=runtime[0],expected=runtime.slice(1).filter(r=>r[headers.indexOf('Availability')]==='Starter').map(r=>r[0]);
for(const id of expected)if(!manifest[id])throw Error('Missing sourced hero '+id);
for(const [id,card] of Object.entries(manifest)){const bytes=readFileSync('public/'+card.face.replace('./',''));if(bytes.readUInt32BE(16)!==card.pixelWidth||bytes.readUInt32BE(20)!==card.pixelHeight)throw Error('Wrong raster size '+id);}
