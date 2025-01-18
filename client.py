#МКР ГОЛОВАТЮК КІ-23
import socket
import struct
import json
import numpy as np
import random

HOST = '127.0.0.1'
PORT = 65434


def send_data(sock, data):
    """Функція для відправлення даних через сокет."""
    sock.sendall(data)

def start_client():
    # 1. Генеруємо розміри для матриць
    rows = random.randint(1001, 1100)
    cols = random.randint(1001, 1100)
    depth = random.randint(1001, 1100)

    # 2. Створюємо матриці з випадковими цілими числами
    matrix1 = np.random.randint(0, 10, size=(rows, cols))  # матриця розміру rows x cols
    matrix2 = np.random.randint(0, 10, size=(cols, depth))  # матриця розміру cols x depth

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        # 3. Відправляємо розміри матриць
        sock.sendall(struct.pack('!iii', rows, cols, depth))

        # 4. Відправляємо матриці у вигляді JSON
        matrix1_json = json.dumps(matrix1.tolist()).encode('utf-8')
        sock.sendall(struct.pack('!i', len(matrix1_json)))
        send_data(sock, matrix1_json)

        matrix2_json = json.dumps(matrix2.tolist()).encode('utf-8')
        sock.sendall(struct.pack('!i', len(matrix2_json)))
        send_data(sock, matrix2_json)

        # 5. Отримуємо результат множення матриць
        length_data = sock.recv(4)
        result_size = struct.unpack('!i', length_data)[0]
        result_data = b''
        while len(result_data) < result_size:
            chunk = sock.recv(result_size - len(result_data))
            if not chunk:
                break
            result_data += chunk
        result_matrix = np.array(json.loads(result_data.decode('utf-8')))

        # Перевіряємо розмір отриманої матриці
        print(f"Розмір отриманої матриці: {result_matrix.shape}")
        # Виводимо перші 5x5 елементів результату
        print(result_matrix[:5, :5])

if __name__ == "__main__":
    start_client()
#Головатюк Михайло КІ-23 МКР