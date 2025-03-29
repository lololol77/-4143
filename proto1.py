# Streamlit 기반 장애인 일자리 매칭 시스템
import streamlit as st
import sqlite3

# DB 연결 함수
def connect_db():
    conn = sqlite3.connect("job_matching_fixed.db")
    return conn

# 매칭 결과 조회 함수
def get_matching_results(role, input_data):
    conn = connect_db()
    cur = conn.cursor()

    if role == '구직자':
        disability, severity = input_data
        query = '''
        SELECT a.name, m.suitability 
        FROM abilities a
        JOIN matching m ON a.id = m.ability_id
        JOIN disabilities d ON d.id = m.disability_id
        WHERE d.name = ? AND d.severity = ?;
        '''
        cur.execute(query, (disability, severity))
        results = cur.fetchall()
    else:
        abilities = input_data
        results = []
        for ability in abilities:
            query = '''
            SELECT d.name, d.severity, m.suitability 
            FROM disabilities d
            JOIN matching m ON d.id = m.disability_id
            JOIN abilities a ON a.id = m.ability_id
            WHERE a.name = ?;
            '''
            cur.execute(query, (ability,))
            results.extend(cur.fetchall())

    conn.close()
    return results

# Streamlit UI
st.title("장애인 일자리 매칭 시스템")

role = st.selectbox("사용자 역할 선택", ["구직자", "구인자"])

if role == "구직자":
    disability = st.selectbox("장애유형", ["시각장애", "청각장애", "지체장애", "뇌병변장애", "언어장애", "안면장애", "신장장애", "심장장애", "간장애", "호흡기장애", "장루·요루장애", "뇌전증장애", "지적장애", "자폐성장애", "정신장애"])
    severity = st.selectbox("장애 정도", ["심하지 않은", "심한"])
    if st.button("매칭 결과 보기"):
        results = get_matching_results("구직자", (disability, severity))
        for ability, suitability in results:
            st.write(f"- {ability}: {suitability}")

elif role == "구인자":
    abilities = st.multiselect("필요한 능력 선택", ["주의력", "아이디어 발상 및 논리적 사고", "기억력", "지각능력", "수리능력", "공간능력", "언어능력", "지구력", "유연성 · 균형 및 조정", "체력", "움직임 통제능력", "정밀한 조작능력", "반응시간 및 속도", "청각 및 언어능력", "시각능력"])
    if st.button("매칭 결과 보기"):
        results = get_matching_results("구인자", abilities)
        for name, severity, suitability in results:
            st.write(f"- {name} ({severity}): {suitability}")

# 유료 서비스 여부 확인
if st.button("대화 종료"):
    use_service = st.radio("AI 이력서 첨삭 서비스 이용하시겠습니까?", ["네", "아니요"])
    if use_service == "네":
        st.write("AI 이력서 첨삭 서비스를 이용해 주셔서 감사합니다!")
    else:
        st.write("대화를 종료합니다.")
