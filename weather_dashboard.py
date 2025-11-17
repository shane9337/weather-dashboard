import requests
import streamlit as st

# ==== Streamlit UI ====
st.title("🌦 台灣 36 小時天氣預報 Dashboard")
st.write("資料來源：中央氣象署開放資料平台 CWA")

# 使用者輸入你的 API Key
api_key = st.text_input("請輸入你的 CWA API Key")

# 城市選單
cities = [
    "Taipei", "New Taipei", "Taoyuan", "Hsinchu",
    "Taichung", "Tainan", "Kaohsiung", "Keelung",
]

city = st.selectbox("選擇城市", cities)


# ==== 按鈕觸發查詢 ====
if st.button("查詢天氣"):

    if api_key == "":
        st.error("請先輸入 API Key")
    else:
        # CWA API URL
        url = (
    "http://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001" f"?Authorization={api_key}&locationName={city}")
      r = requests.get(url, timeout=10)


        if r.status_code != 200:
            st.error("API 請求失敗，請檢查 API Key 或網路")
        else:
            data = r.json()

            try:
                location = data["records"]["location"][0]
                weather_elements = location["weatherElement"]

                # 提取資料
                wx = weather_elements[0]["time"][0]["parameter"]["parameterName"]  # 天氣描述
                pop = weather_elements[1]["time"][0]["parameter"]["parameterName"]  # 降雨機率
                min_temp = weather_elements[2]["time"][0]["parameter"]["parameterName"]
                max_temp = weather_elements[4]["time"][0]["parameter"]["parameterName"]
                ci = weather_elements[3]["time"][0]["parameter"]["parameterName"]   # 舒適度

                # ==== 顯示於 Dashboard ====
                st.subheader(f"{city} 未來 36 小時天氣")
                st.write(f"🌥 天氣狀況：{wx}")
                st.write(f"🌧 降雨機率：{pop}%")
                st.write(f"🌡 氣溫：{min_temp}°C ~ {max_temp}°C")
                st.write(f"🙂 舒適度：{ci}")

            except:
                st.error("資料解析失敗，請確認 API Key 是否正確")

