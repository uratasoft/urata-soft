import hashlib
import json
import datetime

class Block:
    hsh = 0
    def __init__(self, index, timestamp, transaction, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.difficulty = 4 #難易度
        self.property_dict = {str(i): j for i, j in self.__dict__.items()}
        self.now_hash = self.calc_hash()
        self.proof = None # プルーフ
        self.proof_hash = None # プルーフを追加して計算したハッシュ

    # ハッシュの計算
    def calc_hash(self):
        # ハッシュ計算用の辞書をjsonに変換して、中身の並べ替え、エンコードの変換
        block_string = json.dumps(self.property_dict, sort_keys=True).encode('ascii')
        #global hsh
        hsh = hashlib.sha256(block_string).hexdigest()
        return hsh

    print(hsh.to_bytes)

    # プルーフの検証用関数
    def check_proof(self, proof):
        proof_string = self.now_hash + str(proof)
        calced = hashlib.sha256(proof_string.encode("ascii")).hexdigest()
        if calced[:self.difficulty:].count('0') == self.difficulty:
            self.proof_hash = calced
            return True
        else:
            return False
 
    # プルーフを採掘するための関数
    def mining(self):
        proof = 0
        while True:
            if self.check_proof(proof):
                break
            else:
                proof += 1
        return proof

##########################################################
    # トランザクション(取引)生成
    def new_transaction(sender, recipient, amount):
        transaction = {
        "差出人": sender,
        "あて先": recipient,
        "金額": amount,
        }
        return transaction

#１．ブロックチェーンを代入するリスト
block_chain = [] 

#２．ブロック作成
# index,timestamp,transaction,previous_hash 初期化
block = Block(0, 0, [], '-')
block.proof = block.mining() 

#３．ブロックチェーンListに最初のブロックを代入
block_chain.append(block) 

#４．トランザクション生成
transaction = Block.new_transaction("太郎", "花子", 100)
# ブロックにindex,timestamp,transaction,previous_hash を格納
new_block = Block(1, str(datetime.datetime.now()),transaction , block_chain[0].now_hash)
# ブロックチェーンListにブロックを代入
block_chain.append(new_block)
########################################################### 
 
for i in range(5):
 
    block = Block(i+1, str(datetime.datetime.now()), ["適当なトランザクション"], block_chain[i].now_hash)
    block.proof = block.mining()
    block_chain.append(block)
 
for block in block_chain:
    for key, value in block.__dict__.items():
        print(key, ':', value)
    print("")