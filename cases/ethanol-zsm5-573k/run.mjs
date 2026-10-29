// Reproduce the upstream simplification and a Table-12 adsorption variant.
// No upstream fixture outputs are read. The requests are ordinary CHEPTA JSON.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';

const here = fileURLToPath(new URL('.', import.meta.url));
if (!process.argv[2]) throw new Error('Usage: node run.mjs /path/to/pinned/CHEPTA');
const engine = resolve(process.argv[2]);
const c = JSON.parse(readFileSync(join(here, 'input.json')));
if (c.T_K !== 573.15 || c.P_kPa !== 101.325 || c.feed_mol_h !== 1 || c.W_over_F_gcat_h_mol.some(w => w < 0.38 || w > 1.166)) {
  throw new Error('This benchmark is scoped to the audited fixed conditions and W/F interval; review new conditions before extending it.');
}
let observedCommit = null;
try { observedCommit = execFileSync('git', ['-C', engine, 'rev-parse', 'HEAD'], {encoding:'utf8', stdio:['ignore','pipe','ignore']}).trim(); } catch {}
if (observedCommit && observedCommit !== c.engine_commit) throw new Error('Wrong CHEPTA revision');
const { run } = await import(pathToFileURL(join(engine, 'src/index.js')));
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const hashes = Object.fromEntries(['package.json','src/index.js','src/units/kinetic-reactors.js','src/reactions/kinetics.js','src/util/ode.js'].map(p => [p, sha(readFileSync(join(engine,p)))]));
const p = id => `(p['${id}'] / 101.325)`;
const a=p('ethanol'), o=p('ethylene'), w=p('water'), e=p('diethyl-ether');
const output = join(here, 'results'); mkdirSync(output, {recursive:true});
const write = (name, value) => writeFileSync(join(output,name), JSON.stringify(value,null,2)+'\n');
const runs=[];
for (const variant of ['upstream_simplified','table12_adsorption']) {
  for (const wf of c.W_over_F_gcat_h_mol) {
    const k={...c.constants, k1:c.constants.k1/3.6, k2:c.constants.k2/3.6};
    const extra1=variant==='table12_adsorption' ? ` + ${e}*KE1 + ${w}*KW1` : '';
    const extra2=variant==='table12_adsorption' ? ` + ${e}*KE2 + ${w}*KW2 + ${o}*KO2` : '';
    // There is no inert in this feed: P_I*K_I is exactly zero, not a fitted omission.
    const formulas=[`k1*(${a}-${o}*${w}/Keq1)/(1+${a}*KA1${extra1})`,
      `k2*KA2^2*(${a}^2-${w}*${e}/Keq2)/(1+${a}*KA2${extra2})^2`];
    const W_kg=wf*c.feed_mol_h/1000;
    const L_m=W_kg/(c.bed_kg_m3*Math.PI*c.D_m**2/4);
    const reactions=c.stoichiometry.map((stoichiometry,i)=>({id:`E${i+1}`,stoichiometry,phase:'vapour',
      rate:{form:'expression',rate:formulas[i],constants:k,per:'catalyst-mass',basis:'partial-pressure'}}));
    const flowsheet={components:c.components,thermo:{model:'PR'},reactions,
      blocks:[{id:'F',type:'feed',spec:{flow_kmol_h:[c.feed_mol_h/1000,0,0,0],T_K:c.T_K,P_kPa:c.P_kPa}},
        {id:'R',type:'pfr',spec:{reactions:['E1','E2'],L_m,D_m:c.D_m,bed_kg_m3:c.bed_kg_m3,T_K:c.T_K}},
        {id:'P',type:'product',spec:{}}],
      streams:[{id:'feed',from:'F.out',to:'R.in'},{id:'product',from:'R.out',to:'P.in'}]};
    const request={capability:'solve_flowsheet',input:{flowsheet}};
    const id=`${variant}-wf${wf}`;
    write(`${id}.request.json`,request);
    const result=run(request);
    write(`${id}.output.json`,result); // Preserve failures as well as successes.
    runs.push({id,variant,W_over_F_gcat_h_mol:wf,W_kg,L_m,outcome:result.outcome,
      request_file:`results/${id}.request.json`,output_file:`results/${id}.output.json`,request_sha256:sha(JSON.stringify(request))});
  }
}
write('run-manifest.json',{executed_at:new Date().toISOString(),node:process.version,
  engine_commit_requested:c.engine_commit,engine_commit_observed:observedCommit,
  revision_note:observedCommit?'Git HEAD checked; hashes below identify key loaded files.':'Archive checkout: commit not discoverable locally; verify acquisition provenance separately. Key file hashes recorded.',
  engine_file_sha256:hashes,input_sha256:sha(readFileSync(join(here,'input.json'))),runs});
console.log(JSON.stringify(runs.map(({id,outcome})=>({id,outcome})),null,2));
if (runs.some(r=>r.outcome!=='ok')) process.exitCode=1;
