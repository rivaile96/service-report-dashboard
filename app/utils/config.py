import os

class Config:
    DATA_DIR = os.path.join("app", "data")
    DATA_FILE = os.path.join(DATA_DIR, "service_data.xlsx")
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    
    @staticmethod
    def init_app():
        os.makedirs(Config.DATA_DIR, exist_ok=True)