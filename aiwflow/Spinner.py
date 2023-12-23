import concurrent.futures
import threading
import time
import itertools

class Spinner:
    loading_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.function_args = args
        self.function_kwargs = kwargs
        self.api_request_done = threading.Event()
        self.result = None  # 保存函数执行结果
        self._run()

    def loading_animation(self):
        for char in itertools.cycle(self.loading_chars):
            if self.api_request_done.is_set():
                break
            print(f"Loading... {char}", end='\r')
            time.sleep(0.1)

    def execute_function(self):
        result = self.function(*self.function_args, **self.function_kwargs)
        self.api_request_done.set()
        self.result = result  # 保存函数执行结果
        return result

    def _run(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 创建loading线程
            loading_thread = threading.Thread(target=self.loading_animation)

            # 在ThreadPoolExecutor中执行函数
            future = executor.submit(self.execute_function)

            # 启动loading线程
            loading_thread.start()

            # 等待执行函数完成
            result = future.result()

            # 当执行函数完成后，loading线程会检测到Event被设置，然后结束loading提示
            self.api_request_done.set()
            loading_thread.join()

            print("\033[K", end='')  # 清除当前行
            return result

# 示例函数，可以替换为你实际的函数
def sample_function(param1, param2):
    time.sleep(3)  # 模拟函数执行时间
    return f"Function result with params: {param1}, {param2}"

def main():
    # 使用示例
    params = {"param1": "value1", "param2": "value2"}
    loading_with_thread_pool = Spinner(sample_function, **params)
    print("Function result:", loading_with_thread_pool.result)

if __name__ == "__main__":
    main()
