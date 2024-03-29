import sys,time, json, pika

AMQP_HOST= sys.argv[1]
AMQP_PORT= int(sys.argv[2])
creds_broker= pika.PlainCredentials("guest","guest")
conn_params= pika.ConnectionParameters(AMQP_HOST,port=AMQP_PORT,virtual_host= "/",credentials= creds_broker)
conn_broker= pika.BlockingConnection(conn_params)

channel= conn_broker.channel()

msg= json.dumps({"content": "ClusterTest!","time": time.time()})
msg_props= pika.BasicProperties(content_type="application/json")

channel.basic_publish(body=msg,exchange="cluster_test",properties=msg_props,routing_key="cluster_test")
print "Sent cluster test message."