import hashlib
import json
import datetime

# ハッシュの計算
def start(self, index, timestamp, transaction, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.transaction = transaction
    self.previous_hash = previous_hash
    self.property_dict = {str(i): j for i, j in self.__dict__.items()}
    self.now_hash = self.calc_hash()

def calc_hash(self):
    # ハッシュ計算用の辞書をjsonに変換して、中身の並べ替え、エンコードの変換
    block_string = json.dumps(self.property_dict, sort_keys=True).encode('ascii')
    hsh = hashlib.sha256(block_string).hexdigest()
    print(hsh)
    return hsh

start()