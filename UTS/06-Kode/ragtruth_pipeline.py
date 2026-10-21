"""Evaluasi prediksi biner per respons; bukan implementasi pelatihan B1/B2."""
import argparse,csv,json,math
from pathlib import Path

def metrics(labels,scores,threshold):
 if not labels or len(labels)!=len(scores):raise ValueError('Label dan skor harus sama panjang dan tidak kosong.')
 if any(y not in (0,1) for y in labels):raise ValueError('Label harus 0 atau 1.')
 if any(not math.isfinite(s) or not 0<=s<=1 for s in scores):raise ValueError('Probabilitas harus finite dalam [0,1].')
 pred=[int(s>=threshold) for s in scores]
 tp=sum(y==1 and p==1 for y,p in zip(labels,pred));tn=sum(y==0 and p==0 for y,p in zip(labels,pred))
 fp=sum(y==0 and p==1 for y,p in zip(labels,pred));fn=sum(y==1 and p==0 for y,p in zip(labels,pred))
 div=lambda a,b:a/b if b else None
 f1p=div(2*tp,2*tp+fp+fn);f1n=div(2*tn,2*tn+fp+fn)
 # AP dihitung pada kelompok skor setara, bukan urutan arbitrer baris.
 ap=None;positive=sum(labels)
 if positive:
  groups={}
  for y,s in zip(labels,scores):groups.setdefault(s,[]).append(y)
  found=0;count=0;ap=0.0
  for s in sorted(groups,reverse=True):
   new=sum(groups[s]);found+=new;count+=len(groups[s]);ap+=(new/positive)*(found/count)
 return {'threshold':threshold,'n':len(labels),'positive':positive,'negative':len(labels)-positive,'tp':tp,'tn':tn,'fp':fp,'fn':fn,'macro_f1':(f1p+f1n)/2 if f1p is not None and f1n is not None else None,'f1_positive':f1p,'f1_negative':f1n,'precision':div(tp,tp+fp),'recall':div(tp,tp+fn),'average_precision':ap,'accuracy':(tp+tn)/len(labels),'undefined_policy':'null berarti NA: penyebut nol atau tidak ada kelas positif untuk AP.'}

def read_predictions(path):
 with path.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
 if not rows:raise ValueError('CSV tidak memiliki prediksi; template kosong tidak dapat dievaluasi.')
 required={'response_id','source_id','strategy','seed','label','probability'}
 if not required.issubset(rows[0]):raise ValueError(f'Kolom wajib: {sorted(required)}')
 groups={};seen=set()
 for r in rows:
  key=(r['strategy'],r['seed']);unique=key+(r['response_id'],)
  if unique in seen:raise ValueError(f'Prediksi respons duplikat: {unique}')
  seen.add(unique);groups.setdefault(key,[]).append(r)
 return groups

def choose_threshold(rows):
 labels=[int(r['label']) for r in rows];scores=[float(r['probability']) for r in rows]
 candidates=[]
 for i in range(5,96):
  t=i/100;score=metrics(labels,scores,t)['macro_f1']
  if score is not None:candidates.append((score,-abs(i-50),-i,t))
 if not candidates:raise ValueError('Macro-F1 validasi tidak terdefinisi.')
 return max(candidates)[-1]

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('predictions',type=Path);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--threshold',type=float);g.add_argument('--validation',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 try:
  if a.threshold is not None and not 0<=a.threshold<=1:raise ValueError('Ambang harus dalam [0,1].')
  test=read_predictions(a.predictions);validation=read_predictions(a.validation) if a.validation else None
  if a.validation and a.validation.resolve()==a.predictions.resolve():raise ValueError('Validasi dan uji harus berbeda.')
  results=[]
  for key,rows in test.items():
   if validation is not None:
    if key not in validation:raise ValueError(f'Run validasi tidak ditemukan: {key}')
    if {r['source_id'] for r in rows}&{r['source_id'] for r in validation[key]}:raise ValueError('source_id validasi dan uji beririsan.')
    threshold=choose_threshold(validation[key])
   else:threshold=a.threshold
   results.append(dict(strategy=key[0],seed=key[1],**metrics([int(r['label']) for r in rows],[float(r['probability']) for r in rows],threshold)))
  a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(results,indent=2,allow_nan=False),encoding='utf-8');print(f'Metrik tersimpan: {a.output}')
 except (ValueError,OSError,KeyError) as e:p.exit(2,f'Evaluasi gagal: {e}\n')
if __name__=='__main__':main()
