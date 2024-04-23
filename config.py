from pathlib import Path
from famgz_utils import json_

source_dir = Path(__file__).parent.resolve()
data_dir = Path(source_dir, 'data')
debug_dir = Path(source_dir, 'debug')
products_json_path = Path(data_dir, 'products.json')
sample_path = Path(source_dir, 'product-sample.html')

# create folders
for path in [data_dir, debug_dir]:
     if not path.exists:
          path.mkdir(exist_ok=True)

# create 
if not products_json_path.exists():
     json_(products_json_path, [])