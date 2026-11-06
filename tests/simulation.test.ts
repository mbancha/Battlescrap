import {it,expect} from 'vitest';
import {newGame,draw,damage} from '../src/engine';
import {gameSummary,summarize,simulateGame,defaultSim} from '../src/simulation';
it('attributes actual draws and repeated defeat events',()=>{
 const s=newGame(1,{simulation:true});s.deck=['Fire-attack:shared:0'];draw(s,0,'moonstone');draw(s,0,'objective');
 expect(s.metrics['drawReceived:moonstone']).toBe(1);expect(s.metrics['drawRequested:objective']).toBe(1);expect(s.metrics['drawReceived:objective']).toBeUndefined();
 const r={owner:0,index:0,hex:'5,4',wounds:0,tokens:{}};s.units.push(r);damage(s,r,1);damage(s,r,1);expect(s.metrics.recruitDeaths).toBe(1);r.hex='5,4';r.wounds=0;damage(s,r,1);expect(s.metrics.recruitDeaths).toBe(2);
});
it('reports individual heroes and completed-game denominators',()=>{
 const games:any=[{complete:true,teams:[['h01','h03'],['h06']],winner:0,first:0,metrics:{turns:10,paidActions:4,tacticPlays:2,heroDeaths:1,recruitDeaths:3,'drawReceived:startingHand':4,'drawReceived:objective':2}},{complete:false,teams:[['h01'],['h06']],metrics:{turns:100}}];
 expect(summarize(games).map(r=>r.id).sort()).toEqual(['h01','h03','h06']);expect(summarize(games).find(r=>r.id==='h01')?.rate).toBe(1);
 expect(gameSummary(games)).toMatchObject({completed:1,unfinished:1,meanTurns:10,meanActions:6,meanHeroDeaths:1,meanRecruitDeaths:3,meanTacticsEarned:2});expect(gameSummary([]).meanTurns).toBe(null);
});
it('interpolates the median for even completed-game samples',()=>{const games:any=[10,20].map(turns=>({complete:true,teams:[[],[]],metrics:{turns}}));expect(gameSummary(games).turnsMedian).toBe(15);});
it('pairs each roster across opposite deployment zones',()=>{
 const options={...defaultSim,maxCommands:2};
 const first=simulateGame(options,0),second=simulateGame(options,1);
 expect(first.teams[0]).toEqual(second.teams[1]);
 expect(first.zones[0]).not.toBe(second.zones[1]);
 expect(first.seed).toBe(second.seed);
});
