Peer review response - Lab 6 AES Socket

Thành viên 1: Đặng Quang Tiến (msv: 1871020570)
Thành viên 2: Nguyễn Hoàng (msv: 1871020250)

- Sender/Receiver AES-CBC + PKCS#7 padding chạy đúng theo protocol 2 kênh (KEY_PORT và DATA_PORT).
- Header 4 byte (length) được dùng để truyền độ dài ciphertext; key channel truyền [key_length][key][iv].
- Các test âm (wrong key, tampered ciphertext) được xử lý đúng: receiver sẽ lỗi hoặc plaintext không khớp.

Ghi chú bổ sung: Đây là mô hình demo/learning, kênh key truyền plaintext nên không an toàn trong thực tế.
