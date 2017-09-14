from threading import Thread 

def debug(f):
    def wrapper(*args, **kwargs):
        stream = logging.StreamHandler(sys.stdout)
        stream.setLevel(logging.DEBUG)
        log = logging.getLogger(f)
        log.addHandler(stream)
        log.setLevel(logging.DEBUG)
    return wrapper

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper
