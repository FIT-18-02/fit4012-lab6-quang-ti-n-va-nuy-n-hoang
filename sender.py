import os
import socket
import time
from pathlib import Path

from aes_socket_utils import build_data_packet, build_key_packet, encrypt_aes_cbc

SERVER_IP = os.getenv("SERVER_IP", "127.0.0.1")
DATA_PORT = int(os.getenv("DATA_PORT", "6000"))
KEY_PORT = int(os.getenv("KEY_PORT", "6001"))
AES_KEY_SIZE = int(os.getenv("AES_KEY_SIZE", "16"))
MESSAGE_ENV = os.getenv("MESSAGE")
INPUT_FILE = os.getenv("INPUT_FILE", "")
LOG_FILE = os.getenv("SENDER_LOG_FILE", "")
TIMEOUT = float(os.getenv("SOCKET_TIMEOUT", "10"))


def get_plaintext() -> bytes:
    """Read plaintext from INPUT_FILE, MESSAGE, or keyboard input."""
    if INPUT_FILE:
        return Path(INPUT_FILE).read_bytes()
    if MESSAGE_ENV is not None:
        return MESSAGE_ENV.encode("utf-8")
    return input("Nhập bản tin: ").encode("utf-8")


def send_packet(host: str, port: int, packet: bytes) -> None:
    """Open one TCP connection and send all bytes."""
    # Thử kết nối lại nếu receiver chưa sẵn sàng
    max_retries = 5
    for attempt in range(max_retries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(TIMEOUT)
                sock.connect((host, port))
                sock.sendall(packet)
                return  # Thành công thì thoát
        except ConnectionRefusedError:
            if attempt < max_retries - 1:
                print(f"Chờ receiver sẵn sàng... (attempt {attempt + 1}/{max_retries})", flush=True)
                time.sleep(1)  # Chờ 1 giây rồi thử lại
            else:
                raise  # Lần cuối vẫn thất bại thì raise lỗi


def main() -> None:
    # ĐỢI RECEIVER SẴN SÀNG - QUAN TRỌNG!
    print("Đợi receiver khởi động...", flush=True)
    time.sleep(2)  # Chờ 2 giây để receiver kịp lắng nghe
    plaintext = get_plaintext()
    key, iv, ciphertext = encrypt_aes_cbc(plaintext, key_size=AES_KEY_SIZE)

    key_packet = build_key_packet(key, iv)
    data_packet = build_data_packet(ciphertext)
    print("Đang gửi key packet...", flush=True)

    send_packet(SERVER_IP, KEY_PORT, key_packet)
    print("Đã gửi key packet", flush=True)
    
    print("Đang gửi data packet...", flush=True)
    send_packet(SERVER_IP, DATA_PORT, data_packet)
    print("Đã gửi data packet", flush=True)

    lines = [
        "[+] Đã tạo AES key và IV.",
        "[+] Đã gửi key/IV qua kênh khóa.",
        "[+] Đã gửi ciphertext qua kênh dữ liệu.",
        f"Server: {SERVER_IP}",
        f"Key port: {KEY_PORT}",
        f"Data port: {DATA_PORT}",
        f"AES key size: {len(key)} bytes",
        f"Key: {key.hex()}",
        f"IV: {iv.hex()}",
        f"Plaintext length: {len(plaintext)} bytes",
        f"Plaintext: {plaintext.decode('utf-8', errors='replace')}",
        f"Ciphertext length: {len(ciphertext)} bytes",
        f"Ciphertext: {ciphertext.hex()}",
    ]

    for line in lines:
        print(line)
        print(line, flush=True)

    if LOG_FILE:
        Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
        Path(LOG_FILE).write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
