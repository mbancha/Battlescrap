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
