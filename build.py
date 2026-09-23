# -*- coding: utf-8 -*-
import os
import json
import random

ROOT = os.path.dirname(os.path.abspath(__file__))

# =================================================================
# SITE CONFIG — 다른 지역으로 새 사이트를 만들 때는 이 블록만 바꾸면 됨
# (레포를 통째로 복사한 뒤 이 블록 + 학교 목록만 새 지역 것으로 교체하고
#  python build.py 실행하면 끝)
# =================================================================
REGION_SHORT = "거제"              # 지역 짧은 이름 (브랜드/카피에 사용)
REGION_FULL = "경남 거제시"         # 지역 정식 명칭 (breadcrumb 등에 사용)
BRAND = "티치핏" + REGION_SHORT     # 사이트 브랜드명 (필요하면 직접 다른 값으로 덮어써도 됨)
PHONE_DISPLAY = "010-3131-5305"
PHONE_TEL = "01031315305"
BASE_URL = "https://geoje.slovrest.com"   # 이 지역 사이트의 실제 도메인
LEAD_EMAIL = "ookkoo12@naver.com"   # 상담 신청 폼이 도착할 이메일 (FormSubmit 릴레이)
KAKAO_URL = "https://open.kakao.com/o/sCdocZOi"   # 카카오톡 오픈채팅 상담방
NAVER_VERIFICATION = ""  # 네이버 서치어드바이저 소유확인 (거제 서브도메인으로 등록 후 채워넣기)
GOOGLE_VERIFICATION = ""  # 구글 서치콘솔 소유확인 (등록 시 채워넣기)

# 학교 목록 — 시/군 교육지원청 공식 학교안내 기준으로 초/중/고 전체를 넣을 것
# (perfectedu 벤치마킹 원칙: 일부만 골라 넣지 않고 관할 전체를 포함 — 형평성 문제 방지)
# 출처: 경상남도거제교육지원청(gjedu.gne.go.kr) 학교안내, 2026-09-23 확인 (초41·중20·고11)
ELEMENTARY_NAMES = [
    "거제고현초등학교","거제상동초등학교","거제양정초등학교","거제용산초등학교","거제용소초등학교",
    "거제중앙초등학교","거제초등학교","계룡초등학교","국산초등학교","기성초등학교",
    "내곡초등학교","능포초등학교","대우초등학교","동부초등학교","동부초등학교 율포분교",
    "마전초등학교","명사초등학교","사등초등학교","삼룡초등학교","송정초등학교",
    "수월초등학교","숭덕초등학교","신현초등학교","아주초등학교","양지초등학교",
    "연초초등학교","오량초등학교","오비초등학교","옥포초등학교","외간초등학교",
    "외포초등학교","일운초등학교","장목초등학교","장승포초등학교","장평초등학교",
    "제산초등학교","중곡초등학교","진목초등학교","창호초등학교","칠천초등학교",
    "하청초등학교",
]
MIDDLE_NAMES = [
    "거제고현중학교","거제상문중학교","거제장평중학교","거제제일중학교","거제중앙중학교",
    "거제중학교","계룡중학교","동부중학교","둔덕중학교","성포중학교",
    "수월중학교","신현중학교","연초중학교","옥포성지중학교","옥포중학교",
    "외포중학교","장목예술중학교","지세포중학교","하청중학교","해성중학교",
]
HIGH_NAMES = [
    "거제고등학교","거제공업고등학교","거제상문고등학교","거제여자상업고등학교","거제옥포고등학교",
    "거제제일고등학교","거제중앙고등학교","경남산업고등학교","연초고등학교","장평고등학교",
    "해성고등학교",
]
# =================================================================
# CONFIG 끝 — 아래는 전부 재사용 가능한 공통 로직/템플릿
# =================================================================

def has_batchim(word):
    """단어 마지막 글자에 받침이 있는지 (한국어 조사 선택용)"""
    code = ord(word[-1]) - 0xAC00
    if 0 <= code <= 11171:
        return code % 28 != 0
    return False

def josa_eunneun(word):
    return word + ("은" if has_batchim(word) else "는")

def josa_irado(word):
    return word + ("이라도" if has_batchim(word) else "라도")

REGION_EUNNEUN = josa_eunneun(REGION_SHORT)
REGION_IRADO = josa_irado(REGION_SHORT)
BRAND_EUNNEUN = josa_eunneun(BRAND)

FONT_LINK = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap">'

NAV_ITEMS = [
    ("index.html", "홈"),
    ("teachers.html", "선생님"),
    ("regions.html", f"{REGION_SHORT} 학교검색"),
    ("blog.html", "블로그"),
]

def head(title, desc, path_prefix, canonical, noindex=False):
    robots_tag = '<meta name="robots" content="noindex,nofollow">\n' if noindex else ''
    verify_tags = ''
    if NAVER_VERIFICATION:
        verify_tags += '<meta name="naver-site-verification" content="{}">\n'.format(NAVER_VERIFICATION)
    if GOOGLE_VERIFICATION:
        verify_tags += '<meta name="google-site-verification" content="{}">\n'.format(GOOGLE_VERIFICATION)
    return '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/rss+xml" title="{brand} 블로그" href="{base}/rss.xml">
{verify}{robots}{font}
<link rel="stylesheet" href="{p}assets/style.css">
</head>
<body>
'''.format(title=title, desc=desc, canonical=canonical, font=FONT_LINK, p=path_prefix, robots=robots_tag, verify=verify_tags, brand=BRAND, base=BASE_URL)

def wave_strip():
    return '''<svg class="wave-strip" viewBox="0 0 200 7" preserveAspectRatio="none" aria-hidden="true">
  <path d="M0 3.5 Q 12.5 -0.5 25 3.5 T 50 3.5 T 75 3.5 T 100 3.5 T 125 3.5 T 150 3.5 T 175 3.5 T 200 3.5" fill="none" stroke="var(--primary)" stroke-width="2.4"/>
</svg>
'''

def topbar():
    return f'''<div class="topbar">
  <div class="wrap">
    <span>지금 신청하면 30분 무료체험수업부터 받아보실 수 있어요</span>
    <a class="phone" href="tel:{PHONE_TEL}">\U0001F4DE {PHONE_DISPLAY} (09:00–21:00)</a>
  </div>
</div>
'''

def header(path_prefix, active):
    links = []
    mlinks = []
    for href, label in NAV_ITEMS:
        cur = ' aria-current="page"' if href == active else ''
        links.append('<a href="{p}{href}"{cur}>{label}</a>'.format(p=path_prefix, href=href, cur=cur, label=label))
        mlinks.append('<a href="{p}{href}"{cur}>{label}</a>'.format(p=path_prefix, href=href, cur=cur, label=label))
    return '''<header class="site">
  <div class="wrap">
    <a class="logo" href="{p}index.html"><span class="mark">TF</span>{brand}</a>
    <div class="navwrap">
      <nav class="main">
        {links}
      </nav>
      <a class="cta-btn" href="{p}apply.html">무료 상담 신청</a>
      <button class="menu-btn" aria-label="메뉴">☰</button>
    </div>
  </div>
  <div class="mobile-nav-wrap">
    <nav class="mobile-nav">
      {mlinks}
      <a href="{p}apply.html">무료 상담 신청</a>
    </nav>
  </div>
</header>
'''.format(p=path_prefix, brand=BRAND, links='\n        '.join(links), mlinks='\n      '.join(mlinks))

def kakao_fab():
    return f'''<a class="kakao-fab" href="{KAKAO_URL}" target="_blank" rel="noopener">
  <span class="kakao-fab-ico">\U0001F4AC</span><span class="kakao-fab-label">카톡 상담</span>
</a>
'''

def mobile_cta_bar(path_prefix):
    return f'''<div class="mobile-cta-bar">
  <a class="msc-call" href="tel:{PHONE_TEL}">\U0001F4DE 전화상담</a>
  <a class="msc-apply" href="{path_prefix}apply.html">무료 상담 신청</a>
</div>
'''

def footer(path_prefix):
    return '''<footer>
  <div class="wrap">
    <div>
      <a class="logo" href="{p}index.html" style="margin-bottom:10px;"><span class="mark">TF</span>{brand}</a>
      <div class="fnav">
        <a href="{p}services.html">화상과외 소개</a><a href="{p}process.html">매칭 방식</a><a href="{p}teachers.html">선생님</a><a href="{p}regions.html">{region} 학교검색</a><a href="{p}blog.html">블로그</a>
      </div>
      <p class="disclaimer">전화 {phone} · 운영시간 09:00–21:00 · 상담 및 매칭 신청은 무료이며, 실제 수업 진행 여부와 비용은 상담 후 안내해 드립니다. 사업자 정보는 확정 후 별도 고지 예정입니다.</p>
    </div>
  </div>
</footer>
<script src="{p}assets/site.js"></script>
</body>
</html>
'''.format(p=path_prefix, brand=BRAND, region=REGION_SHORT, phone=PHONE_DISPLAY)

def page(filename, title, desc, active, body, path_prefix="", canonical="", noindex=False, extra_js=""):
    full = head(title, desc, path_prefix, canonical, noindex) + wave_strip() + topbar() + header(path_prefix, active) + '<main class="wrap">\n' + body + '\n</main>\n' + footer(path_prefix)
    full = full.replace('</body>', kakao_fab() + '\n</body>')
    if os.path.basename(filename) not in ("apply.html", "thanks.html"):
        full = full.replace('</body>', mobile_cta_bar(path_prefix) + '\n</body>')
    if extra_js:
        full = full.replace('</body>', extra_js + '\n</body>')
    out_path = os.path.join(ROOT, filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full)
    print("wrote", filename)

# ---------------------------------------------------------------
# Revised Romanization (approximate, URL-slug purposes only)
# ---------------------------------------------------------------
CHO = ['g','kk','n','d','tt','r','m','b','pp','s','ss','','j','jj','ch','k','t','p','h']
JUNG = ['a','ae','ya','yae','eo','e','yeo','ye','o','wa','wae','oe','yo','u','wo','we','wi','yu','eu','ui','i']
JONG = ['','g','kk','gs','n','nj','nh','d','l','lg','lm','lb','ls','lt','lp','lh','m','b','bs','s','ss','ng','j','ch','k','t','p','h']

def romanize(text):
    out = []
    for ch in text:
        code = ord(ch) - 0xAC00
        if 0 <= code < 11172:
            cho = code // 588
            jung = (code % 588) // 28
            jong = code % 28
            out.append(CHO[cho] + JUNG[jung] + JONG[jong])
        elif ch.isalnum():
            out.append(ch.lower())
    return ''.join(out)

REGION_SLUG = romanize(REGION_SHORT)  # 예: 군산 -> gunsan (슬러그 접미사로 사용)

def josa_eun_neun(word):
    """받침 유무에 따라 '은'/'는' 중 맞는 조사를 반환 (BRAND가 지역마다 달라져도 문법 맞게)."""
    if not word:
        return "는"
    code = ord(word[-1]) - 0xAC00
    if 0 <= code < 11172:
        return "은" if (code % 28) != 0 else "는"
    return "는"

BRAND_EUN = josa_eun_neun(BRAND)

def sample_keyword(name):
    """검색창 placeholder용 짧은 예시 키워드 — 지역명 접두어·학교급 접미어를 뗀 나머지."""
    base = name.replace('초등학교', '').replace('중학교', '').replace('고등학교', '')
    if base.startswith(REGION_SHORT) and len(base) > len(REGION_SHORT):
        base = base[len(REGION_SHORT):]
    return base[:3] if base else name[:2]

LEVEL_CODE = {'초등학교': 'es', '중학교': 'ms', '고등학교': 'hs'}

def make_slug(name, level, used):
    base = name.replace('초등학교', '').replace('중학교', '').replace('고등학교', '')
    slug = '{}-{}-{}'.format(romanize(base), LEVEL_CODE[level], REGION_SLUG)
    if slug in used:
        n = 2
        while '{}-{}'.format(slug, n) in used:
            n += 1
        slug = '{}-{}'.format(slug, n)
    used.add(slug)
    return slug

_used_slugs = set()
def build_school_list(names, level):
    out = []
    for name in names:
        out.append({"name": name, "level": level, "slug": make_slug(name, level, _used_slugs)})
    return out

SCHOOLS = (
    build_school_list(ELEMENTARY_NAMES, "초등학교")
    + build_school_list(MIDDLE_NAMES, "중학교")
    + build_school_list(HIGH_NAMES, "고등학교")
)

LEVEL_INFO = {
    "초등학교": {
        "stage": "초등학생",
        "focus": "읽기·쓰기·연산 기초와 학습 습관 형성",
        "subjects": ["국어", "영어", "수학"],
        "worry": "아직 공부 습관이 안 잡혀서 무엇부터 시작해야 할지 모르겠다는 점",
    },
    "중학교": {
        "stage": "중학생",
        "focus": "내신 시험 범위에 맞춘 단원별 학습과 기초 개념 보완",
        "subjects": ["국어", "영어", "수학", "사회", "과학"],
        "worry": "시험 범위는 아는데 어디서부터 정리해야 할지 막막하다는 점",
    },
    "고등학교": {
        "stage": "고등학생",
        "focus": "내신 등급 관리와 수능 대비 학습",
        "subjects": ["국어", "영어", "수학", "사회", "과학"],
        "worry": "내신과 수능을 동시에 챙기기엔 시간이 부족하다는 점",
    },
}

# ---------------------------------------------------------------
# index.html
# ---------------------------------------------------------------
index_body = f'''
<section class="hero">
  <div class="grid">
    <div>
      <span class="eyebrow">{REGION_SHORT} 과외</span>
      <h1>{REGION_SHORT} 과외 찾고 계신가요?<br>초·중·고 1:1 <em>화상과외</em></h1>
      <p class="lead">수학·영어·국어 등 전 과목, 초등학생부터 고등학생까지 — {REGION_SHORT} 학교 사정을 잘 아는 선생님을 실시간 화상 수업으로 연결해 드려요. 방문 없이도 집에서 편하게 받을 수 있어요.</p>
      <div class="hero-ctas">
        <a class="cta-btn" href="apply.html">30분 무료체험 신청하기</a>
        <a class="cta-ghost" href="process.html">매칭 방식 보기</a>
      </div>
      <div class="trust-row">
        <span><i class="dot"></i>{REGION_SHORT} 학교 사정에 밝은 선생님</span>
        <span><i class="dot"></i>30분 무료체험수업 먼저 받아보기</span>
        <span><i class="dot"></i>체험 후 결정, 부담 없어요</span>
      </div>
    </div>
    <div>
      <svg viewBox="0 0 300 300" fill="none" style="max-width:380px;margin-inline:auto;display:block;">
        <circle cx="150" cy="150" r="128" stroke="var(--line)" stroke-width="1.5" stroke-dasharray="2 8"/>
        <path d="M95 150a55 55 0 1 1 110 0 55 55 0 0 1-110 0Z" fill="var(--primary-soft)"/>
        <path d="M150 95a55 55 0 0 1 47.5 82.5L150 150Z" fill="var(--accent-soft)"/>
        <circle cx="150" cy="150" r="55" fill="none" stroke="var(--primary)" stroke-width="2.5"/>
        <line x1="150" y1="70" x2="150" y2="88" stroke="var(--muted-2)" stroke-width="2"/>
        <line x1="150" y1="212" x2="150" y2="230" stroke="var(--muted-2)" stroke-width="2"/>
        <line x1="70" y1="150" x2="88" y2="150" stroke="var(--muted-2)" stroke-width="2"/>
        <line x1="212" y1="150" x2="230" y2="150" stroke="var(--muted-2)" stroke-width="2"/>
        <path d="M150 106 L164 150 L150 150 Z" fill="var(--primary-strong)"/>
        <path d="M150 106 L136 150 L150 150 Z" fill="var(--primary)"/>
        <path d="M150 194 L164 150 L150 150 Z" fill="var(--accent-strong)"/>
        <path d="M150 194 L136 150 L150 150 Z" fill="var(--accent)"/>
        <circle cx="150" cy="150" r="7" fill="var(--ink)"/>
      </svg>
    </div>
  </div>
</section>

<div class="stats">
  <div class="wrap">
    <div><div class="num mono">{len(SCHOOLS)}개교</div><div class="lbl">{REGION_SHORT} 전체 초·중·고 매칭 가능</div></div>
    <div><div class="num mono">4단계</div><div class="lbl">선생님 검증 절차</div></div>
    <div><div class="num mono">30분</div><div class="lbl">무료체험수업 제공</div></div>
    <div><div class="num mono">24h</div><div class="lbl">이내 매칭 안내</div></div>
  </div>
</div>

<section id="grades">
  <div class="head-row">
    <div><span class="eyebrow">학년별 과외</span><h2>학년마다 필요한 과외가 달라요</h2></div>
    <p>같은 {REGION_IRADO} 초등·중등·고등에 따라 고민이 다르니, 학년에 맞춰 과목과 방식을 정해드려요.</p>
  </div>
  <div class="services">
    <div class="svc-card">
      <span class="tag">초등</span>
      <h3>{REGION_SHORT} 초등학생 화상과외</h3>
      <p>국어·영어·수학 기초를 다지고 학습 습관을 잡아주는 시기예요. 놀이처럼 부담 없이 시작할 수 있게 진행해요.</p>
      <div class="subjects"><span>국어</span><span>영어</span><span>수학</span></div>
    </div>
    <div class="svc-card">
      <span class="tag">중등</span>
      <h3>{REGION_SHORT} 중학생 수학·영어 화상과외</h3>
      <p>내신 시험 범위에 맞춘 단원별 학습이 중요해지는 시기예요. 학교별 시험 유형을 반영해 대비해요.</p>
      <div class="subjects"><span>수학</span><span>영어</span><span>국어</span><span>사회</span><span>과학</span></div>
    </div>
    <div class="svc-card">
      <span class="tag">고등</span>
      <h3>{REGION_SHORT} 고등학생 내신·수능 화상과외</h3>
      <p>내신 등급 관리와 수능 대비를 함께 챙겨야 하는 시기예요. 목표에 맞춰 커리큘럼을 조정해요.</p>
      <div class="subjects"><span>수학</span><span>영어</span><span>국어</span><span>사회</span><span>과학</span></div>
    </div>
  </div>
</section>

<section id="services">
  <div class="head-row">
    <div><span class="eyebrow">서비스</span><h2>왜 화상과외 하나에만 집중할까요</h2></div>
    <p>방문 선생님을 구하기 어려운 과목도, 화상이라면 훨씬 넓은 범위에서 {REGION_SHORT} 학생에게 맞는 선생님을 찾을 수 있어요.</p>
  </div>
  <div class="services">
    <div class="svc-card">
      <span class="tag">실시간 화상</span>
      <h3>1:1 실시간 화상 수업</h3>
      <p>정해진 시간에 화면으로 만나 실시간으로 진행하는 수업이에요. 이동 시간이 없어 저녁 시간대도 유연하게 잡을 수 있어요.</p>
      <div class="subjects"><span>국어</span><span>영어</span><span>수학</span><span>사회</span><span>과학</span></div>
    </div>
    <div class="svc-card">
      <span class="tag">녹화 복습</span>
      <h3>수업 녹화 다시보기</h3>
      <p>수업 내용을 녹화해 두고 이해가 안 된 부분만 다시 돌려볼 수 있어요. 시험 전 복습에 특히 도움이 돼요.</p>
      <div class="subjects"><span>단원별 복습</span><span>오답 다시보기</span></div>
    </div>
    <div class="svc-card">
      <span class="tag">지역 맞춤</span>
      <h3>{REGION_SHORT} 학교 사정을 아는 선생님</h3>
      <p>같은 화상 수업이라도 {REGION_SHORT} 학교의 시험 범위와 분위기를 아는 선생님과 하면 훨씬 정확해요. 상담 시 재학 중인 학교를 확인해 매칭에 반영합니다.</p>
      <div class="subjects"><span>학교별 내신</span><span>지역 맞춤 매칭</span></div>
    </div>
  </div>
</section>

<section id="cost-vs-visit">
  <div class="head-row"><div><span class="eyebrow">궁금한 점</span><h2>{REGION_SHORT} 과외 비용, 방문과 화상 뭐가 다를까요</h2></div></div>
  <div class="trust-grid" style="grid-template-columns:repeat(2,1fr);">
    <div class="trust-item"><h4>{REGION_SHORT} 과외 비용은 어떻게 결정될까요</h4><p>과목·학년·수업 시간, 선생님 경력에 따라 달라져요. 정확한 비용은 상담 시 학생 상황을 확인한 뒤 안내해 드리고, 30분 무료체험수업으로 먼저 확인하실 수 있어요.</p></div>
    <div class="trust-item"><h4>방문과외와 화상과외의 차이</h4><p>방문은 대면 관리가 필요한 학생에게, 화상은 이동 시간 없이 원하는 시간대에 넓은 범위의 선생님을 찾고 싶은 학생에게 잘 맞아요. {BRAND_EUNNEUN} 화상과외 하나에 집중해 매칭 정확도를 높였어요.</p></div>
  </div>
</section>

<section id="process">
  <div class="head-row">
    <div><span class="eyebrow">매칭 방식</span><h2>우리 아이에게 맞는 선생님 찾는 방법</h2></div>
    <p>진단 없이 배정하지 않습니다. 학습 성향과 생활 패턴까지 확인한 뒤 선생님을 연결해요.</p>
  </div>
  <div class="process-track">
    <div class="p-step"><div class="n">01</div><h4>학습 진단</h4><p>현재 수준과 약점, 학습 성향을 먼저 파악해요.</p></div>
    <div class="p-step"><div class="n">02</div><h4>맞춤 설계</h4><p>목표와 생활 패턴에 맞춘 1:1 커리큘럼을 구성해요.</p></div>
    <div class="p-step"><div class="n">03</div><h4>30분 무료체험수업</h4><p>선생님과 화면으로 만나 30분 동안 무료로 먼저 받아보고 궁합을 확인해요.</p></div>
    <div class="p-step"><div class="n">04</div><h4>숙제·오답 관리</h4><p>배운 내용을 확실히 내 것으로 만들어요.</p></div>
    <div class="p-step"><div class="n">05</div><h4>리포트·피드백</h4><p>진행 상황을 학부모님께 정기 공유해요.</p></div>
  </div>
</section>

<section>
  <div class="head-row"><div><span class="eyebrow">왜 {BRAND}인가</span><h2>믿고 맡길 수 있는 이유</h2></div></div>
  <div class="trust-grid">
    <div class="trust-item"><div class="ico">\U0001F6E1️</div><h4>철저한 검증</h4><p>학력·신원·경력을 확인한 선생님만 매칭에 참여해요.</p></div>
    <div class="trust-item"><div class="ico">\U0001F9ED</div><h4>궁합 기반 매칭</h4><p>성적만이 아니라 성향·목표까지 분석해 연결해요.</p></div>
    <div class="trust-item"><div class="ico">\U0001F3AC</div><h4>30분 무료체험수업</h4><p>정식 신청 전에 30분 동안 선생님과 무료로 먼저 만나보고 결정할 수 있어요.</p></div>
    <div class="trust-item"><div class="ico">\U0001F4CB</div><h4>꼼꼼한 학습 관리</h4><p>수업 리포트와 진도 관리로 흐름을 놓치지 않아요.</p></div>
    <div class="trust-item"><div class="ico">⏱️</div><h4>빠른 응대</h4><p>신청 후 24시간 이내 체험 수업을 안내해 드려요.</p></div>
  </div>
</section>

<section id="regions">
  <div class="head-row">
    <div><span class="eyebrow">{REGION_SHORT} 학교검색</span><h2>초등학교부터 고등학교까지, {REGION_SHORT} 학교 {len(SCHOOLS)}곳 모두</h2></div>
  </div>
  <div class="region-card" style="max-width:640px;">
    <div class="count">초등학교 {len(ELEMENTARY_NAMES)}곳 · 중학교 {len(MIDDLE_NAMES)}곳 · 고등학교 {len(HIGH_NAMES)}곳 — 어느 학교든 화상과외 매칭이 가능해요.</div>
    <div style="margin-top:16px;"><a class="cta-btn" href="regions.html">우리 학교 검색해보기 →</a></div>
  </div>
</section>

<section id="apply">
  <div class="apply-wrap">
    <div>
      <span class="eyebrow" style="color:var(--accent-strong)">무료 상담</span>
      <h2>지금 우리 아이 학습 궁합을 확인해보세요</h2>
      <p>이름과 연락처만 남겨주시면 24시간 이내에 담당자가 직접 연락드려요.</p>
      <ul class="apply-perks">
        <li>상담·매칭 신청 전 과정 무료</li>
        <li>검증된 선생님만 매칭에 참여</li>
        <li>30분 무료체험수업 먼저 받아보고 결정</li>
      </ul>
    </div>
    {{apply_form}}
  </div>
</section>
'''

APPLY_FORM = f'''<form class="form-card" action="https://formsubmit.co/{LEAD_EMAIL}" method="POST">
      <input type="hidden" name="_subject" value="[{BRAND}] 새 상담 신청">
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_next" value="thanks.html">
      <div class="field"><label for="tf-name">이름</label><input id="tf-name" name="이름" type="text" placeholder="학부모님 성함" required></div>
      <div class="field"><label for="tf-phone">연락처</label><input id="tf-phone" name="연락처" type="tel" placeholder="010-0000-0000" required></div>
      <div class="field"><label for="tf-school">재학 중인 학교 ({REGION_SHORT} 소재)</label><input id="tf-school" name="학교" type="text" placeholder="예: {next((s['name'] for s in SCHOOLS if s['level'] == '중학교'), SCHOOLS[0]['name'] if SCHOOLS else '')}"></div>
      <div class="field">
        <label>학년</label>
        <div class="radio-row">
          <label><input type="radio" name="학년" value="초등">초등</label>
          <label><input type="radio" name="학년" value="중등">중등</label>
          <label><input type="radio" name="학년" value="고등">고등</label>
        </div>
      </div>
      <div class="field"><label for="tf-memo">남기실 말 (선택)</label><textarea id="tf-memo" name="메모" rows="2" placeholder="희망 과목, 시간대 등"></textarea></div>
      <button class="submit-btn" type="submit">무료 상담 신청하기</button>
      <p class="form-note">신청 즉시 담당자에게 전달되며, 24시간 이내 연락드립니다.</p>
    </form>'''

index_body = index_body.format(apply_form=APPLY_FORM)

# ---------------------------------------------------------------
# services.html / process.html / teachers.html
# ---------------------------------------------------------------
services_body = f'''
<section class="page-hero">
  <span class="eyebrow">화상과외 소개</span>
  <h1>{REGION_SHORT} 학생을 위한 화상과외, 이렇게 다릅니다</h1>
  <p>{BRAND}{BRAND_EUN} 방문 수업이나 입시 컨설팅 없이, 오직 화상과외 하나에만 집중합니다. 대신 그 안에서 {REGION_SHORT} 지역 학교 사정까지 반영한 매칭을 제공해요.</p>
</section>
<section>
  <div class="services">
    <div class="svc-card">
      <span class="tag">실시간 화상</span>
      <h3>1:1 실시간 화상 수업</h3>
      <p>정해진 시간에 화면으로 만나 실시간으로 진행돼요. 선생님이 이동할 필요가 없어 저녁·주말 등 원하는 시간대를 잡기가 더 쉽고, {REGION_SHORT} 안에서 구하기 어려운 과목·스타일의 선생님도 연결할 수 있어요.</p>
      <div class="subjects"><span>국어</span><span>영어</span><span>수학</span><span>사회</span><span>과학</span></div>
    </div>
    <div class="svc-card">
      <span class="tag">녹화 복습</span>
      <h3>수업 녹화로 다시 보는 복습</h3>
      <p>매 수업을 녹화해 두기 때문에, 이해가 덜 된 부분만 골라 다시 볼 수 있어요. 시험 기간 벼락치기 복습에도, 결석했을 때 따라잡기에도 유용해요.</p>
      <div class="subjects"><span>단원별 복습</span><span>오답 다시보기</span></div>
    </div>
    <div class="svc-card">
      <span class="tag">지역 맞춤</span>
      <h3>{REGION_SHORT} 학교 사정을 아는 선생님</h3>
      <p>같은 화상 수업이라도 학교별 시험 범위와 난이도를 아는 선생님과 하면 훨씬 정확해요. 상담 시 재학 중인 학교를 먼저 확인하고, 그 학교 학생을 지도한 경험이 있는 선생님 위주로 매칭합니다.</p>
      <div class="subjects"><span>학교별 내신</span><span>지역 맞춤 매칭</span></div>
    </div>
  </div>
</section>
<section>
  <div class="head-row"><div><span class="eyebrow">방문 수업이 필요하시다면</span><h2>화상으로 먼저 경험해보세요</h2></div></div>
  <div class="apply-wrap" style="grid-template-columns:1fr;">
    <div>
      <p style="color:#DCEEE8;">{BRAND}{BRAND_EUN} 현재 화상과외 하나에만 집중하고 있어요. 방문 수업이 꼭 필요한 경우라면 상담 시 말씀해 주세요 — 상황에 따라 안내해 드릴 수 있는 방법을 함께 찾아볼게요.</p>
      <div style="margin-top:18px;"><a class="cta-btn" href="apply.html" style="background:var(--accent);color:var(--primary-strong)!important;">무료 상담 신청하기</a></div>
    </div>
  </div>
</section>
'''

process_body = '''
<section class="page-hero">
  <span class="eyebrow">매칭 방식</span>
  <h1>성적이 오르는 5단계 관리 시스템</h1>
  <p>진단 없이 곧바로 선생님을 배정하지 않아요. 아이의 학습 상태를 먼저 확인하고, 그 다음 순서로 매칭과 관리가 이어집니다.</p>
</section>
<section>
  <div class="process-track">
    <div class="p-step"><div class="n">01</div><h4>학습 진단</h4><p>현재 수준·약점을 정확히 파악합니다. 최근 시험 결과와 학습 습관을 함께 확인해요.</p></div>
    <div class="p-step"><div class="n">02</div><h4>맞춤 설계</h4><p>목표에 맞춘 1:1 커리큘럼을 만듭니다. 단기 내신 대비인지 장기 실력 향상인지에 따라 설계가 달라져요.</p></div>
    <div class="p-step"><div class="n">03</div><h4>30분 무료체험수업</h4><p>정해진 시간에 화면으로 만나 30분 동안 무료로 먼저 수업을 받아봐요. 이 시간으로 선생님과의 궁합을 확인해요.</p></div>
    <div class="p-step"><div class="n">04</div><h4>숙제·오답 관리</h4><p>정식 수업을 시작하면 배운 내용을 확실히 내 것으로 만듭니다. 오답 노트와 복습 계획을 함께 챙겨요.</p></div>
    <div class="p-step"><div class="n">05</div><h4>리포트·피드백</h4><p>진행 상황을 학부모님께 정기적으로 공유합니다. 필요하면 커리큘럼을 다시 조정해요.</p></div>
  </div>
</section>
<section>
  <div class="head-row"><div><span class="eyebrow">한 가지 더</span><h2>결제는 체험 수업 다음에 결정하세요</h2></div></div>
  <div class="trust-grid" style="grid-template-columns:repeat(2,1fr);">
    <div class="trust-item"><div class="ico">\U0001F3AC</div><h4>30분 무료체험수업</h4><p>정식 신청 전에 선생님과 30분 동안 무료로 먼저 만나볼 수 있어요. 궁합이 어떤지 직접 확인해보세요.</p></div>
    <div class="trust-item"><div class="ico">\U0001F4AC</div><h4>체험 후 자유롭게 결정</h4><p>체험 수업이 마음에 들 때만 정식으로 시작하시면 돼요. 부담 갖지 않으셔도 됩니다.</p></div>
  </div>
</section>
'''

# ---------------------------------------------------------------
# 선생님 풀 — 실제 보유 선생님 규모(600명+)를 반영한 예시 데이터
# (개인정보 보호를 위해 이름은 성만 표시. 실제 매칭 시 정확한 프로필은 상담 후 안내)
# ---------------------------------------------------------------
TEACHER_POOL_SIZE = 614

def generate_teacher_pool(n, seed_key):
    rnd = random.Random(1000 + sum(ord(c) for c in seed_key))
    surnames = ["김","이","박","최","정","강","조","윤","장","임","한","오","서","신","권","황","안","송","전","홍","고","문","양","손","배","백","허","유","남","심"]
    unis = ["서울대","연세대","고려대","이화여대","한국외대","성균관대","한양대","경상국립대","창원대","부산대","전남대","충남대"]
    subj_weights = [("수학",34), ("영어",26), ("국어",16), ("과학",14), ("사회",10)]
    subj_pool = [s for s, w in subj_weights for _ in range(w)]

    def pick_subjects():
        r = rnd.random()
        if r < 0.06:
            return ["국어", "영어", "수학", "사회", "과학"]
        if r < 0.22:
            first = rnd.choice(subj_pool)
            second = rnd.choice([s for s in ["국어","영어","수학","사회","과학"] if s != first])
            return [first, second]
        return [rnd.choice(subj_pool)]

    def pick_levels():
        r = rnd.random()
        if r < 0.22:
            return ["초등"]
        if r < 0.40:
            return ["중등"]
        if r < 0.55:
            return ["고등"]
        if r < 0.72:
            return ["초등", "중등"]
        if r < 0.88:
            return ["중등", "고등"]
        return ["초등", "중등", "고등"]

    range_by_levels = {
        ("초등",): ["초1~초6", "초2~초6", "초3~초6"],
        ("중등",): ["중1~중3"],
        ("고등",): ["고1~고3"],
        ("초등", "중등"): ["초4~중3", "초1~중3"],
        ("중등", "고등"): ["중1~고3", "중2~고3"],
        ("초등", "중등", "고등"): ["초1~고3"],
    }

    def make_tag(subjects, levels):
        subj_label = "전과목" if len(subjects) >= 4 else "·".join(subjects)
        r = rnd.random()
        if r < 0.32:
            return f"{rnd.choice(unis)} 출신 {subj_label} 화상과외"
        if r < 0.58:
            return f"교습경력 {rnd.randint(3,14)}년차 {subj_label} 화상과외"
        return f"{subj_label} 화상과외"

    pool = []
    for i in range(n):
        surname = rnd.choice(surnames)
        gender = "여" if rnd.random() < 0.58 else "남"
        subjects = pick_subjects()
        levels = pick_levels()
        grade_range = rnd.choice(range_by_levels[tuple(levels)])
        pool.append({
            "name": f"{surname}OO 선생님",
            "avatar": surname,
            "g": gender,
            "s": subjects,
            "lv": levels,
            "gr": grade_range,
            "tag": make_tag(subjects, levels),
            "fit": rnd.randint(84, 98),
        })
    return pool

TEACHER_POOL = generate_teacher_pool(TEACHER_POOL_SIZE, REGION_SLUG)

teachers_body = f'''
<section class="page-hero">
  <span class="eyebrow">선생님</span>
  <h1>검증된 선생님만 매칭에 참여합니다</h1>
  <p>학력·신원·경력 확인을 거치고, {REGION_SHORT} 학생 지도 경험이 있거나 {REGION_SHORT} 학교 사정을 파악한 선생님 위주로 화상과외를 안내해 드려요.</p>
</section>
<div class="stats" style="margin-bottom:52px;">
  <div class="wrap" style="grid-template-columns:repeat(3,1fr);">
    <div><div class="num mono">600명+</div><div class="lbl">전국 화상과외 선생님 풀</div></div>
    <div><div class="num mono">5과목</div><div class="lbl">국어·영어·수학·사회·과학</div></div>
    <div><div class="num mono">4단계</div><div class="lbl">등록 전 검증 절차</div></div>
  </div>
</div>
<section>
  <div class="head-row"><div><span class="eyebrow">검증 절차</span><h2>선생님 등록 전 4단계 확인</h2></div></div>
  <div class="trust-grid" style="grid-template-columns:repeat(2,1fr);">
    <div class="trust-item"><div class="ico">\U0001F4C4</div><h4>학력 확인</h4><p>졸업증명 등 학력 서류를 확인합니다.</p></div>
    <div class="trust-item"><div class="ico">\U0001F194</div><h4>신원 확인</h4><p>본인 확인 및 신원 정보를 검증합니다.</p></div>
    <div class="trust-item"><div class="ico">\U0001F4BC</div><h4>경력 확인</h4><p>과외·강의 경력을 확인하고 전공·지도 과목을 매칭합니다.</p></div>
    <div class="trust-item"><div class="ico">\U0001F4DE</div><h4>사전 인터뷰</h4><p>화상 수업 방식과 성향을 미리 확인해 학생과의 궁합을 예측합니다.</p></div>
  </div>
</section>
<section id="teachers">
  <div class="head-row"><div><span class="eyebrow">선생님 찾기</span><h2>조건에 맞는 선생님을 미리 둘러보세요</h2></div></div>
  <p class="sample-note"><span class="badge">예시</span>아래 프로필은 실제 보유 선생님 풀 규모에 맞춘 예시 카드예요. 선생님 성함은 개인정보 보호를 위해 성만 표시하고, 정확한 프로필은 상담 신청 후 안내해 드려요.</p>
  <div class="teacher-filter">
    <div class="field">
      <label>과목</label>
      <div class="radio-row" id="f-subject">
        <label><input type="radio" name="f-subject" value="전체" checked> 전체</label>
        <label><input type="radio" name="f-subject" value="국어"> 국어</label>
        <label><input type="radio" name="f-subject" value="영어"> 영어</label>
        <label><input type="radio" name="f-subject" value="수학"> 수학</label>
        <label><input type="radio" name="f-subject" value="사회"> 사회</label>
        <label><input type="radio" name="f-subject" value="과학"> 과학</label>
      </div>
    </div>
    <div class="field">
      <label>학년</label>
      <div class="radio-row" id="f-level">
        <label><input type="radio" name="f-level" value="전체" checked> 전체</label>
        <label><input type="radio" name="f-level" value="초등"> 초등</label>
        <label><input type="radio" name="f-level" value="중등"> 중등</label>
        <label><input type="radio" name="f-level" value="고등"> 고등</label>
      </div>
    </div>
    <div class="field">
      <label>성별</label>
      <div class="radio-row" id="f-gender">
        <label><input type="radio" name="f-gender" value="전체" checked> 전체</label>
        <label><input type="radio" name="f-gender" value="여"> 여</label>
        <label><input type="radio" name="f-gender" value="남"> 남</label>
      </div>
    </div>
  </div>
  <p class="sample-note" style="margin-top:18px;"><span class="badge mono" id="match-count">-</span><span id="match-label">조건에 맞는 선생님이 있어요</span></p>
  <div class="teachers" id="teacher-results"></div>
  <p style="margin-top:22px;"><a class="cta-btn" href="apply.html">이 조건으로 무료 상담 신청하기</a></p>
</section>
'''

teachers_js = '''<script>window.TEACHER_POOL=''' + json.dumps(TEACHER_POOL, ensure_ascii=False) + ''';</script>
<script>
(function(){
  var pool = window.TEACHER_POOL || [];
  var results = document.getElementById('teacher-results');
  var countEl = document.getElementById('match-count');
  var labelEl = document.getElementById('match-label');
  if(!results) return;

  function cardHtml(t){
    return '<div class="t-card"><div class="avatar">' + t.avatar + '</div><h4>' + t.name + '</h4>' +
      '<div class="meta">' + t.s.join('·') + ' · ' + t.gr + ' · ' + t.g + ' · ' + t.tag + '</div>' +
      '<div class="fit-score">예상 궁합도 <b class="mono">' + t.fit + '%</b></div></div>';
  }

  function currentFilter(name){
    var checked = document.querySelector('input[name="' + name + '"]:checked');
    return checked ? checked.value : '전체';
  }

  function render(){
    var subject = currentFilter('f-subject');
    var level = currentFilter('f-level');
    var gender = currentFilter('f-gender');
    var matched = pool.filter(function(t){
      if(subject !== '전체' && t.s.indexOf(subject) === -1) return false;
      if(level !== '전체' && t.lv.indexOf(level) === -1) return false;
      if(gender !== '전체' && t.g !== gender) return false;
      return true;
    });
    var shown = matched.slice(0, 9);
    results.innerHTML = shown.map(cardHtml).join('');
    countEl.textContent = matched.length + '명';
    labelEl.textContent = matched.length > shown.length
      ? '조건에 맞는 선생님이 있어요 (인기 ' + shown.length + '명 우선 표시)'
      : '조건에 맞는 선생님이 있어요';
  }

  ['f-subject','f-level','f-gender'].forEach(function(group){
    document.querySelectorAll('input[name="' + group + '"]').forEach(function(input){
      input.addEventListener('change', render);
    });
  });
  render();
})();
</script>'''

# ---------------------------------------------------------------
# regions.html -> {지역} 학교검색 (search UI over all schools)
# ---------------------------------------------------------------
def regions_body_and_js():
    groups = []
    for level in ["초등학교", "중학교", "고등학교"]:
        items = [s for s in SCHOOLS if s["level"] == level]
        lis = "\n        ".join(
            '<li data-name="{name}" data-level="{level}"><a href="schools/{slug}.html">{name} <span class="arrow">→</span></a></li>'.format(
                name=s["name"], level=s["level"], slug=s["slug"]
            )
            for s in items
        )
        groups.append('''<div class="school-group" data-group="{level}" hidden>
      <h3 style="font-size:15px;margin:22px 0 10px;">{level} <span class="mono" style="font-size:12px;color:var(--muted-2);font-weight:400;">({count}곳)</span></h3>
      <ul class="school-list" id="list-{level}">
        {lis}
      </ul>
    </div>'''.format(level=level, count=len(items), lis=lis))

    body = '''
<section class="page-hero">
  <span class="eyebrow">{region} 학교검색</span>
  <h1>우리 학교, 검색해서 바로 확인하세요</h1>
  <p>초등학교 {n_es}곳, 중학교 {n_ms}곳, 고등학교 {n_hs}곳까지 {region}의 모든 학교를 안내하고 있어요. 학교 이름을 입력하면 바로 찾아드려요.</p>
</section>
<section>
  <div class="field" style="max-width:480px;margin-bottom:8px;">
    <label for="school-search">학교 이름으로 검색</label>
    <input id="school-search" type="text" placeholder="예: {sample}" autocomplete="off">
  </div>
  <p id="search-prompt" class="sample-note">학교 이름을 입력하면 결과가 나타나요.</p>
  <p id="search-empty" class="sample-note" hidden>검색 결과가 없어요. 학교 이름을 다시 확인해 주세요.</p>
  <div id="school-groups">
    {groups}
  </div>
</section>
'''.format(
        region=REGION_SHORT, n_es=len(ELEMENTARY_NAMES), n_ms=len(MIDDLE_NAMES), n_hs=len(HIGH_NAMES),
        sample=", ".join(
            sample_keyword(s["name"])
            for lvl in ["초등학교", "중학교", "고등학교"]
            for s in [next((x for x in SCHOOLS if x["level"] == lvl), None)]
            if s
        ),
        groups="\n    ".join(groups),
    )

    js = '''<script>
(function(){{
  var input = document.getElementById('school-search');
  var prompt = document.getElementById('search-prompt');
  var empty = document.getElementById('search-empty');
  var groups = document.querySelectorAll('.school-group');
  if(!input) return;
  input.addEventListener('input', function(){{
    var q = input.value.trim().toLowerCase();
    if(q === ''){{
      prompt.hidden = false;
      empty.hidden = true;
      groups.forEach(function(g){{ g.hidden = true; }});
      return;
    }}
    prompt.hidden = true;
    var anyVisible = false;
    groups.forEach(function(g){{
      var items = g.querySelectorAll('li');
      var groupHasMatch = false;
      items.forEach(function(li){{
        var name = (li.getAttribute('data-name') || '').toLowerCase();
        var match = name.indexOf(q) !== -1;
        li.hidden = !match;
        if(match) groupHasMatch = true;
      }});
      g.hidden = !groupHasMatch;
      if(groupHasMatch) anyVisible = true;
    }});
    empty.hidden = anyVisible;
  }});
}})();
</script>'''
    return body, js

regions_body, regions_js = regions_body_and_js()

# ---------------------------------------------------------------
# blog.html (index only, cards to be added over time)
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# 블로그 글 목록 — 새 글은 이 리스트 맨 앞(최신순)에 추가
# 각 항목: slug, title, date(YYYY-MM-DD), category, teaser(카드용 요약), body(본문 HTML, <h2>/<p>/<strong> 등)
# ---------------------------------------------------------------
BLOG_POSTS = []  # 아래에서 append (파일 뒷부분 참고)

def blog_card(post):
    return '''<div class="article-card">
      <div class="meta">{date} · {category}</div>
      <h3>{title}</h3>
      <p>{teaser}</p>
      <a class="more" href="blog/{slug}.html">본문 보기 →</a>
    </div>'''.format(date=post["date"], category=post["category"], title=post["title"], teaser=post["teaser"], slug=post["slug"])

def build_blog_body():
    cards = "\n    ".join(blog_card(p) for p in BLOG_POSTS)
    return f'''
<section class="page-hero">
  <span class="eyebrow">블로그</span>
  <h1>{REGION_SHORT} 학교별 내신·과목별 학습 전략</h1>
  <p>{REGION_SHORT} 학교별 내신 대비, 학년별·과목별 화상과외 학습 전략을 꾸준히 올리고 있어요.</p>
</section>
<section>
  <div class="article-grid">
    <!-- BLOG_GRID_START -->
    {cards}
    <!-- BLOG_GRID_END -->
  </div>
</section>
'''

def blog_post_body(post):
    return f'''
<nav class="breadcrumb"><a href="../blog.html">블로그</a> / {post["category"]}</nav>
<section class="page-hero">
  <span class="eyebrow">{post["date"]} · {post["category"]}</span>
  <h1>{post["title"]}</h1>
</section>
<section>
  <article class="prose">
    {post["body"]}
  </article>
</section>
<section>
  <div class="apply-wrap" style="grid-template-columns:1fr;">
    <div>
      <span class="eyebrow" style="color:var(--accent-strong)">지금 확인해보세요</span>
      <h2>30분 무료체험수업 먼저 받아보세요</h2>
      <p style="color:#DCEEE8;">이름과 연락처만 남겨주시면 24시간 이내에 담당자가 연락드립니다.</p>
      <div style="margin-top:18px;"><a class="cta-btn" href="../apply.html" style="background:var(--accent);color:var(--primary-strong)!important;">무료 상담 신청하기</a></div>
    </div>
  </div>
</section>
<p style="margin-top:14px;"><a href="../blog.html">← 블로그 목록으로</a></p>
'''

# ---------------------------------------------------------------
# 블로그 글: 거제 학교 x 화상과외 키워드 조합 (일일 업로드분)
# ---------------------------------------------------------------
BLOG_POSTS.append({
    "slug": "geoje-jungdeung-gimalgosa-naeshin",
    "title": "거제중학교·거제고현중학교 2학기 기말고사 대비, 내신관리 어떻게 시작할까요",
    "date": "2026-09-23",
    "category": "중등 내신관리",
    "teaser": "2학기 기말고사가 얼마 안 남았어요. 거제중학교·거제고현중학교 학생 기준으로 지금부터 챙겨야 할 것들을 정리했어요.",
    "body": '''
    <p><strong>거제중학교</strong>나 <strong>거제고현중학교</strong>에 다니는 자녀를 둔 학부모님이라면, 2학기 기말고사가 다가올수록 마음이 조급해지실 거예요. 2학기 기말고사는 겨울방학 전 마지막 시험이라 내신 등급에 미치는 영향이 크고, 범위도 넓어서 미리 계획을 세우지 않으면 막판에 몰아서 공부하다 끝나는 경우가 많아요.</p>
    <h2>거제중학교·거제고현중학교 2학기 기말고사, 왜 미리 준비해야 할까요</h2>
    <p>2학기 기말고사는 1학기보다 시험 범위가 넓은 경우가 대부분이에요. 특히 국어·사회처럼 암기와 이해가 함께 필요한 과목은 벼락치기로 대응하기 어렵고, 수학은 2학기 진도 자체가 1학기보다 난이도가 높아지는 경우가 많아 미리 개념을 잡아두지 않으면 시험 직전에 당황하기 쉬워요.</p>
    <p>티치핏거제에서는 상담 시 재학 중인 학교와 최근 시험 성적을 먼저 확인해요. 거제중학교와 거제고현중학교는 같은 거제 안에서도 시험 문제 유형과 서술형 비중이 다르기 때문에, 학교 이름만 알아도 어떤 방식으로 준비해야 할지 방향을 잡을 수 있어요.</p>
    <h2>내신관리, 시험 2주 전부터는 이렇게 다르게 접근해요</h2>
    <p>기말고사 2주 전부터는 새로운 내용을 넓히기보다 <strong>이미 배운 범위를 확실히 다지는 것</strong>이 더 중요해요. 특히 서술형 문제 비중이 높은 학교라면, 개념을 정확한 문장으로 설명할 수 있는지 점검하는 연습이 꼭 필요합니다.</p>
    <p>화상과외로 진행하면 아이의 취약 단원만 골라서 집중적으로 복습할 수 있어요. 수업을 녹화해두기 때문에, 이해가 덜 된 부분만 다시 돌려보면서 시험 직전까지 반복 학습이 가능하다는 것도 큰 장점이에요.</p>
    <h2>화상과외가 기말고사 내신관리에 잘 맞는 이유</h2>
    <p>거제 안에서 원하는 시간대에, 학교 시험 유형까지 잘 아는 선생님을 구하기는 생각보다 쉽지 않아요. 화상과외라면 지역 제약 없이 더 넓은 범위에서 거제중학교·거제고현중학교 학생을 지도해본 경험이 있는 선생님을 연결받을 수 있고, 이동 시간이 없어 시험 기간에도 유연하게 수업 시간을 잡을 수 있어요.</p>
    <p><strong>Q. 거제중학교, 거제고현중학교 둘 다 매칭이 가능한가요?</strong><br>
    네, 두 학교 모두 매칭 가능하고 그 외 거제 관내 중학교 20곳 전부 안내해 드려요. 상담 시 재학 중인 학교를 알려주시면 그에 맞춰 준비해 드립니다.</p>
    <p><strong>Q. 지금 신청하면 기말고사 전에 시작할 수 있나요?</strong><br>
    신청 후 24시간 이내 담당자가 연락드리고, 30분 무료체험수업으로 먼저 선생님과의 궁합을 확인한 뒤 바로 시작하실 수 있어요.</p>
    ''',
})

BLOG_POSTS.append({
    "slug": "geoje-chodeung-seonhaenghaksup",
    "title": "장승포초등학교·수월초등학교 학부모님이 묻는 선행학습, 언제 시작해야 할까요",
    "date": "2026-09-23",
    "category": "초등 선행학습",
    "teaser": "선행학습, 무작정 빨리 시작하는 게 능사는 아니에요. 장승포초등학교·수월초등학교 학생 기준으로 시기와 방법을 짚어봤어요.",
    "body": '''
    <p><strong>장승포초등학교</strong>나 <strong>수월초등학교</strong> 학부모님과 상담하다 보면 "선행학습, 지금 시작해도 되는 걸까요?"라는 질문을 정말 많이 받아요. 옆집 아이가 몇 학년 진도를 나간다는 얘기를 들으면 조급해지기 마련이지만, 사실 선행학습은 시기보다 <strong>아이가 지금 배우는 내용을 얼마나 소화했는지</strong>가 먼저예요.</p>
    <h2>선행학습, 무조건 빨리 시작하면 안 되는 이유</h2>
    <p>현재 학년 내용을 제대로 이해하지 못한 상태에서 다음 학년 진도부터 나가면, 아이는 두 가지를 동시에 어려워하게 돼요. 지금 배우는 것도 헷갈리고, 미리 배운 것도 기초가 얕아 금방 잊어버리는 거예요. 그래서 선행학습을 시작하기 전에는 현재 학년 개념이 얼마나 탄탄한지부터 점검하는 게 순서예요.</p>
    <h2>장승포초등학교·수월초등학교 학생이라면 이런 순서를 추천해요</h2>
    <p>티치핏거제에서는 상담 시 아이의 현재 학년 이해도를 먼저 확인하고, 부족한 단원이 있다면 그것부터 채운 다음 선행 진도를 조금씩 얹는 방식으로 진행해요. 장승포초등학교, 수월초등학교처럼 학교마다 학습 분위기와 진도 체감이 다르기 때문에, 재학 중인 학교를 먼저 확인하는 것도 이런 이유예요.</p>
    <p>고학년이라면 중학교 수학과 연결되는 개념(비와 비율, 도형 등)을 의식하면서 선행을 진행하는 게 좋고, 저학년이라면 선행보다는 숫자 감각과 학습 습관을 먼저 다지는 편이 장기적으로 더 유리해요.</p>
    <h2>화상과외가 선행학습에 유리한 이유</h2>
    <p>선행학습은 아이 속도에 맞춰 진도를 조절할 수 있는 선생님을 만나는 게 핵심이에요. 화상과외라면 거제 지역 안에서만 찾을 때보다 훨씬 넓은 범위에서, 선행 지도 경험이 많은 선생님을 연결받을 수 있어요. 수업을 녹화해두기 때문에 이해가 안 된 부분은 부모님이 함께 다시 확인해볼 수 있다는 것도 장점이에요.</p>
    <p><strong>Q. 장승포초등학교, 수월초등학교 학생 모두 매칭이 가능한가요?</strong><br>
    네, 두 학교 모두 매칭 가능하고 거제 관내 초등학교 41곳 전부 안내해 드려요.</p>
    <p><strong>Q. 아직 선행이 필요한지 판단이 안 서요, 상담만 받아도 되나요?</strong><br>
    물론이에요. 상담 시 현재 학습 상태를 먼저 확인해 드리고, 선행이 필요한 시점인지도 함께 안내해 드려요. 30분 무료체험수업으로 먼저 확인해보실 수 있습니다.</p>
    ''',
})

BLOG_POSTS.append({
    "slug": "geoje-godeung-suneung-naeshin-gyunhyeong",
    "title": "거제고등학교·거제제일고등학교 학생이라면, 내신과 수능 균형을 이렇게 잡으세요",
    "date": "2026-09-23",
    "category": "고등 내신·수능",
    "teaser": "고등학교 때는 내신과 수능을 같이 챙겨야 해서 더 헷갈려요. 거제고등학교·거제제일고등학교 학생 기준으로 정리했어요.",
    "body": '''
    <p><strong>거제고등학교</strong>나 <strong>거제제일고등학교</strong>에 다니는 학생이라면, 고등학교에 올라오면서 가장 크게 부딪히는 고민이 "내신 공부와 수능 공부를 따로 해야 하나"일 거예요. 시간은 한정돼 있는데 둘 다 챙겨야 한다는 부담감 때문에 오히려 이도 저도 아니게 되는 경우가 적지 않아요.</p>
    <h2>내신과 수능, 완전히 다른 공부는 아니에요</h2>
    <p>내신은 학교 진도와 문제 스타일에 맞춰 준비하는 것이고, 수능은 전국 단위 출제 기준에 맞춰 준비하는 거라 방향이 달라 보이지만, 개념 자체는 크게 다르지 않아요. 다만 <strong>같은 개념을 어떤 방식으로 훈련하느냐</strong>가 다를 뿐이에요. 그래서 학기 중 내신 기간에는 학교 시험 스타일에 맞춰 훈련하고, 방학이나 시험 사이 기간에는 수능형 문제로 개념을 확장하는 방식이 효율적이에요.</p>
    <h2>거제고등학교·거제제일고등학교 학생에게 맞는 시기별 전략</h2>
    <p>내신 기간 2~3주 전에는 학교 기출 스타일과 서술형 비중을 확인해 그에 맞춰 집중적으로 준비하고, 내신 기간이 끝난 직후에는 곧바로 수능형 문제로 넘어가 감을 유지하는 게 좋아요. 티치핏거제는 상담 시 재학 중인 학교와 최근 시험 결과를 확인해서, 이 두 가지 사이를 자연스럽게 오갈 수 있도록 커리큘럼을 조정해 드려요.</p>
    <h2>화상과외로 관리하면 좋은 점</h2>
    <p>고3이 가까워질수록 내신·수능을 함께 지도해본 경험이 있는 선생님을 만나는 게 중요한데, 거제 지역 안에서만 찾으면 선택지가 좁아질 수밖에 없어요. 화상과외라면 지역 제약 없이 폭넓게 비교하고 고를 수 있고, 저녁 늦은 시간대에도 유연하게 수업을 잡을 수 있어 학교·학원 일정과 겹치지 않게 조정하기 편해요.</p>
    <p><strong>Q. 거제고등학교, 거제제일고등학교 모두 매칭 가능한가요?</strong><br>
    네, 두 학교 모두 매칭 가능하고 거제 관내 고등학교 11곳 전부 안내해 드려요.</p>
    <p><strong>Q. 고3인데 지금 시작해도 늦지 않을까요?</strong><br>
    현재 학습 상태를 먼저 진단한 뒤 남은 기간에 맞는 현실적인 계획을 세워드려요. 30분 무료체험수업으로 먼저 방향을 확인해보실 수 있습니다.</p>
    ''',
})

BLOG_POSTS.append({
    "slug": "geoje-chodeung-naeshin-seubgwan-gyeryong-aju",
    "title": "계룡초등학교·아주초등학교, 초등 내신 습관은 몇 학년부터 잡아야 할까요",
    "date": "2026-09-23",
    "category": "초등 학습습관",
    "teaser": "초등학교엔 내신이 없다고 안심하기엔 일러요. 계룡초등학교·아주초등학교 학부모님이 자주 묻는 학습 습관 잡는 시기를 정리했어요.",
    "body": '''
    <p><strong>계룡초등학교</strong>나 <strong>아주초등학교</strong> 학부모님 중에는 "초등학교는 내신이 없는데 굳이 지금부터 학습 습관을 챙겨야 하나요?"라고 물으시는 분들이 있어요. 맞는 말이에요, 초등학교엔 성적표에 등급이 찍히지 않죠. 하지만 <strong>중학교 첫 시험에서 결과가 갈리는 지점</strong>은 사실 초등 고학년 때 만들어진 학습 습관인 경우가 많아요.</p>
    <h2>왜 초등학교 때부터 학습 습관을 챙겨야 할까요</h2>
    <p>중학교에 올라가면 갑자기 시험 범위, 서술형 문항, 수행평가까지 한꺼번에 마주하게 돼요. 이때 스스로 계획을 세우고 복습하는 습관이 안 잡혀 있으면, 아무리 똑똑한 아이라도 첫 시험에서 크게 당황하는 경우가 많아요. 반대로 초등 고학년 때부터 스스로 정리하고 확인하는 습관을 들인 아이는 중학교 진입이 훨씬 수월해요.</p>
    <h2>계룡초등학교·아주초등학교 학생이라면 몇 학년부터 시작하면 좋을까요</h2>
    <p>저학년(1~3학년)은 학습량보다 <strong>스스로 생각하고 설명하는 습관</strong>을 만드는 시기예요. 짧고 재미있게, 놀이처럼 접근하는 게 좋아요. 고학년(4~6학년)부터는 시험 범위를 스스로 정리해보고, 틀린 문제를 다시 풀어보는 습관을 조금씩 들이는 게 중학교 대비에 실질적으로 도움이 돼요.</p>
    <p>티치핏거제는 상담 시 아이의 학년과 재학 중인 학교를 먼저 확인해서, 계룡초등학교·아주초등학교 같은 학교 분위기와 학년 수준을 고려한 선생님을 연결해 드려요.</p>
    <h2>화상과외가 학습 습관 잡기에도 도움이 되는 이유</h2>
    <p>화상 수업은 정해진 시간에 화면으로 만나는 구조라, 아이 입장에서는 "이 시간엔 공부한다"는 루틴이 자연스럽게 생겨요. 수업 녹화 덕분에 부모님도 나중에 수업 분위기를 확인하실 수 있어, 아이가 스스로 잘 따라가고 있는지 점검하기도 편해요.</p>
    <p><strong>Q. 계룡초등학교, 아주초등학교 둘 다 매칭 가능한가요?</strong><br>
    네, 두 학교 모두 매칭 가능하고 거제 관내 초등학교 41곳 전부 안내해 드려요.</p>
    <p><strong>Q. 아직 어린데 화상 수업에 잘 적응할 수 있을까요?</strong><br>
    생각보다 빠르게 적응하는 경우가 많아요. 30분 무료체험수업으로 먼저 아이 반응을 확인해보실 수 있어요.</p>
    ''',
})

BLOG_POSTS.append({
    "slug": "geoje-ogpo-jungdeung-godeung-siheom-hwasang",
    "title": "옥포중학교·옥포고등학교 시험 기간, 화상과외로 준비하면 다른 점",
    "date": "2026-09-23",
    "category": "중고등 시험대비",
    "teaser": "옥포 지역 학생들은 학원 이동 시간도 부담이에요. 옥포중학교·옥포고등학교 기준으로 화상과외가 시험 준비에 어떻게 도움이 되는지 정리했어요.",
    "body": '''
    <p><strong>옥포중학교</strong>나 <strong>옥포고등학교</strong>에 다니는 학생이라면, 시험 기간마다 학원을 오가는 이동 시간이 은근히 부담스러웠을 거예요. 안 그래도 부족한 시험 준비 시간을 이동하는 데 쓰다 보면, 정작 문제 풀고 개념 정리할 시간이 줄어드는 경우가 많아요.</p>
    <h2>옥포중학교·옥포고등학교 학생이 시험 기간에 겪는 고민</h2>
    <p>옥포 지역은 학원이 몰려 있는 시간대엔 원하는 선생님을 구하기 어렵고, 저녁 시간대는 이동까지 겹쳐 아이가 지치기 쉬워요. 특히 시험 2주 전처럼 촘촘하게 계획을 짜야 하는 시기엔, 이동 시간 자체가 학습 효율을 떨어뜨리는 요인이 되기도 해요.</p>
    <h2>화상과외로 시험 준비하면 달라지는 점</h2>
    <p>화상과외는 이동 시간이 아예 없기 때문에, 그만큼 학습에 쓸 수 있는 시간이 늘어나요. 저녁 늦은 시간대도 유연하게 잡을 수 있어서, 학교·학원 일정이 끝난 뒤에도 부담 없이 수업을 넣을 수 있어요. 또한 옥포 지역 안에서만 찾을 때보다 훨씬 넓은 범위에서 옥포중학교·옥포고등학교 학생을 지도해본 경험이 있는 선생님을 연결받을 수 있다는 것도 큰 장점이에요.</p>
    <p>티치핏거제는 상담 시 재학 중인 학교와 시험 범위를 먼저 확인하고, 그에 맞춰 단원별로 취약한 부분을 콕 집어 복습할 수 있도록 커리큘럼을 짜드려요. 수업은 녹화되기 때문에 시험 직전까지 반복해서 다시 볼 수 있어요.</p>
    <h2>시험 기간, 언제부터 화상과외를 시작하면 좋을까요</h2>
    <p>이상적으로는 시험 2~3주 전부터 시작해서 취약 단원을 먼저 채우고, 마지막 1주는 실전 문제 풀이 위주로 마무리하는 방식을 추천해요. 다만 지금 당장 급하게 필요한 경우라도, 상담 시 남은 기간에 맞춰 현실적인 계획을 함께 세워드려요.</p>
    <p><strong>Q. 옥포중학교, 옥포고등학교 모두 매칭 가능한가요?</strong><br>
    네, 두 학교 모두 매칭 가능하고 그 외 거제 관내 중·고등학교 전부 안내해 드려요.</p>
    <p><strong>Q. 시험이 얼마 안 남았는데 지금 신청해도 될까요?</strong><br>
    네, 신청 후 24시간 이내 담당자가 연락드리고 30분 무료체험수업부터 빠르게 진행해 드릴 수 있어요.</p>
    ''',
})

# ---------------------------------------------------------------
# apply.html (noindex, standalone page reusing hero form)
# ---------------------------------------------------------------
apply_body = f'''
<section class="page-hero">
  <span class="eyebrow">30분 무료체험</span>
  <h1>학습 궁합부터 확인하는 화상과외 체험 신청</h1>
  <p>이름과 연락처만 남겨주시면 24시간 이내에 담당자가 직접 연락드려요. 상담과 30분 체험 수업은 모두 무료입니다.</p>
</section>
<section>
  <div class="apply-wrap">
    <div>
      <span class="eyebrow" style="color:var(--accent-strong)">신청 전 확인해주세요</span>
      <h2>이렇게 진행됩니다</h2>
      <ul class="apply-perks">
        <li>신청 후 24시간 이내 담당자 연락</li>
        <li>학습 진단 → 선생님 추천 → 30분 무료체험수업</li>
        <li>체험 수업이 마음에 들 때만 정식으로 결정</li>
      </ul>
      <div style="margin-top:24px; padding-top:20px; border-top:1px solid rgba(255,255,255,.15);">
        <p style="color:#BFDCD3; font-size:13.5px; margin-bottom:10px;">폼 작성이 번거로우시면 전화나 카카오톡으로 바로 상담하셔도 돼요.</p>
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
          <a class="cta-ghost" style="border-color:rgba(255,255,255,.35); color:#fff;" href="tel:{PHONE_TEL}">\U0001F4DE 전화 상담</a>
          <a class="cta-ghost" style="border-color:rgba(255,255,255,.35); color:#fff;" href="{KAKAO_URL}" target="_blank" rel="noopener">\U0001F4AC 카카오톡 상담</a>
        </div>
      </div>
    </div>
    {APPLY_FORM}
  </div>
</section>
'''

# ---------------------------------------------------------------
# school page template (level-aware, templated copy + real school name)
# ---------------------------------------------------------------
def school_body(school):
    level = school["level"]
    info = LEVEL_INFO[level]
    same_level_others = [s for s in SCHOOLS if s["level"] == level and s["slug"] != school["slug"]]
    nearby = same_level_others[:5]
    other_links = "\n        ".join(
        '<li><a href="{slug}.html">{name} <span class="arrow">→</span></a></li>'.format(slug=s["slug"], name=s["name"])
        for s in nearby
    )
    subjects_row = "".join('<span>{}</span>'.format(s) for s in info["subjects"])
    return f'''
<nav class="breadcrumb"><a href="../regions.html">{REGION_SHORT} 학교검색</a> / {REGION_FULL} · {level}</nav>
<section class="page-hero">
  <span class="eyebrow">{REGION_FULL} {level} · 화상과외</span>
  <h1>{school["name"]} 화상과외, 학교 특성부터 확인하고 시작하세요</h1>
  <p>{school["name"]} {info["stage"]} 학생을 위해, 학교 사정을 아는 선생님과 실시간 화상으로 연결해 드려요.</p>
</section>
<section>
  <div class="prose">
    <h2>{school["name"]} {info["stage"]}이 상담에서 자주 이야기하는 고민</h2>
    <p>{school["name"]} 학생과 학부모님이 상담에서 가장 많이 말씀하시는 건 <strong>{info["focus"]}</strong>이에요. 특히 <strong>{info["worry"]}</strong>을 어려워하는 경우가 많아요. 학교마다 진도와 분위기가 다르기 때문에, 같은 학년이라도 접근 방식을 다르게 가져가야 해요.</p>
    <p>{BRAND}에서는 상담 시 최근 학습 상태와 취약 부분을 먼저 확인한 뒤, {school["name"]} 같은 {level} 학생을 지도해본 경험이 있거나 {REGION_SHORT} 지역 사정을 아는 선생님을 화상으로 연결해 드립니다.</p>
    <h3>왜 화상과외가 {school["name"]} 학생에게 잘 맞을까요</h3>
    <p>{REGION_SHORT} 안에서 원하는 과목·시간대·스타일의 선생님을 구하기 어려운 경우가 많아요. 화상 수업이면 지역 제약 없이 훨씬 넓은 범위에서 맞는 선생님을 찾을 수 있고, 이동 시간이 없어 저녁 시간대도 유연하게 잡을 수 있어요. 수업은 녹화되어 복습에도 활용할 수 있습니다.</p>
    <h3>과목별 과외 안내</h3>
    <p>{school["name"]} 학생 대상으로는 아래 과목의 화상과외를 안내하고 있어요.</p>
    <div class="subjects" style="margin-bottom:6px;">{subjects_row}</div>
  </div>
</section>
<section>
  <div class="head-row"><div><span class="eyebrow">같은 급 다른 학교</span><h2>{level} 학생이 많이 찾는 학교</h2></div></div>
  <ul class="school-list" style="max-width:480px;">
    {other_links}
  </ul>
  <p style="margin-top:14px;font-size:13.5px;"><a href="../regions.html">{REGION_SHORT} 학교 전체 검색하기 →</a></p>
</section>
<section>
  <div class="apply-wrap" style="grid-template-columns:1fr;">
    <div>
      <span class="eyebrow" style="color:var(--accent-strong)">{school["name"]} 학생 학부모님께</span>
      <h2>지금 무료 상담을 신청해보세요</h2>
      <p style="color:#DCEEE8;">이름과 연락처만 남겨주시면 24시간 이내에 담당자가 연락드립니다.</p>
      <div style="margin-top:18px;"><a class="cta-btn" href="../apply.html" style="background:var(--accent);color:var(--primary-strong)!important;">무료 상담 신청하기</a></div>
    </div>
  </div>
</section>
'''

# generate all pages
# ---------------------------------------------------------------
page("index.html", f"{REGION_SHORT} 과외 | 초등·중등·고등 수학 영어 1:1 화상과외 · {BRAND}", f"{REGION_SHORT} 과외를 찾고 계신가요? 초등학생부터 고등학생까지, 수학·영어·국어 등 전 과목 1:1 화상과외를 30분 무료체험수업으로 먼저 받아보세요.", "index.html",
     index_body,
     path_prefix="", canonical=BASE_URL + "/index.html")

page("services.html", f"화상과외 소개 | {BRAND}", f"{REGION_SHORT} 학생을 위한 실시간 화상과외, 녹화 복습, 지역 맞춤 매칭을 소개합니다.", "services.html",
     services_body, path_prefix="", canonical=BASE_URL + "/services.html")

page("process.html", f"매칭 방식 | {BRAND}", f"학습 진단부터 리포트까지, {BRAND}의 5단계 화상과외 매칭 프로세스를 소개합니다.", "process.html",
     process_body, path_prefix="", canonical=BASE_URL + "/process.html")

page("teachers.html", f"선생님 소개 | {BRAND}", f"학력·신원·경력 검증을 거친 {BRAND} 화상과외 선생님 매칭 기준을 소개합니다.", "teachers.html",
     teachers_body, path_prefix="", canonical=BASE_URL + "/teachers.html", extra_js=teachers_js)

page("regions.html", f"{REGION_SHORT} 학교검색 | {BRAND}", f"{REGION_SHORT} 초·중·고 {len(SCHOOLS)}개 학교를 검색해서 바로 찾는 {BRAND} 화상과외 학교 안내입니다.", "regions.html",
     regions_body, path_prefix="", canonical=BASE_URL + "/regions.html", extra_js=regions_js)

page("blog.html", f"블로그 | {BRAND}", f"{REGION_SHORT} 학교별 내신 대비, 과목별 화상과외 학습 전략을 소개하는 {BRAND} 블로그입니다.", "blog.html",
     build_blog_body(), path_prefix="", canonical=BASE_URL + "/blog.html")

for post in BLOG_POSTS:
    page(
        "blog/{}.html".format(post["slug"]),
        "{} | {}".format(post["title"], BRAND),
        post["teaser"],
        "blog.html",
        blog_post_body(post),
        path_prefix="../",
        canonical=BASE_URL + "/blog/{}.html".format(post["slug"]),
    )

page("apply.html", f"무료 상담 신청 | {BRAND}", f"{BRAND} 화상과외 매칭 무료 상담을 신청하세요.", "apply.html",
     apply_body, path_prefix="", canonical=BASE_URL + "/apply.html", noindex=True)

thanks_body = '''
<section class="page-hero" style="text-align:center;">
  <span class="eyebrow">신청 완료</span>
  <h1>상담 신청이 접수되었습니다</h1>
  <p style="max-width:52ch;margin-inline:auto;">24시간 이내에 담당자가 남겨주신 연락처로 안내드릴게요. 잠시만 기다려 주세요.</p>
  <div style="margin-top:22px;"><a class="cta-btn" href="index.html">홈으로 돌아가기</a></div>
</section>
'''
page("thanks.html", f"신청 완료 | {BRAND}", f"{BRAND} 상담 신청이 정상적으로 접수되었습니다.", "",
     thanks_body, path_prefix="", canonical=BASE_URL + "/thanks.html", noindex=True)

for school in SCHOOLS:
    page(
        "schools/{}.html".format(school["slug"]),
        "{} 화상과외 | {}".format(school["name"], BRAND),
        "{} 학생을 위한 1:1 화상과외 매칭, {}에서 상담해보세요.".format(school["name"], BRAND),
        "regions.html",
        school_body(school),
        path_prefix="../",
        canonical=BASE_URL + "/schools/{}.html".format(school["slug"]),
    )

# ---------------------------------------------------------------
# sitemap.xml (public pages only)
# ---------------------------------------------------------------
sitemap_urls = ["index.html", "services.html", "process.html", "teachers.html", "regions.html", "blog.html"]
for school in SCHOOLS:
    sitemap_urls.append("schools/{}.html".format(school["slug"]))
for post in BLOG_POSTS:
    sitemap_urls.append("blog/{}.html".format(post["slug"]))

sitemap_items = "\n".join(
    "  <url><loc>{}/{}</loc></url>".format(BASE_URL, u) for u in sitemap_urls
)
sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{}\n</urlset>\n'.format(sitemap_items)
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap_xml)
print("wrote sitemap.xml")

# ---------------------------------------------------------------
# rss.xml (blog posts, newest first)
# ---------------------------------------------------------------
def rss_pubdate(date_str):
    import datetime
    d = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return d.strftime("%a, %d %b %Y 00:00:00 +0900")

rss_items = "\n".join('''  <item>
    <title>{title}</title>
    <link>{base}/blog/{slug}.html</link>
    <guid>{base}/blog/{slug}.html</guid>
    <description>{teaser}</description>
    <pubDate>{pubdate}</pubDate>
  </item>'''.format(title=p["title"], base=BASE_URL, slug=p["slug"], teaser=p["teaser"], pubdate=rss_pubdate(p["date"]))
    for p in sorted(BLOG_POSTS, key=lambda p: p["date"], reverse=True)
)
rss_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{brand} 블로그</title>
  <link>{base}/blog.html</link>
  <description>{region} 학교별 내신·과목별 화상과외 학습 전략</description>
  <language>ko-kr</language>
  <atom:link href="{base}/rss.xml" rel="self" type="application/rss+xml"/>
  <lastBuildDate>{lastbuild}</lastBuildDate>

  <!-- RSS_ITEMS_START -->
{items}
  <!-- RSS_ITEMS_END -->

</channel>
</rss>
'''.format(brand=BRAND, base=BASE_URL, region=REGION_SHORT, items=rss_items,
           lastbuild=rss_pubdate(BLOG_POSTS[0]["date"]) if BLOG_POSTS else rss_pubdate("2026-01-01"))
with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
    f.write(rss_xml)
print("wrote rss.xml")

robots_txt = '''User-agent: *
Disallow: /apply.html
Disallow: /thanks.html
Allow: /

Sitemap: {}/sitemap.xml
'''.format(BASE_URL)
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(robots_txt)
print("wrote robots.txt")

print("DONE - {} schools (region: {})".format(len(SCHOOLS), REGION_SLUG))
