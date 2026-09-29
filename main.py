import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------------------
# 기본 설정
# ---------------------------------------------------------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/happykth/data/main/kobis_movies.csv"
)

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)


# ---------------------------------------------------------------------------
# 데이터 불러오기
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner="데이터를 불러오는 중...")
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 개봉일: 20240101 같은 여덟 자리 숫자 -> 진짜 날짜(datetime)
    df["openDt"] = pd.to_datetime(df["openDt"].astype(str), format="%Y%m%d")

    # 장르: 세로막대(|)로 여러 개 적힌 경우 첫 번째 장르만 사용
    df["genre"] = df["genre"].astype(str).str.split("|").str[0].str.strip()

    return df


# ---------------------------------------------------------------------------
# 공통 도우미
# ---------------------------------------------------------------------------
def show_insight(text: str) -> None:
    """그래프 아래에 '이 그래프로 알 수 있는 것' 한 문장을 보여 주는 자리."""
    st.markdown(f"**💡 이 그래프로 알 수 있는 것**  \n{text}")


# ---------------------------------------------------------------------------
# 구역 1: 분포
# ---------------------------------------------------------------------------
def section_genre_donut(df: pd.DataFrame) -> None:
    st.header("1-1. 장르별 영화 편수")

    genre_counts = df["genre"].value_counts().reset_index()
    genre_counts.columns = ["장르", "편수"]

    fig = px.pie(
        genre_counts,
        names="장르",
        values="편수",
        hole=0.5,
        title="장르별 영화 편수",
    )
    fig.update_traces(
        textinfo="label+percent",
        hovertemplate="장르: %{label}<br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
    )
    st.plotly_chart(fig, use_container_width=True)

    # 👇 여기 문장을 직접 채워 넣으세요
    show_insight("여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어 주세요.")


def section_genre_movie_treemap(df: pd.DataFrame) -> None:
    st.header("1-2. 장르 안의 영화 - 총 관객 트리맵")

    fig = px.treemap(
        df,
        path=["genre", "movieNm"],
        values="total_audi",
        title="장르별 영화 총 관객 트리맵",
    )
    fig.update_traces(
        hovertemplate="영화명: %{label}<br>총 관객: %{value:,}명<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True)

    # 👇 여기 문장을 직접 채워 넣으세요
    show_insight("여기에 이 그래프로 알 수 있는 내용을 한 문장으로 적어 주세요.")


# ---------------------------------------------------------------------------
# 구역 2 이후: 그래프를 추가할 자리
# 새 그래프는 위와 같은 형태의 함수(section_...)를 만들고
# 아래 main()에 st.divider()와 함께 호출만 추가하면 됩니다.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 앱 시작
# ---------------------------------------------------------------------------
def main() -> None:
    st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
    st.caption("KOBIS 박스오피스 10위권 진입 영화 216편 요약 (1년간 개봉작)")

    df = load_data()

    section_genre_donut(df)
    st.divider()

    section_genre_movie_treemap(df)
    st.divider()

    # 다음 그래프 구역은 여기에 추가
    # section_next_graph(df)
    # st.divider()


if __name__ == "__main__":
    main()
