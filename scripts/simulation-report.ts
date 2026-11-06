import {mkdirSync,writeFileSync} from 'node:fs';
import {defaultSim,simulateGame,summarize,gameSummary} from '../src/simulation';
const options={...defaultSim,games:Number(process.argv[2]||50),heroCount:Number(process.argv[3]||3)},results=[];
for(let i=0;i<options.games;i++)results.push(simulateGame(options,i));
const report={options,results,summary:summarize(results),totals:gameSummary(results)};
mkdirSync('artifacts',{recursive:true});writeFileSync('artifacts/simulation-report.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report.totals,null,2));
