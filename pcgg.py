import multiprocessing
import time
import threading

def cpu_load():
    # Sürekli ağır hesaplama
    while True:
        sum(i*i for i in range(20_000_000))  # çok daha yoğun işlem

def ram_load():
    # RAM’i zorlamak için sürekli büyük listeler oluştur
    big_data = []
    while True:
        big_data.append('x'*10_000_000)  # her döngüde ~10MB
        time.sleep(0.1)

if __name__ == "__main__":
    cpu_count = multiprocessing.cpu_count()
    print(f"{cpu_count} çekirdek ve RAM üzerinde maksimum yük başlatılıyor...")

    processes = []

    # CPU yükü
    for _ in range(cpu_count):
        p = multiprocessing.Process(target=cpu_load)
        p.start()
        processes.append(p)

    # RAM yükü
    ram_thread = threading.Thread(target=ram_load)
    ram_thread.start()

    try:
        for p in processes:
            p.join()
        ram_thread.join()
    except KeyboardInterrupt:
        print("Durduruluyor...")
        for p in processes:
            p.terminate()
        print("Tüm işlemler sonlandırıldı.")

