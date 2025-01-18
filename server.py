import socket
import struct
import json
import concurrent.futures
import numpy as np

HOST = '0.0.0.0'
PORT = 65434

def read_bytes(sock, size):

    buffer = b''
    while len(buffer) < size:
        part = sock.recv(size - len(buffer))
        if not part:
            return None
        buffer += part
    return buffer

def process_client_connection(conn, addr):
    print(f"[{addr}] З'єднання встановлено")
    try:
        # 1. Отримуємо розміри матриць
        header_data = read_bytes(conn, 12)  # три int32 (N, M, L)
        if not header_data:
            return
        N, M, L = struct.unpack('!iii', header_data)

        # 2. Отримуємо матриці у вигляді байт
        matrix1_size_data = read_bytes(conn, 4)
        matrix1_size = struct.unpack('!i', matrix1_size_data)[0]
        matrix1_data = read_bytes(conn, matrix1_size)

        matrix1 = np.array(json.loads(matrix1_data.decode('utf-8')))

        matrix2_size_data = read_bytes(conn, 4)
        matrix2_size = struct.unpack('!i', matrix2_size_data)[0]
        matrix2_data = read_bytes(conn, matrix2_size)

        matrix2 = np.array(json.loads(matrix2_data.decode('utf-8')))

        # 3. Виконуємо множення матриць
        result_matrix = np.dot(matrix1, matrix2)

        # 4. Відправляємо результат назад
        result_data = json.dumps(result_matrix.tolist()).encode('utf-8')
        conn.sendall(struct.pack('!i', len(result_data)))  # відправляємо довжину
        conn.sendall(result_data)  # відправляємо самі дані

    except Exception as e:
        print(f"[{addr}] Помилка: {e}")
    finally:
        conn.close()
        print(f"[{addr}] З'єднання завершено")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Сервер слухає на порту {PORT}...")

        # Використовуємо пул потоків для обробки запитів
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
            while True:
                client_conn, client_addr = server_socket.accept()
                pool.submit(process_client_connection, client_conn, client_addr)

if __name__ == "__main__":
    start_server()
#Головатюк Михайло КІ-23 МКР