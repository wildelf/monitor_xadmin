
import os,sys
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)


from core import info_collection

if __name__ == '__main__':

    sent_data = info_collection.InfoCollection()
    sent_data.run()