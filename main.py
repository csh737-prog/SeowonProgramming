import random
import os
import streamlit as st

st.set_page_config(
    page_title="너와 나의 유전자",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# 기본 설정
# -----------------------------
CHARACTERS = {
    "시우": {
        "role": "냉철한 천재 · 연구 동아리 부장",
        "color": "#8CB7D8",
        "intro": "무뚝뚝하지만 연구에 누구보다 진심인 동아리 부장.",
        "good_end": "시우는 네 연구 노트를 조심스럽게 덮었다. “너와 함께라면 어려운 연구도 즐거울 것 같아.” 두 사람은 서로를 가장 믿을 수 있는 연구 파트너이자 특별한 사람으로 받아들였다.",
        "bad_end": "연구 결과만 쫓던 두 사람은 서로의 마음을 제대로 전하지 못했다. 시우는 마지막 인사를 남기고 다른 연구 프로젝트에 참여하러 떠났다.",
    },
    "도윤": {
        "role": "다정한 소꿉친구 · 든든한 동료",
        "color": "#E5B27C",
        "intro": "늘 네 곁에서 응원해 주는 다정하고 밝은 친구.",
        "good_end": "도윤은 학교 정원에서 작은 꽃 한 송이를 건넸다. “사실 오래전부터 네가 좋았어.” 너는 웃으며 그의 손을 잡았다. 두 사람의 새로운 이야기가 시작됐다.",
        "bad_end": "도윤은 끝내 마음을 고백하지 못했다. 졸업식 날, 그는 평소처럼 웃으며 너를 응원했고, 말하지 못한 마음은 조용한 추억으로 남았다.",
    },
    "하린": {
        "role": "실력파 라이벌 · 전학생",
        "color": "#B8A0DE",
        "intro": "승부욕이 강하지만 함께 성장할 줄 아는 실력파 연구자.",
        "good_end": "하린은 연구 발표가 끝난 뒤 네게 손을 내밀었다. “이제 경쟁자 말고, 가장 가까운 편이 되어 줄래?” 라이벌로 시작된 관계는 누구보다 솔직한 사랑으로 이어졌다.",
        "bad_end": "하린은 네게 고개를 끄덕이며 다음에는 꼭 이기겠다고 말했다. 서로를 성장시킨 라이벌로 남았지만, 두 사람의 마음은 끝내 같은 곳에 닿지 못했다.",
    },
}

CHAPTERS = [
    {
        "day": "DAY 1 · 첫 만남",
        "title": "운명의 첫 만남",
        "scene": "방과 후, 처음으로 생명과학 연구 동아리실 문을 열었다. 창가에는 실험 도구가 놓여 있고 세 사람이 너를 바라본다.",
        "dialogues": [
            ("시우", "신입생? 생명공학에 관심이 있어서 온 건가?"),
            ("도윤", "어? 너도 여기 들어왔어? 같이 활동하면 재밌겠다!"),
            ("하린", "흥미롭네. 네가 얼마나 실력 있는지 한번 볼까?"),
        ],
        "choices": [
            ("시우에게 연구 실력으로 인정받고 싶다고 말한다.", "시우", 2),
            ("도윤에게 반갑게 인사하며 웃는다.", "도윤", 2),
            ("하린에게 자신 있게 도전장을 내민다.", "하린", 2),
        ],
    },
    {
        "day": "DAY 2 · 공동 연구",
        "title": "작은 실험, 커지는 마음",
        "scene": "동아리에서 식물 생장 데이터를 분석하게 됐다. 예상과 다른 결과가 나와 모두가 고민하는 순간, 네 선택이 필요하다.",
        "dialogues": [
            ("시우", "결과가 예상과 다르네. 측정 조건부터 다시 확인하자."),
            ("도윤", "괜찮아. 실수도 데이터야. 같이 원인을 찾아보자."),
            ("하린", "가설을 바꾸기 전에 근거를 더 모으는 게 좋겠어."),
        ],
        "choices": [
            ("측정값과 실험 조건을 꼼꼼히 다시 확인한다.", "시우", 2),
            ("팀원들을 격려하고 역할을 나눠 함께 분석한다.", "도윤", 2),
            ("다른 가능성을 세우고 추가 자료를 비교한다.", "하린", 2),
        ],
    },
    {
        "day": "DAY 3 · 진심",
        "title": "결과보다 중요한 것",
        "scene": "발표 전날, 늦은 시간까지 준비하던 너에게 한 사람이 다가온다. 평소와 달리 표정이 조금 진지하다.",
        "dialogues": [
            ("시우", "너랑 연구하면 나도 모르게 더 잘하고 싶어져."),
            ("도윤", "힘들면 꼭 말해. 네가 혼자 버티지 않았으면 좋겠어."),
            ("하린", "너를 경쟁자로만 생각했는데, 요즘은 그게 전부가 아닌 것 같아."),
        ],
        "choices": [
            ("시우에게 함께 연구할 때 믿음이 간다고 말한다.", "시우", 3),
            ("도윤에게 네가 곁에 있어 줘서 든든하다고 말한다.", "도윤", 3),
            ("하린에게 앞으로도 서로 솔직하게 경쟁하자고 말한다.", "하린", 3),
        ],
    },
]

def init_state():
    defaults = {
        "chapter": 0,
        "affection": {"시우": 0, "도윤": 0, "하린": 0},
        "history": [],
        "ending": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value.copy() if isinstance(value, dict) else value

def restart_game():
    for key in ["chapter", "affection", "history", "ending"]:
        if key in st.session_state:
            del st.session_state[key]
    init_state()

def character_card(name):
    c = CHARACTERS[name]
    score = st.session_state.affection[name]
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,{c['color']}33,#ffffff);
                    border:1px solid {c['color']};border-radius:16px;padding:14px;
                    margin-bottom:10px;">
            <div style="font-size:22px;font-weight:700;">{name}</div>
            <div style="font-size:13px;color:#555;margin:4px 0 10px;">{c['role']}</div>
            <div style="font-size:13px;">호감도 · {score}</div>
            <div style="height:8px;background:#e8e8e8;border-radius:10px;margin-top:6px;">
                <div style="height:8px;width:{min(score / 7 * 100, 100)}%;
                            background:{c['color']};border-radius:10px;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

init_state()

# -----------------------------
# 제목 / 소개
# -----------------------------
st.markdown(
    """
    <div style="padding:28px 24px;border-radius:20px;
                background:linear-gradient(120deg,#173f48,#466b7c,#9b91bd);
                color:white;margin-bottom:20px;">
      <div style="font-size:13px;letter-spacing:3px;">BIOLOGY · YOUTH · CHOICES</div>
      <h1 style="margin:8px 0 4px;">🧬 너와 나의 유전자</h1>
      <p style="margin:0;font-size:16px;">선택에 따라 달라지는 연구 동아리 로맨스</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if os.path.exists("assets/title_art.png"):
    st.image("assets/title_art.png", use_container_width=True)

st.write(
    "생명과학 연구 동아리에 들어온 당신. 세 명의 동료와 함께 연구하고 대화하며 "
    "관계를 쌓아 보세요. 선택에 따라 호감도가 달라지고, 마지막에는 서로 다른 엔딩을 맞이합니다."
)

st.subheader("💌 공략 캐릭터")
portrait_cols = st.columns(3)
for col, (name, filename) in zip(
    portrait_cols,
    [("시우", "char_siwoo.png"), ("도윤", "char_doyun.png"), ("하린", "char_harin.png")]
):
    with col:
        image_path = os.path.join("assets", filename)
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        st.markdown(f"**{name}**")
        st.caption(CHARACTERS[name]["role"])

with st.expander("게임 방법"):
    st.markdown(
        "- 각 장면을 읽고 가장 마음에 드는 선택지를 고르세요.\n"
        "- 선택한 인물의 호감도가 올라갑니다.\n"
        "- 3일의 이야기가 끝나면 호감도가 가장 높은 인물과 엔딩을 확인합니다.\n"
        "- 이 게임의 호감도는 게임 진행을 위한 가상 수치이며 실제 성격이나 생물학적 특성과는 관계가 없습니다."
    )

# -----------------------------
# 사이드바: 호감도 / 재시작
# -----------------------------
with st.sidebar:
    st.header("💗 관계 현황")
    for character in CHARACTERS:
        character_card(character)
    st.divider()
    if st.button("🔄 처음부터 다시 하기", use_container_width=True):
        restart_game()
        st.rerun()
    st.caption("Made with Python & Streamlit")

# -----------------------------
# 엔딩 화면
# -----------------------------
if st.session_state.ending:
    winner = st.session_state.ending
    score = st.session_state.affection[winner]
    st.balloons()
    st.markdown("---")
    st.subheader("✨ STORY END")
    st.title(f"{winner} 엔딩")
    st.markdown(f"**최종 호감도: {score}**")
    ending_image = os.path.join("assets", f"ending_{winner.lower()}.png")
    # 파일 이름은 캐릭터 이름에 맞춰 아래에서 안전하게 지정합니다.
    ending_files = {"시우": "ending_siwoo.png", "도윤": "ending_doyun.png", "하린": "ending_harin.png"}
    ending_image = os.path.join("assets", ending_files[winner])
    if os.path.exists(ending_image):
        st.image(ending_image, use_container_width=True)
    if score >= 5:
        st.success(CHARACTERS[winner]["good_end"])
        st.markdown("### 💗 해피 엔딩")
    else:
        st.info(CHARACTERS[winner]["bad_end"])
        st.markdown("### 🌙 아쉬운 엔딩")
    st.write("### 최종 호감도")
    st.bar_chart(st.session_state.affection)
    if st.button("다른 선택으로 다시 플레이하기", type="primary"):
        restart_game()
        st.rerun()
    st.stop()

# -----------------------------
# 현재 장면
# -----------------------------
chapter_index = st.session_state.chapter
if chapter_index >= len(CHAPTERS):
    max_score = max(st.session_state.affection.values())
    winners = [n for n, score in st.session_state.affection.items() if score == max_score]
    winner = random.choice(winners)
    st.session_state.ending = winner
    st.rerun()

chapter = CHAPTERS[chapter_index]
st.progress(chapter_index / len(CHAPTERS), text=f"스토리 진행도 · {chapter_index}/{len(CHAPTERS)}")
st.markdown(f"### {chapter['day']}")
st.header(chapter["title"])

scene_image = ["bg_school.png", "bg_lab.png", "bg_rooftop.png"][chapter_index]
scene_path = os.path.join("assets", scene_image)
if os.path.exists(scene_path):
    st.image(scene_path, use_container_width=True)

st.markdown(
    f"""
    <div style="background:#f5f2fa;border-left:5px solid #8b83b8;
                border-radius:10px;padding:18px;color:#292735;line-height:1.8;">
      {chapter['scene']}
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("#### 💬 동아리 친구들의 말")
for person, line in chapter["dialogues"]:
    st.markdown(f"**{person}**　{line}")

st.divider()
st.subheader("어떤 선택을 할까?")
st.caption("선택지는 해당 인물과의 호감도에 영향을 줍니다.")

choice_labels = [item[0] for item in chapter["choices"]]
selected = st.radio(
    "선택지를 하나 골라 줘.",
    choice_labels,
    index=None,
    key=f"choice_{chapter_index}",
    label_visibility="collapsed",
)

if st.button("선택 확정하기 💌", type="primary", use_container_width=True, disabled=selected is None):
    idx = choice_labels.index(selected)
    _, target, points = chapter["choices"][idx]
    st.session_state.affection[target] += points
    st.session_state.history.append(
        {"day": chapter["day"], "choice": selected, "target": target, "points": points}
    )
    st.session_state.chapter += 1
    if st.session_state.chapter >= len(CHAPTERS):
        max_score = max(st.session_state.affection.values())
        winners = [n for n, score in st.session_state.affection.items() if score == max_score]
        st.session_state.ending = random.choice(winners)
    st.rerun()

with st.expander("📖 지금까지의 선택 기록"):
    if st.session_state.history:
        for i, record in enumerate(st.session_state.history, 1):
            st.write(f"{i}. {record['day']} — {record['choice']} (+{record['points']} · {record['target']})")
    else:
        st.caption("아직 선택한 기록이 없습니다.")

st.caption("교육용 창작 게임입니다. 등장인물과 사건은 허구이며 실제 생명과학 연구 결과를 나타내지 않습니다.")
