import pika


zhihu_qname = 'zhihu'
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
zhihu_c = connection.channel()
zhihu_c.queue_declare(queue=zhihu_qname, durable=True)


toutiao_qname = 'toutiao'
toutiao_c = connection.channel()
toutiao_c.queue_declare(queue=toutiao_qname, durable=True)
