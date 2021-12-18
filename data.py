from config import DATA_DIR
from models import Storage

STORAGE_FILE = DATA_DIR/'data.json'

def load_data():
	if STORAGE_FILE.exists():
		return Storage.parse_file(STORAGE_FILE)
	else:
		return Storage(talks={}, lower_thirds={}, version="")

def save_data(data):
	with open(STORAGE_FILE, "w") as f:
		f.write(data.json(indent='\t'))

def reset():
	save_data(Storage(talks={}, lower_thirds={}, version=""))
