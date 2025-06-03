from Блокчейн import Input
from Блокчейн import Transaction
from Блокчейн import Output

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