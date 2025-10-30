# user-ip-mapping-syslog

Trình tạo Log User-ID Syslog cho Palo Alto

Một script Python đơn giản được thiết kế để tạo và gửi các log message User-ID mapping qua Syslog (UDP) đến tường lửa Palo Alto Networks.

Mục đích

Script này được sử dụng để tích hợp thông tin User-IP mapping từ các nguồn tùy chỉnh vào tính năng User-ID của tường lửa Palo Alto.

Trong nhiều môi trường không tích hợp trực tiếp với Active Directory (AD), hoặc khi người dùng được xác thực bởi các hệ thống khác (ví dụ: Wi-Fi controller, VPN, ứng dụng nội bộ), script này có thể được điều chỉnh để đọc thông tin (user, ip) từ nguồn đó và gửi đến tường lửa. Điều này cho phép tường lửa thực thi các chính sách bảo mật dựa trên danh tính người dùng, thay vì chỉ dựa trên địa chỉ IP.

Các trường hợp sử dụng phổ biến:

Tích hợp tùy chỉnh: Gửi thông tin đăng nhập từ các hệ thống không-phải-Microsoft (ví dụ: máy chủ DHCP, Linux, macOS, các ứng dụng web) đến Palo Alto.

Kiểm thử Chính sách (Policy): Thử nghiệm các Security Policy dựa trên User-ID (ví dụ: "chỉ cho phép nhóm Kế toán truy cập máy chủ tài chính").

Kiểm tra Phân tích (Parsing): Xác minh rằng cấu hình "Syslog Parse Profile" trên Palo Alto của bạn đang hoạt động chính xác và trích xuất đúng user/ip.

Tạo dữ liệu mẫu: Làm đầy (populate) bảng User-ID mapping trên tường lửa cho mục đích demo hoặc kiểm thử.

Tính năng

Giao thức: Gửi log qua UDP.

Tùy chỉnh Máy chủ: Dễ dàng cấu hình IP và port của Palo Alto (Syslog server profile).

Tạo Dữ liệu Động: Tự động tạo 100 cặp user/IP mapping.

Chạy theo lịch: Tự động lặp lại việc gửi log mỗi 30 phút (hữu ích để mô phỏng việc "refresh" thông tin mapping).

Định dạng Log

Để Palo Alto User-ID có thể đọc được, log message cần ở một định dạng đơn giản, rõ ràng mà "Syslog Parse Profile" có thể trích xuất được. Script này (cần được cập nhật) để gửi định dạng đơn giản như sau:

Định dạng khuyến nghị: DOMAIN\user,ip_address

Ví dụ:

MYDOMAIN\johndoe01,192.168.3.101


Trong đó:

MYDOMAIN là tên domain (có thể tùy chỉnh).

johndoeXX sẽ tăng từ johndoe01 đến johndoe100.

192.168.3.XXX sẽ tăng từ 192.168.3.101 đến 192.168.3.200.

(Lưu ý: Bạn sẽ cần cấu hình một "Syslog Parse Profile" trên Palo Alto với Regex phù hợp, ví dụ: (.*)\,(.*), để trích xuất user và ip từ định dạng này).

Cách sử dụng

1. Yêu cầu

Python 3

Tường lửa Palo Alto đã được cấu hình với "Syslog Server Profile" và "Syslog Parse Profile".

2. Cấu hình

Trước khi chạy, hãy mở file send_syslog.py và chỉnh sửa các biến:

# --- CẤU HÌNH ---
# IP của Palo Alto (hoặc Panorama) nơi bạn đã cấu hình Syslog Server Profile
SYSLOG_SERVER_IP = '192.168.1.112' 
SYSLOG_SERVER_PORT = 514           # Cổng UDP (mặc định cho syslog)
SLEEP_INTERVAL = 30 * 60           # 30 phút
# --------------------


QUAN TRỌNG: Bạn cũng cần cập nhật logic tạo log_message trong file .py để khớp với định dạng log mới (ví dụ: log_message = f"MYDOMAIN\\{user_id},{source_ip}").

3. Chạy Script

Chạy script từ terminal của bạn:

python send_syslog.py


Script sẽ bắt đầu gửi loạt log đầu tiên và in output ra màn hình (giả sử script đã được cập nhật):

Đang chuẩn bị gửi log đến 192.168.1.112:514...
Đã gửi: MYDOMAIN\johndoe01,192.168.3.101
Đã gửi: MYDOMAIN\johndoe02,192.168.3.102
...
--- Đã gửi xong 100 log. ---
Đã gửi xong. Tạm nghỉ 30.0 phút...


4. Dừng Script

Nhấn Ctrl+C để dừng vòng lặp.

