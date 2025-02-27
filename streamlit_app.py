import streamlit as st
import anthropic
import json
import time

# 제목과 설명 표시
st.title("🏢 정부지원과제 사업계획서 작성기")
st.write(
    "정부지원과제 공고 내용과 회사 정보를 입력하면 Claude AI가 맞춤형 사업계획서를 작성해 드립니다. "
    "이 앱을 사용하려면 Anthropic의 Claude API 키가 필요합니다."
)

# 사용자로부터 Claude API 키 입력 받기
claude_api_key = st.text_input("Claude API Key", type="password")

if not claude_api_key:
    st.info("계속하려면 Claude API 키를 입력해주세요.", icon="🔑")
else:
    try:
        # Claude 클라이언트 생성
        client = anthropic.Anthropic(api_key=claude_api_key)
        
        # 사용 가능한 모델 목록 가져오기
        with st.spinner("사용 가능한 Claude 모델을 확인 중입니다..."):
            models_response = client.models.list()
            available_models = [model.id for model in models_response.data if "claude" in model.id.lower()]
        
        if not available_models:
            st.error("사용 가능한 Claude 모델이 없습니다. API 키를 확인해주세요.")
        else:
            # 사용자가 모델 선택
            selected_model = st.selectbox("사용할 Claude 모델 선택", available_models)
            
            # 입력 섹션 생성
            st.subheader("1. 정부지원과제 공고 정보")
            announcement = st.text_area(
                "정부지원과제 공고 내용을 입력해주세요",
                height=200,
                placeholder="예: 중소기업 디지털 전환 지원사업 공고\n지원대상: 제조업 분야 중소기업\n지원내용: 스마트공장 구축 및 디지털 전환..."
            )
            
            st.subheader("2. 회사 정보")
            company_name = st.text_input("회사명")
            business_type = st.text_input("업종")
            company_size = st.selectbox("회사 규모", ["소기업", "중기업", "중견기업"])
            employee_count = st.number_input("직원 수", min_value=1, value=10)
            annual_revenue = st.number_input("연간 매출액(백만원)", min_value=0, value=500)
            
            company_history = st.text_area(
                "회사 연혁",
                height=100,
                placeholder="예: 2015년 설립, 2018년 벤처기업 인증, 2020년 수출유망기업 선정..."
            )
            
            core_business = st.text_area(
                "주요 사업 내용",
                height=100,
                placeholder="회사의 주요 제품, 서비스, 기술력 등을 설명해주세요."
            )
            
            company_strength = st.text_area(
                "회사의 강점",
                height=100,
                placeholder="기술력, 인력, 특허, 시장 점유율 등 회사의 강점을 설명해주세요."
            )
            
            project_goals = st.text_area(
                "이 정부지원과제를 통해 달성하고자 하는 목표",
                height=100,
                placeholder="예: 생산성 향상, 신제품 개발, 해외 시장 진출 등"
            )
            
            # 사업계획서 생성 버튼
            if st.button("사업계획서 생성"):
                if not announcement or not company_name or not business_type or not core_business:
                    st.error("필수 정보(공고 내용, 회사명, 업종, 주요 사업 내용)를 모두 입력해주세요.")
                else:
                    # 회사 정보 구성
                    company_info = f"""
                    회사명: {company_name}
                    업종: {business_type}
                    회사 규모: {company_size}
                    직원 수: {employee_count}명
                    연간 매출액: {annual_revenue}백만원
                    회사 연혁: {company_history}
                    주요 사업 내용: {core_business}
                    회사의 강점: {company_strength}
                    프로젝트 목표: {project_goals}
                    """
                    
                    # 프롬프트 작성
                    prompt = f"""
                    당신은 정부지원과제 사업계획서 작성 전문가입니다. 다음 정보를 기반으로 약 30페이지 분량의 상세한 사업계획서를 작성해주세요.
                    
                    ## 정부지원과제 공고 내용:
                    {announcement}
                    
                    ## 회사 정보:
                    {company_info}
                    
                    사업계획서는 다음 구조를 따라 작성해주세요:
                    
                    1. 사업 개요
                       - 사업의 배경 및 필요성
                       - 사업의 목표 및 범위
                       - 기대효과
                    
                    2. 기업 소개
                       - 기업 현황 및 연혁
                       - 조직 구성 및 인력 현황
                       - 주요 사업 분야 및 실적
                       - 기술력 및 경쟁력 분석
                    
                    3. 시장 분석
                       - 국내외 시장 동향
                       - 경쟁사 분석
                       - SWOT 분석
                    
                    4. 사업 내용
                       - 핵심 기술 소개
                       - 추진 전략 및 방법론
                       - 세부 추진 계획 및 일정
                       - 추진 체계
                    
                    5. 사업화 전략
                       - 마케팅 전략
                       - 판매 전략
                       - 해외 진출 전략 (해당 시)
                    
                    6. 소요 자금 계획
                       - 총 사업비 구성
                       - 연차별 자금 소요 계획
                       - 정부지원금 활용 계획
                    
                    7. 기대효과 및 성과지표
                       - 기술적 기대효과
                       - 경제적 기대효과
                       - 성과 측정 지표 및 방법
                    
                    8. 향후 발전 방향
                       - 중장기 발전 계획
                       - 후속 연구개발 계획
                    
                    각 항목을 상세히 작성하고, 공고 내용과 회사 정보를 적절히 연계하여 설득력 있는 사업계획서를 작성해주세요.
                    문서는 한글로 작성해주세요.
                    """
                    
                    with st.spinner("사업계획서 작성 중... (약 3-5분 소요됩니다)"):
                        try:
                            # 스트리밍 응답을 위한 빈 텍스트 공간 생성
                            response_placeholder = st.empty()
                            full_response = ""
                            
                            # Claude API를 사용하여 사업계획서 생성 (스트리밍 방식)
                            with client.messages.stream(
                                model=selected_model,
                                max_tokens=100000,
                                temperature=0.7,
                                messages=[
                                    {"role": "user", "content": prompt}
                                ]
                            ) as stream:
                                for text in stream.text_stream:
                                    full_response += text
                                    response_placeholder.markdown(full_response)
                            
                            # 결과 표시
                            st.subheader("📝 생성된 사업계획서")
                            st.markdown(full_response)
                            
                            # 다운로드 버튼 추가
                            st.download_button(
                                label="사업계획서 다운로드 (.txt)",
                                data=full_response,
                                file_name=f"{company_name}_사업계획서.txt",
                                mime="text/plain"
                            )
                            
                        except Exception as e:
                            st.error(f"사업계획서 생성 중 오류가 발생했습니다: {str(e)}")
                
    except Exception as e:
        st.error(f"API 연결 중 오류가 발생했습니다: {str(e)}")
