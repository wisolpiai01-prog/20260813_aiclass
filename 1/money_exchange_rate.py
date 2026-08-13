import json
from datetime import datetime
from urllib.error import HTTPError, URLError
import urllib.request

import streamlit as st

try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None


CURRENCY_OPTIONS = ["USD", "JPY", "CNY"]
BASE_CURRENCY = "KRW"


@st.cache_data(ttl=30)
def fetch_exchange_rate(currency_code: str):
    url = f"https://open.er-api.com/v6/latest/{currency_code}"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))

    if "rates" not in data or BASE_CURRENCY not in data["rates"]:
        raise ValueError(f"{currency_code}의 환율 정보를 찾을 수 없습니다.")

    rate = float(data["rates"][BASE_CURRENCY])
    updated = data.get("time_last_update_utc", "알 수 없음")
    return rate, updated


def format_update_time(value: str) -> str:
    if value == "알 수 없음":
        return value

    try:
        parsed = datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %z")
        return parsed.strftime("%Y-%m-%d %H:%M:%S %Z")
    except ValueError:
        return value


st.set_page_config(page_title="실시간 환율 조회", layout="centered")

if st_autorefresh is not None:
    st_autorefresh(interval=30000, key="exchange_rate_refresh")

st.title("실시간 환율 조회")
st.caption("USD, JPY, CNY 중 하나를 선택하면 30초마다 최신 환율을 자동으로 확인합니다.")

selected_currency = st.selectbox("통화 선택", CURRENCY_OPTIONS, index=0)

try:
    rate, updated = fetch_exchange_rate(selected_currency)

    st.metric(label=f"1 {selected_currency}", value=f"{rate:,.2f} KRW")
    st.info(f"업데이트 시간: {format_update_time(updated)}")
    st.success("30초마다 자동 갱신됩니다.")
except (HTTPError, URLError, ValueError) as exc:
    st.error(f"환율 정보를 가져오지 못했습니다: {exc}")
