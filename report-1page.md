# Report 1 page - Lab 6 AES-CBC Socket

## Thông tin nhóm

- Thành viên 1: Đặng Quang Tiến (msv: 1871020570)
- Thành viên 2: Nguyễn Hoàng (msv: 1871020250)

## Mục tiêu

Thiết kế và triển khai hệ thống gửi/nhận dữ liệu qua TCP socket với mã hóa AES-CBC. Tách rõ 2 kênh truyền: kênh khóa (KEY_PORT) dùng để gửi AES key và IV, và kênh dữ liệu (DATA_PORT) dùng để gửi ciphertext. Áp dụng PKCS#7 padding cho AES-CBC và xây dựng header 4 byte để truyền độ dài ciphertext. Viết test cho các luồng đúng/sai và rút ra điểm yếu bảo mật khi key/IV được gửi plaintext.

## Phân công thực hiện

- Sender (mã hóa + gửi 2 packet qua socket): Đặng Quang Tiến
- Receiver (nhận + parse header + giải mã + ghi output/log): Nguyễn Hoàng
- Test/log/threat model: cả hai cùng thực hiện và rà soát theo hợp đồng CI

## Cách làm

Sender đọc plaintext từ INPUT_FILE hoặc biến MESSAGE, sau đó mã hóa AES-CBC kèm PKCS#7 padding. Sender đóng gói key/IV theo cấu trúc: [key_length:4][key:16/32][iv:16] rồi gửi qua KEY_PORT. Sender đóng gói ciphertext theo cấu trúc: [ciphertext_length:4][ciphertext:N] rồi gửi qua DATA_PORT. Receiver dùng recv_exact để nhận đủ số byte theo header, parse key packet và length header, rồi decrypt_aes_cbc để lấy plaintext, ghi OUTPUT_FILE và/hoặc RECEIVER_LOG_FILE khi được cấu hình.

## Kết quả

Chạy demo local bằng 2 terminal cho thấy Receiver nhận đúng ciphertext và giải mã khớp với plaintext đầu vào. Các test CI gồm: roundtrip padding/header/key/data channel và các test negative như wrong key và tampered ciphertext đều hoạt động đúng (receiver lỗi hoặc plaintext không trùng). Khi bật log, các file log trong logs/ ghi lại tiến trình nhận/gửi để minh chứng.

## Kết luận

AES-CBC giúp che nội dung plaintext nhưng không tự cung cấp xác thực toàn vẹn; vì vậy ciphertext bị sửa vẫn có thể gây lỗi hoặc tạo plaintext sai mà không có cơ chế xác minh. Điểm yếu lớn trong bài lab là kênh khóa truyền key/IV dạng plaintext (mô phỏng), trong hệ thống thật cần kênh trao đổi khóa an toàn và cơ chế xác thực dữ liệu.
