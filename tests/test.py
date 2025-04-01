import threading
import queue
import time , random

def worker(task_queue, thread_id):
    while True:
        try:
            data = task_queue.get(timeout=1)  # Lấy dữ liệu từ hàng đợi
            print(f"Thread-{thread_id} đang xử lý dữ liệu: {data}")
            time.sleep(random.randint(5,30))  # Giả lập thời gian xử lý
            print(f"Thread-{thread_id} đã hoàn thành dữ liệu: {data}")
            task_queue.task_done()
        except queue.Empty:
            break

if __name__ == "__main__":
    total_tasks = 10  # Tổng số công việc
    max_concurrent_threads = 5  # Số luồng chạy đồng thời
    
    task_queue = queue.Queue()
    for i in range(1, total_tasks + 1):
        task_queue.put(i)
    
    threads = []
    for _ in range(max_concurrent_threads):
        thread = threading.Thread(target=worker, args=(task_queue, len(threads) + 1))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    print("Tất cả công việc đã hoàn thành!")
