import multiprocessing as mp


def f(conn):
    print("The f has been started, pid is {}, process name is {}, current process is {}".format(
        mp.Process.pid, mp.Process.name, mp.current_process()))
    conn.send([1,'test',None])
    conn.send([2,'test',None])
    print(conn.recv())
    conn.close()


if __name__ == "__main__":

    parent_conn, child_conn = mp.Pipe()

    tasks = []

    while 1:
        mp.Process(target=f, args=(child_conn,)).start()

    print(parent_conn.recv())
    print("The main has been started, pid is {}, process name is {}, current process is {}".format(
        mp.Process.pid, mp.Process.name, mp.current_process()))
    parent_conn.send('father test')
