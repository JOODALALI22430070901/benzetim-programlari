import streamlit as st
import pandas as pd
from main import run_simulation

# Simülasyon verilerini yükler ve çalıştırır
@st.cache_data
def get_simulation_data():
    # Simülasyonu çalıştırır ve verileri döndürür
    return run_simulation()

data, logs, occupancy_history, spot_events = get_simulation_data()

# Başlık
st.title("Akıllı Otopark Simülasyon Sistemi")

# Zaman kaydırıcısı
max_time = 100.0
current_time = st.slider("Zaman (dk)", 0.0, max_time, 0.0, step=0.1)

# Geçerli zamandaki park yeri durumlarını hesaplar
def get_spot_status_at_time(time):
    # Her park yeri için son durumu bulur
    status_dict = {}
    for spot in data["spots"]:
        status_dict[spot["id"]] = "empty"  # Varsayılan
    for event_time, spot_id, status in spot_events:
        if event_time <= time:
            status_dict[spot_id] = status
    return status_dict

current_status = get_spot_status_at_time(current_time)

# Doluluk oranını hesaplar
occupied_count = sum(1 for status in current_status.values() if status == "occupied")
occupancy_rate = occupied_count / len(data["spots"])

# Metrikler
col1, col2, col3 = st.columns(3)
col1.metric("Toplam Kapasite", data["total_spots"])
col2.metric("Mevcut Doluluk", f"{occupied_count}/{data['total_spots']}")
col3.metric("Doluluk Oranı", ".2%")

# Park yeri ızgarası
st.subheader("Park Yeri Haritası")
# x ve y koordinatlarına göre ızgara oluşturur
max_x = max(spot["x"] for spot in data["spots"])
max_y = max(spot["y"] for spot in data["spots"])

cols = st.columns(max_x + 1)
for x in range(max_x + 1):
    with cols[x]:
        for y in range(max_y + 1):
            spot = next((s for s in data["spots"] if s["x"] == x and s["y"] == y), None)
            if spot:
                color = "🟢" if current_status[spot["id"]] == "empty" else "🔴"
                st.write(f"{color} Yer {spot['id']}")
            else:
                st.write(" ")

# Doluluk grafiği
st.subheader("Doluluk Oranı Grafiği")
# Geçerli zamana kadar olan verileri alır
history_up_to_now = [(t, r) for t, r in occupancy_history if t <= current_time]
if history_up_to_now:
    df = pd.DataFrame(history_up_to_now, columns=["Zaman", "Doluluk Oranı"])
    st.line_chart(df.set_index("Zaman"))
else:
    st.write("Henüz veri yok")

# İşlem kayıtları (Logs)
st.subheader("İşlem Kayıtları")
logs_up_to_now = [msg for t, msg in logs if t <= current_time]
st.text_area("Kayıtlar", "\n".join(logs_up_to_now), height=200)
