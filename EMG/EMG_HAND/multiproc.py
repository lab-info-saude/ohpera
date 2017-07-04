
import multiprocessing  # the module we will be using for multiprocessing

def work(number):
    """
    Multiprocessing work
    
    Parameters
    ----------
    number : integer
        unit of work number
    """
    
    print "Unit of work number %d" % number  # simply print the worker's number
    
if __name__ == "__main__":  # Allows for the safe importing of the main module
    print("There are %d CPUs on this machine" % multiprocessing.cpu_count())
    number_processes = 2
    pool = multiprocessing.Pool(number_processes)
    total_tasks = 16
    tasks = range(total_tasks)
    results = pool.map_async(work, tasks)
    pool.close()
    pool.join()