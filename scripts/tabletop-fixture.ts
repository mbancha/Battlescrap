import {readFileSync,writeFileSync} from 'node:fs';
import {actions} from '../src/engine';
const s=JSON.parse(readFileSync('artifacts/audit-roll-fixture.json','utf8'));s.combat=null;s.ap=9;s.rap=9;s.config.controllers=['human','human'];s.players.forEach((p:any)=>p.hand=[]);const move=actions(s).find((a:any)=>a.type==='move'&&a.unit===s.active);if(!move)throw Error('No fixture move');writeFileSync('artifacts/tabletop-move.json',JSON.stringify(s));writeFileSync('artifacts/tabletop-move-action.json',JSON.stringify(move));
