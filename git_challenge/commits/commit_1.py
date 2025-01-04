import time


def typing(content: str):
    for i in range(len(content)):
        print(f"\r{content[:i+1]}", end="")
        time.sleep(0.1)


typing("Hello, World!")
