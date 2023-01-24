def create_queue(length):
    queue = [0]*(length+1) # premier element : index du dernier ajoute
    return queue

def add_element(elem, queue):
    length = len(queue) - 1
    elem_index = int(queue[0]%length + 1)
    queue[elem_index] = elem
    queue[0] = elem_index

def avg_queue(queue):
    n = len(queue) - 1
    avg = (sum(queue) - queue[0])/n
    return avg
