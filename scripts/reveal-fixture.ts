import {writeFileSync,mkdirSync} from 'node:fs';
import {newGame,actions,dispatch,bot,playerView,owner} from '../src/engine';
const s=newGame(42,{equipment:false});
for(let i=0;s.phase!=='battle'&&i<200;i++)dispatch(s,bot({...playerView(s,owner(s)),decisionOwner:owner(s)},actions(s)));
s.side=1;s.active=s.units.find(u=>u.owner===1&&u.hero).id;s.ap=0;s.rap=0;s.used={};s.config.target=100;s.units.find(u=>u.id===s.active).suit='Water';s.players[1].hand=['Fire-moveHeal:shared:0'];
mkdirSync('artifacts',{recursive:true});writeFileSync('artifacts/reveal-fixture.json',JSON.stringify(s));
