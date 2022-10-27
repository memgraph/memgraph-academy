import mgp
import json


@mgp.transformation
def transaction(messages: mgp.Messages
                ) -> mgp.Record(query=str, parameters=mgp.Nullable[mgp.Map]):
    result_queries = []

    for i in range(messages.total_messages()):
        message = messages.message_at(i)
        transaction_info = json.loads(message.payload().decode('utf8'))
        result_queries.append(
            mgp.Record(
                query=("MATCH (c:Card {id: $card_id}), (p:Pos {id: $pos_id}) "
                       "CREATE (t:Transaction {id: $transaction_id, fraudReported: $compromised}) "
                       "CREATE (c)<-[:Using]-(t)-[:At]->(p)"),
                parameters={
                    "card_id": transaction_info["card_id"],
                    "pos_id": transaction_info["pos_id"],
                    "transaction_id": transaction_info["transaction_id"],
                    "compromised": transaction_info["compromised"]}))

    return result_queries
