#encoding: UTF-8
#生产者/消费者模式
import threading
import time
 
# 商品
product = None
# 条件变量
con = threading.Condition()
 
# 生产者方法
def produce():
    global product
    
    if con.acquire():
        while True:
            if product is None:
                print 'produce...'
                product = 'anything'
                
                # 通知消费者，商品已经生产     
                # 调用这个方法将从等待池挑选一个线程并通知，收到通知的线程将自动调用acquire()尝试获得锁定（进入锁定池）；
                # 其他线程仍然在等待池中。调用这个方法不会释放锁定。使用前线程必须已获得锁定，否则将抛出异常
                con.notify()
                
                #notifyAll(): 调用这个方法将通知等待池中所有的线程，这些线程都将进入锁定池尝试获得锁定。调用这个方法不会释放锁定。使用前线程必须已获得锁定，否则将抛出异常
            
            # 等待通知   wait会block
            con.wait() 
            time.sleep(2)
 
# 消费者方法
def consume():
    global product
    
    if con.acquire():
        while True:
            if product is not None:
                print 'consume...'
                product = None
                
                # 通知生产者，商品已经没了
                con.notify()
            
            # 等待通知  调用这个方法将使线程进入Condition的等待池等待通知，并释放锁。使用前线程必须已获得锁定，否则将抛出异常
            con.wait()  #wait会block
            time.sleep(2)
 
t1 = threading.Thread(target=produce)
t2 = threading.Thread(target=consume)
t2.start()
t1.start()