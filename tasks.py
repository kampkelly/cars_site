from includes.index import *

@celery.task()
def add_together(a, b):
    print('okay')
    return a + b

result = add_together.delay(23, 42)
result.wait()