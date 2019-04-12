
def a():
    try:
        print(1)
        return
    finally:
        print(2)

a()