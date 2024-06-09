import socket
import psutil
import threading
import time


def get_process_memory_usage(pid):
    """
    This function retrieves memory usage for a specific process ID.

    Args:
        pid: The process ID of the process to monitor.

    Returns:
        The memory usage percentage of the process as a float, or None if process not found.
    """
    try:
        process = psutil.Process(pid)
        info = process.as_dict(attrs=['memory_info'])
        memory_used = info['memory_info'].rss / (1024 * 1024)  # Convert to MB
        total_memory = psutil.virtual_memory().total / (1024 * 1024)  # Convert to MB
        return memory_used / total_memory * 100
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None


def monitor_memory(pid, interval=1):
    """
    This function monitors memory usage for a given process ID in a separate thread.

    Args:
        pid: The process ID of the process to monitor.
        interval: The time interval (in seconds) between checks.
    """
    while True:
        usage = get_process_memory_usage(pid)
        if usage is not None:
            print(f"Process PID: {pid}, Memory Usage: {usage:.2f}%")
        time.sleep(interval)

# Replace this with your actual socket process logic


def your_socket_process():
    # Your socket communication code goes here
    print("Socket process running...")

    master = socket.socket()

    host = "localhost"
    port = 8080

    master.bind((host, port))
    master.listen(1)

    slave, address = master.accept()

    while True:
        print(">", end=" ")
        command = input()
        slave.send(command.encode())

        if command == "exit":
            break

        output = slave.recv(5000)
        print(output.decode())

    master.close()

if __name__ == "__main__":
    # Get the PID of your socket process (replace with actual method)
    socket_process_pid = your_socket_process()  # Hypothetical function

    # Start the memory monitoring thread for the socket process
    memory_thread = threading.Thread(
        target=monitor_memory, args=(socket_process_pid,))
    memory_thread.start()
