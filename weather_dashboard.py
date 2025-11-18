import os
import requests
import streamlit as st

# ==== Streamlit UI ====
st.title("🌦 台灣 36 小時天氣預報 Dashboard")
st.write("資料來源：中央氣象署開放資料平台 CWA")

# 從環境變數讀 API Key
api_key = os.getenv("CWA_API_KEY")

if not api_key:
    st.error("找不到環境變數 CWA_API_KEY，請先到系統設定 API 金鑰！")
    st.stop()

# 顯示用城市（英文）
cities = [
    "Taipei", "New Taipei", "Taoyuan", "Yunlin",
    "Taichung", "Tainan", "Kaohsiung", "Keelung",
]

# 實際丟給 API 的中文地名
city_map = {
    "Taipei": "臺北市",
    "New Taipei": "新北市",
    "Taoyuan": "桃園市",
    "Yunlin": "雲林縣",
    "Taichung": "臺中市",
    "Tainan": "臺南市",
    "Kaohsiung": "高雄市",
    "Keelung": "基隆市",
}

city_display = st.selectbox("選擇城市", cities)

# ==== 查詢 ====
if st.button("查詢天氣"):

    api_city = city_map[city_display]  # 給 API 用的中文地名

    base_url = "http://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": api_key,
        "locationName": api_city,
    }

    try:
        r = requests.get(base_url, params=params, timeout=10)
    except Exception as e:
        st.error("連線到中央氣象署失敗，請檢查網路。")
        st.write(e)
        st.stop()

    if r.status_code != 200:
        st.error("API 請求失敗！請檢查 API Key 或網路連線。")
        st.write("狀態碼：", r.status_code)
    else:
        data = r.json()
        locations = data.get("records", {}).get("location", [])

        # 如果沒資料，避免再炸 IndexError
        if not locations:
            st.error("中央氣象署沒有回傳這個地點的資料，請確認 API 金鑰與城市名稱。")
            st.write("DEBUG 回傳內容：", data)
        else:
            try:
                location = locations[0]
                weather_elements = location["weatherElement"]

                wx = weather_elements[0]["time"][0]["parameter"]["parameterName"]   # 天氣狀況
                pop = weather_elements[1]["time"][0]["parameter"]["parameterName"]  # 降雨機率
                min_temp = weather_elements[2]["time"][0]["parameter"]["parameterName"]
                max_temp = weather_elements[4]["time"][0]["parameter"]["parameterName"]
                ci = weather_elements[3]["time"][0]["parameter"]["parameterName"]   # 舒適度

                st.subheader(f"{city_display}（{api_city}）未來 36 小時天氣")
                st.write(f"🌥 天氣狀況：{wx}")
                st.write(f"🌧 降雨機率：{pop}%")
                st.write(f"🌡 氣溫：{min_temp}°C ~ {max_temp}°C")
                st.write(f"🙂 舒適度：{ci}")

            except Exception as e:
                st.error("資料解析失敗（API 回傳格式有問題）")
                st.write("DEBUG 回傳內容：", data)
                st.write(e)
