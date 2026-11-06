import {mkdirSync,writeFileSync} from 'node:fs';
import {newGame,actions,dispatch,bot,playerView,owner} from '../src/engine';
const s=newGame(42,{equipment:false});
for(let i=0;s.phase!=='battle'&&i<200;i++){
 const error=dispatch(s,bot({...playerView(s,owner(s)),decisionOwner:owner(s)},actions(s)));
 if(error)throw Error(error);
}
s.config.controllers=['human','bot'];s.config.target=100;s.side=0;s.pending=null;s.response=null;s.effects=[];s.cleanup=0;
s.players.forEach(p=>{p.hand=[];p.pp=0;});
const a=s.units.find(u=>u.owner===0&&u.hero),d=s.units.find(u=>u.owner===1&&u.hero);
s.units.forEach(u=>u.hex=null);a.hex='5,4';d.hex='6,4';s.active=a.id;
s.combat={attacker:a.id,defender:d.id,basic:true,override:null,isCounter:false,stage:'roll',priority:0,passes:2,bonus:0,defBonus:0,extraDamage:0,counter:false,attackDice:[],defenseDice:[]};
mkdirSync('artifacts',{recursive:true});writeFileSync('artifacts/audit-roll-fixture.json',JSON.stringify(s));
