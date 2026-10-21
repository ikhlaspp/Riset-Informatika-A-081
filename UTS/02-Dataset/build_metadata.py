"""Audit split JSONL asli dan bangun metadata; tidak mengunduh atau membuat data."""
import argparse,csv,hashlib,json
from pathlib import Path
FIELDS=['response_id','source_id','source_hash','generator','source_origin','split','official_split','label','label_excluding_implicit_true','quality']
def load_splits(folder):
 result={};seen_responses=set();source_split={};hash_split={}
 for split in ('train','validation','test'):
  path=folder/(split+'.jsonl')
  if not path.is_file():raise ValueError(f'Berkas asli belum tersedia: {path}')
  rows=[]
  for line_no,line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(),1):
   if not line.strip():continue
   row=json.loads(line)
   missing=set(FIELDS+['source_text','response_text','original_labels'])-row.keys()
   if missing:raise ValueError(f'{path.name}:{line_no}: kolom tidak lengkap: {sorted(missing)}')
   rid=str(row['response_id']);sid=str(row['source_id'])
   if rid in seen_responses:raise ValueError(f'response_id duplikat: {rid}')
   seen_responses.add(rid)
   if row['split']!=split:raise ValueError(f'Split tidak cocok: {rid}')
   expected='test' if split=='test' else 'train'
   if row['official_split']!=expected:raise ValueError(f'official_split tidak cocok: {rid}')
   if row['quality']!='good':raise ValueError(f'quality bukan good: {rid}')
   if not isinstance(row['original_labels'],list):raise ValueError(f'original_labels bukan list: {rid}')
   for label in row['original_labels']:
    if not isinstance(label,dict) or not isinstance(label.get('implicit_true',False),bool):raise ValueError(f'Anotasi tidak valid: {rid}')
   if row['label']!=int(bool(row['original_labels'])):raise ValueError(f'Label utama tidak cocok: {rid}')
   alternate=int(any(not a.get('implicit_true',False) for a in row['original_labels']))
   if row['label_excluding_implicit_true']!=alternate:raise ValueError(f'Label alternatif tidak cocok: {rid}')
   if not isinstance(row['source_text'],str) or not row['source_text'].strip():raise ValueError(f'Teks sumber kosong: {rid}')
   if not isinstance(row['response_text'],str) or not row['response_text'].strip():raise ValueError(f'Teks respons kosong: {rid}')
   # Hash audit tersendiri; tidak mengganti source_hash asli maupun offset teks.
   normalized=' '.join(row['source_text'].split()).casefold()
   audit_hash=hashlib.sha256(normalized.encode()).hexdigest()
   for key,mapping in [(sid,source_split),(audit_hash,hash_split)]:
    if key in mapping and mapping[key]!=split:raise ValueError(f'Kebocoran sumber antarsplit: {rid}')
    mapping[key]=split
   rows.append(row)
  if not rows:raise ValueError(f'Split kosong: {path.name}')
  result[split]=rows
 return result

def write_csv(path,fields,rows):
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--data-dir',type=Path,default=Path(__file__).resolve().parent);a=p.parse_args()
 try:data=load_splits(a.data_dir)
 except (ValueError,OSError) as e:p.exit(2,f'Audit gagal: {e}\n')
 rows=[r for group in data.values() for r in group];sample=data['train'][:6]
 write_csv(a.data_dir/'dataset_metadata.csv',FIELDS,rows)
 write_csv(a.data_dir/'sampel_metadata.csv',FIELDS,sample)
 write_csv(a.data_dir/'label_halusinasi.csv',['response_id','label','label_excluding_implicit_true'],rows)
 (a.data_dir/'sampel').mkdir(exist_ok=True)
 (a.data_dir/'sampel/contoh_6_respons.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in sample),encoding='utf-8')
 audit={'status':'audit_struktur_dan_duplikasi_persis_selesai','catatan':'Kemiripan nonidentik dan panjang token belum diaudit. Hash audit: SHA256 teks casefold dengan whitespace digabung.','splits':{s:{'sources':len({str(r['source_id']) for r in rr}),'responses':len(rr),'positive':sum(r['label'] for r in rr),'negative':sum(1-r['label'] for r in rr),'sha256':hashlib.sha256((a.data_dir/(s+'.jsonl')).read_bytes()).hexdigest()} for s,rr in data.items()}}
 (a.data_dir/'audit_dataset.json').write_text(json.dumps(audit,indent=2),encoding='utf-8');print(json.dumps(audit,indent=2))
if __name__=='__main__':main()
