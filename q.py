import pika


zhihu_qname = 'zhihu'
toutiao_qname = 'toutiao'


def get_ch(qname):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch = connection.channel()
    ch.queue_declare(queue=qname, durable=True)
    return ch
