from pathlib import Path
import re, hashlib
root=Path(__file__).parent
source=Path('F:/Enivornmental Audiiting/ANNEX/FBS_EIA_Survey_Analysis_Template.xlsx')
target=root/'dist/assets/FBS_EIA_Survey_Analysis_Template.xlsx'
target.write_bytes(source.read_bytes())
for name in ['dist/index.html','build_annex.py']:
 p=root/name
 text=p.read_text(encoding='utf-8')
 text=text.replace('The supplied workbook includes Summary, Responses and Codebook sheets, covering 49 questionnaire items.','The supplied workbook contains a Summary sheet with questionnaire items and response labels for the FBS building assessment.')
 text=re.sub(r'<div class="survey-stats">.*?</div></div><p class="note">.*?</p>', '<p class="note">This version contains no response-count or percentage tables. Download the workbook to view its supplied questionnaire content.</p>',text,flags=re.S)
 p.write_text(text,encoding='utf-8')
assert source.read_bytes()==target.read_bytes()
page=(root/'dist/index.html').read_text(encoding='utf-8')
assert 'Synthetic practice responses' not in page
assert 'Codebook sheets' not in page
print('Replacement verified byte-for-byte; outdated survey summary removed.')
