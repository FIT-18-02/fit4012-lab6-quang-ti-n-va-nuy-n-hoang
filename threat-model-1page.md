# Threat Model - Lab 6 AES-CBC Socket

## Thông tin nhóm

- Thành viên 1: Đặng Quang Tiến (msv: 1871020570)
- Thành viên 2: Nguyễn Hoàng (msv: 1871020250)

## Assets

Cần bảo vệ: plaintext (nội dung người dùng), AES key và IV, ciphertext, file đầu vào/đầu ra và nội dung log (log không nên chứa key hay thông tin nhạy cảm).

## Attacker model

Kẻ tấn công có thể hoạt động trong LAN hoặc trên đường truyền: nghe lén gói tin, bắt/giữ và phát lại (replay) packet, sửa đổi ciphertext hoặc thay đổi key/IV trong kênh khóa. Ngoài ra kẻ tấn công có thể đọc log nếu log bị lộ.

## Threats

Một số mối đe dọa chính:

- **Key/IV disclosure**: key và IV được gửi plaintext trên KEY_PORT nên có thể bị lộ.
- **Tampering (mắc chỉnh sửa ciphertext)**: attacker sửa một vài byte của ciphertext khiến receiver giải mã ra dữ liệu sai hoặc gây lỗi padding.
- **Replay attack**: attacker phát lại các packet cũ (cả key packet và/hoặc data packet) để gây lặp thông điệp.
- **Log leakage**: sender/receiver ghi log có thể vô tình chứa key/IV hoặc dữ liệu nhạy cảm.
- **No authentication**: receiver không xác thực danh tính sender nên không chống được giả mạo sender.

## Mitigations

Các biện pháp giảm thiểu (ít nhất 3):

- Không gửi key/IV dưới dạng plaintext trong hệ thống thật; dùng TLS hoặc key exchange an toàn (ví dụ Diffie-Hellman/ephemeral keys).
- Thay vì AES-CBC “thuần”, dùng cơ chế có xác thực toàn vẹn như **AES-GCM** hoặc **encrypt-then-MAC**.
- Bổ sung nonce/timestamp hoặc sequence number để giảm replay.
- Hạn chế thông tin ghi vào log: không ghi key/IV thật, chỉ ghi metadata phục vụ debug.

## Residual risks

Vẫn còn rủi ro vì mô hình bài lab dùng key channel dạng mô phỏng và thiếu xác thực/chống replay đầy đủ; do đó hệ thống không đạt mức an toàn cho môi trường triển khai thực tế.
