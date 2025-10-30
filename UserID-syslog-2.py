import socket
import time
import datetime

# --- CẤU HÌNH ---
# !!! QUAN TRỌNG: Thay đổi IP này thành địa chỉ IP của máy chủ Syslog (SIEM, log collector...) của bạn
SYSLOG_SERVER_IP = '192.168.2.1' 
SYSLOG_SERVER_PORT = 514           # Cổng UDP 514 như bạn yêu cầu
SLEEP_INTERVAL = 30 * 60           # 30 phút * 60 giây/phút
# --------------------

def send_log_batch(server_ip, port):
    """
    Hàm này tạo và gửi một loạt 100 log message qua UDP.
    """
    print(f"Đang chuẩn bị gửi log đến {server_ip}:{port}...")
    
    # Sử dụng 'with' để đảm bảo socket được đóng đúng cách
    # AF_INET = sử dụng IPv4
    # SOCK_DGRAM = sử dụng UDP
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            # Vòng lặp để tạo 100 user và 100 IP
            # range(1, 101) sẽ chạy từ 1 đến 100
            for i in range(1, 101):
                
                # --- Tạo dữ liệu log động ---
                
                # 1. Tạo user (ví dụ: johndoe01, johndoe02, ...)
                user_id = f"johndoe{i:02d}"
                
                # 2. Tạo địa chỉ IP (ví dụ: 192.168.3.101 ... 192.168.3.200)
                #    (Tôi cập nhật dải IP dựa trên ví dụ của bạn)
                source_ip = f"192.168.2.{100 + i}"
                
                # 3. Lấy thời gian hiện tại và định dạng nó
                #    (Ví dụ: Tue Oct 30 10:30:05 2025 ICT)
                now = datetime.datetime.now()
                tz_name = time.strftime('%Z') # Lấy tên múi giờ (ví dụ: ICT, CDT, PST)
                timestamp = f"{now.strftime('%a %b %d %H:%M:%S %Y')} {tz_name}"
                
                # --- Tạo log message theo đúng định dạng bạn yêu cầu ---
                log_message = f"Login events—[{timestamp}] Administratorauthentication success User:{user_id} Source:{source_ip}"
                
                # Gửi log message.
                # Dữ liệu cần được encode sang 'utf-8' (dạng bytes) trước khi gửi
                sock.sendto(log_message.encode('utf-8'), (server_ip, port))
                
                print(f"Đã gửi: {log_message}")

            print(f"--- Đã gửi xong 100 log. ---")

    except socket.error as e:
        print(f"Lỗi socket: {e}")
    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn: {e}")

def main_loop():
    """
    Vòng lặp chính, gọi hàm send_log_batch và ngủ 30 phút.
    """
    while True:
        try:
            send_log_batch(SYSLOG_SERVER_IP, SYSLOG_SERVER_PORT)
            
            print(f"Đã gửi xong. Tạm nghỉ {SLEEP_INTERVAL / 60} phút...")
            time.sleep(SLEEP_INTERVAL)
            
        except KeyboardInterrupt:
            # Xử lý khi người dùng nhấn Ctrl+C để dừng script
            print("\nĐã nhận tín hiệu dừng (Ctrl+C). Đang thoát...")
            break
        except Exception as e:
            # Xử lý các lỗi khác và thử lại sau 5 phút
            print(f"Lỗi trong vòng lặp chính: {e}")
            print("Sẽ thử lại sau 5 phút...")
            time.sleep(5 * 60)

if __name__ == "__main__":
    if SYSLOG_SERVER_IP == '127.0.0.1':
        print("CẢNH BÁO: Script đang được cấu hình để gửi log đến '127.0.0.1' (localhost).")
        print("Vui lòng mở file .py và thay đổi biến 'SYSLOG_SERVER_IP' thành IP máy chủ của bạn.")
        time.sleep(3) # Dừng 3 giây để người dùng đọc
        
    main_loop()