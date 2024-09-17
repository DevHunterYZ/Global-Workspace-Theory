import threading
import time
import random

class GlobalWorkspace:
    def __init__(self):
        self.content = None
        self.lock = threading.Lock()
        self.observers = []

    def set_content(self, content):
        with self.lock:
            self.content = content
            print(f"Küresel Çalışma Alanı güncellendi: {content}")
            # Gözlemcileri bilgilendir
            for observer in self.observers:
                observer.notify(content)

    def register_observer(self, observer):
        self.observers.append(observer)

class Processor:
    def __init__(self, name, workspace):
        self.name = name
        self.workspace = workspace
        self.workspace.register_observer(self)

    def process(self):
        # İşlem yap ve bazen bilgiyi küresel alana gönder
        while True:
            time.sleep(random.uniform(0.5, 2.0))
            if random.random() < 0.3:
                content = f"{self.name} işlemlediği veri"
                print(f"{self.name} Küresel Çalışma Alanı'na içerik gönderiyor")
                self.workspace.set_content(content)

    def notify(self, content):
        print(f"{self.name} Küresel Çalışma Alanı'ndan içerik aldı: {content}")
        # İçerikle ilgili işlem yap

# Küresel Çalışma Alanı oluştur
global_workspace = GlobalWorkspace()

# İşlemcileri oluştur
processors = [Processor(f"İşlemci_{i}", global_workspace) for i in range(5)]

# İşlemci iş parçacıklarını başlat
threads = []
for processor in processors:
    t = threading.Thread(target=processor.process)
    t.daemon = True
    t.start()
    threads.append(t)

# Ana iş parçacığını canlı tut
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
