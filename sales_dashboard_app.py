import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 골드앤 샘플 매출 분석 대시보드")

st.markdown("---")
st.subheader("1. CSV 파일 업로드")

uploaded_file = st.file_uploader("쿠팡 매출 데이터를 업로드하세요 (CSV 형식)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ 데이터 업로드 완료!")

    # 날짜 처리
    df['날짜'] = pd.to_datetime(df['날짜'])
    df['월'] = df['날짜'].dt.to_period('M')

    # 제품별 요약
    product_summary = df.groupby('상품명')[['판매수량', '매출']].sum().sort_values(by="매출", ascending=False)
    st.subheader("2. 제품별 누적 매출")
    st.dataframe(product_summary)

    # 월별 매출 추이
    monthly_summary = df.groupby('월')[['판매수량', '매출']].sum().reset_index()
    st.subheader("3. 월별 매출 추이")
    fig, ax = plt.subplots()
    ax.plot(monthly_summary['월'].astype(str), monthly_summary['매출'], marker='o')
    ax.set_ylabel("매출")
    ax.set_xlabel("월")
    ax.set_title("월별 매출 변화 추이")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # 상위 상품 파이차트
    st.subheader("4. 상위 제품 매출 비중")
    top5 = product_summary.head(5)
    fig2, ax2 = plt.subplots()
    ax2.pie(top5['매출'], labels=top5.index, autopct='%1.1f%%', startangle=140)
    ax2.axis('equal')
    st.pyplot(fig2)
else:
    st.info("⬆️ 위에 CSV 파일을 업로드하면 자동 분석됩니다.")

