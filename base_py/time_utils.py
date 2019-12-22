import time


def cal_time_delta():
    t1 = time.time()

    for i in range(2):
        # do program here
        time.sleep(2)

    t2 = time.time()

    print(t2 - t1)
