import {chromium} from 'playwright';
import {preview} from 'vite';
import assert from 'node:assert/strict';
const server=await preview({preview:{host:'127.0.0.1',port:4185,strictPort:true}});
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
try{
 const page=await browser.newPage();
 await page.goto('http://127.0.0.1:4185');
 await page.getByRole('button',{name:'Begin scenario',exact:true}).click();
 await page.locator('input[type=file]').setInputFiles('artifacts/audit-roll-fixture.json');
 await page.getByRole('button',{name:'Roll all dice',exact:true}).click();
 await page.getByRole('button',{name:'New game',exact:true}).click();
 await page.getByRole('button',{name:'Begin scenario',exact:true}).click();
 await page.waitForTimeout(1200);
 const state=await page.evaluate(()=>JSON.parse(localStorage.getItem('moonfall-tactics-save-v15')));
 assert.equal(state.phase,'bid','An old dice animation must not replace a newly started game');
 assert.equal(state.history.length,0);
 console.log('Dice animation/new-game regression passed');
}finally{await browser.close();await server.httpServer.close();}
