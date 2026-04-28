import simpy
import random
import json
import os

def load_config():
    # JSON dosyasından park yeri yapılandırmasını yükler
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '..', 'data', 'parking_map.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def car(env, name, parking_lot, spots_data, logs, occupancy_history, spot_events):
    # Aracın geliş zamanını kaydeder
    arrival_time = env.now
    logs.append((arrival_time, f"{name} otoparka geldi"))

    with parking_lot.request() as request:
        yield request
        
        # İlk boş yeri bulur
        assigned_spot = next(s for s in spots_data if s["status"] == "empty")
        assigned_spot["status"] = "occupied"
        spot_id = assigned_spot['id']
        
        # Park etme başlangıç zamanını kaydeder
        start_parking = env.now
        logs.append((start_parking, f"{name} Yer ID: {spot_id} konumuna park etti"))
        spot_events.append((start_parking, spot_id, "occupied"))
        
        # Doluluk oranını hesaplar ve kaydeder
        occupied_count = sum(1 for s in spots_data if s["status"] == "occupied")
        occupancy_rate = occupied_count / len(spots_data)
        occupancy_history.append((start_parking, occupancy_rate))
        
        # Rastgele park süresi
        parking_duration = random.randint(15, 45)
        yield env.timeout(parking_duration)
        
        # Araç ayrılır
        assigned_spot["status"] = "empty"
        leave_time = env.now
        logs.append((leave_time, f"{name} ayrıldı (Kaldığı süre: {parking_duration} dk)"))
        spot_events.append((leave_time, spot_id, "empty"))
        
        # Doluluk oranını günceller
        occupied_count = sum(1 for s in spots_data if s["status"] == "occupied")
        occupancy_rate = occupied_count / len(spots_data)
        occupancy_history.append((leave_time, occupancy_rate))

def traffic_generator(env, parking_lot, spots_data, logs, occupancy_history, spot_events):
    # Trafik üretecisi: araçları rastgele aralıklarla gönderir
    car_count = 0
    while True:
        yield env.timeout(random.expovariate(1/5.0))
        car_count += 1
        env.process(car(env, f"Arac_{car_count}", parking_lot, spots_data, logs, occupancy_history, spot_events))

def run_simulation():
    # Simülasyonu çalıştırır ve verileri toplar
    data = load_config()
    env = simpy.Environment()
    capacity = data["total_spots"]
    parking_resource = simpy.Resource(env, capacity=capacity)
    
    logs = []
    occupancy_history = []
    spot_events = []
    
    env.process(traffic_generator(env, parking_resource, data["spots"], logs, occupancy_history, spot_events))
    env.run(until=100)
    
    return data, logs, occupancy_history, spot_events

# Eğer bu dosya doğrudan çalıştırılırsa, simülasyonu çalıştır
if __name__ == "__main__":
    data, logs, occupancy_history, spot_events = run_simulation()
    # Konsola logları yazdır (test için)
    for time, msg in logs:
        print(f"{time:.2f}: {msg}")
