import hashlib
import json

class Input:
    def __init__(self, old_tz_id, output_index):
        self.old_tz_id = old_tz_id
        self.output_index = output_index

    def to_dict(self):
        return {
            'old_tz_id': self.old_tz_id,
            'output_index': self.output_index,
        }

class Output:
    def __init__(self, address, value):
        self.address = address
        self.amount = value

    def to_dict(self):
        return {
            'address': self.address,
            'amount': self.amount,
        }

class Transaction:
    def __init__(self, inputs, outputs):
        self.inputs = inputs          
        self.outputs = outputs         
        self.signature = None     
        self.tz_id = None               

    def to_dict(self):
        return {
            'inputs': [i.to_dict() for i in self.inputs],
            'outputs': [o.to_dict() for o in self.outputs],
            'signature': self.signature,
            'tz_id': self.tz_id,
        }

    def serialize(self):
        return json.dumps(self.to_dict(), sort_keys=True).encode()

    @staticmethod
    def deserialize(serialized_bytes):
        data = json.loads(serialized_bytes.decode())
        
        inputs = [Input(i['old_tz_id'], i['output_index']) for i in data['inputs']]
        
        outputs = [Output(o['address'], o['amount']) for o in data['outputs']]
        
        tx = Transaction(inputs, outputs)
        tx.signature = data.get('signature')
        tx.tz_id = data.get('tz_id')
        
        return tx

    def hash_tz_id(self):
        tz_data = json.dumps(
            {
            'inputs': [i.to_dict() for i in self.inputs],
            'outputs': [o.to_dict() for o in self.outputs],
            }, 
            sort_keys=True).encode()
        
        return hashlib.sha256(tz_data).hexdigest()

    def sign(self, private_key):
        tz_hash = self.hash_tz_id()
        
        signature_data = (private_key + tz_hash).encode() #имитация подписи
        self.signature = hashlib.sha256(signature_data).hexdigest()

        self.tz_id = self.hash_tz_id()

    def verify_signature(self, public_key):
        if not self.signature:
            return False
        
        expected_signature = hashlib.sha256((public_key + self.hash_tz_id()).encode()).hexdigest()
        
        return expected_signature == self.signature
    
#тестирование
if __name__ == "__main__":

    input_1 = Input("prev_tx_hash_1", 0)
    output_1 = Output("Hugo", 18)

    tz1 = Transaction(
        inputs=[input_1],
        outputs=[output_1]
    )

    private_key = "private"
    public_key = "open_key"

    tz1.sign(private_key)

    print("Подлинность подписи:", tz1.verify_signature(public_key))

    serialized_tx = tz1.serialize()
    print("Сериализованная транзакция:", serialized_tx)

    restored_tx = Transaction.deserialize(serialized_tx)
    
    print("Восстановленная транзакция ID:", restored_tx.tz_id)