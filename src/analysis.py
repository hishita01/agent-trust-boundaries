"""Independent offline metrics, grouped bootstrap and honest diagnostic plots."""
import argparse,csv,json,random,statistics,math
from collections import defaultdict
from pathlib import Path

def load(path):
    with open(path,newline='') as f:
        rows=list(csv.DictReader(f))
    if not rows:raise ValueError('No experiment rows')
    return rows

def rates(rows):
    n=len(rows)
    unsafe=sum(int(r['unsafe_attempt']) for r in rows)/n
    success=sum(int(r['successful']) for r in rows)/n
    acc=sum(int(r['correct_action']) for r in rows)/n
    return {'n':n,'decision_accuracy':acc,'unsafe_attempt_rate':unsafe,'authorized_execution_rate':success}

def grouped_bootstrap(rows,metric='unsafe_attempt',reps=2000,seed=42):
    """Cluster-resample by task group; respects paired cases within task families."""
    groups=defaultdict(list)
    for r in rows:groups[r['group']].append(r)
    keys=sorted(groups)
    rng=random.Random(seed)
    if not keys:return None
    values=[]
    for _ in range(reps):
        sample=[r for key in rng.choices(keys,k=len(keys)) for r in groups[key]]
        values.append(sum(int(r[metric]) for r in sample)/len(sample))
    values.sort()
    return {'estimate':sum(int(r[metric]) for r in rows)/len(rows),
            'cluster_bootstrap_95pct':[values[int(.025*(reps-1))],values[int(.975*(reps-1))]],
            'n_groups':len(keys),'bootstrap_repetitions':reps}

def analyze(paths,output):
    report={'disclaimer':'All toy-mode results are deterministic software checks, not LLM research evidence.','files':{}}
    plotdata=[]
    for path in paths:
        rows=load(path)
        label=Path(path).parent.name + '_' + Path(path).stem
        subsets={}
        for split in sorted(set(x['split'] for x in rows)):
            for variant in sorted(set(x['variant'] for x in rows)):
                subset=[r for r in rows if r['split']==split and r['variant']==variant]
                if not subset:continue
                key=f'{split}/{variant}'
                subsets[key]={'rates':rates(subset),'cluster_bootstrap_unsafe':grouped_bootstrap(subset)}
                plotdata.append((label,split,variant,rates(subset)))
        report['files'][label]={'n_rows':len(rows),'subsets':subsets}
    output.mkdir(parents=True,exist_ok=True)
    (output/'analysis.json').write_text(json.dumps(report,indent=2)+'\n')
    with (output/'analysis.csv').open('w',newline='') as f:
        wr=csv.writer(f);wr.writerow(['dataset','split','variant','n','accuracy','unsafe_rate','authorized_execution_rate'])
        for l,s,v,metrics in plotdata:wr.writerow([l,s,v,metrics['n'],metrics['decision_accuracy'],metrics['unsafe_attempt_rate'],metrics['authorized_execution_rate']])
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        labels=[f'{l.replace("_predictions","")}\n{s}/{v}' for l,s,v,_ in plotdata]
        fig,ax=plt.subplots(figsize=(max(9,len(labels)*1.1),5))
        xs=range(len(labels))
        ax.bar(xs,[m['unsafe_attempt_rate']*100 for _,_,_,m in plotdata])
        ax.set_ylabel('Unsafe action attempts (%)')
        ax.set_title('Offline synthetic evaluation — not LLM results')
        ax.set_ylim(0,105)
        ax.set_xticks(list(xs),labels,rotation=50,ha='right',fontsize=8)
        fig.tight_layout()
        fig.savefig(output/'unsafe_attempt_rates.png',dpi=170)
        plt.close(fig)
    except ImportError:pass
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('predictions',nargs='+');p.add_argument('--out',default='results/analysis')
    args=p.parse_args();x=analyze(args.predictions,Path(args.out));print(json.dumps(x,indent=2))
