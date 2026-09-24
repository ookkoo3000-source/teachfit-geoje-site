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

BLOG_POSTS.append({
    "slug": "geoje-sinhyeon-hwasang-gwaoe-iyu",
    "title": "신현중학교·신현초등학교 화상과외, 요즘 학부모님들이 이걸 선택하는 이유",
    "date": "2026-09-24",
    "category": "화상과외 소개",
    "teaser": "방문 과외 선생님 구하기 어려우셨다면, 신현중학교·신현초등학교 학부모님들이 화상과외를 선택하는 진짜 이유를 확인해보세요.",
    "body": '''
    <p>신현중학교나 신현초등학교에 아이를 보내고 계신 학부모님이라면 한 번쯤 '방문 과외가 나을까, 화상과외가 나을까' 고민해보셨을 거예요. 예전에는 화상 수업이라고 하면 어딘가 부족하고 임시방편처럼 느껴지던 시절도 있었지만, 요즘은 오히려 화상과외를 먼저 찾는 학부모님이 눈에 띄게 늘고 있어요. 특히 신현 지역처럼 학원과 과외 선생님 선택지가 한정적인 곳에서는, 화상과외가 단순한 대안이 아니라 더 정확한 매칭을 가능하게 해주는 방법으로 자리잡고 있습니다. 이 글에서는 왜 지금 신현중학교·신현초등학교 학부모님들이 화상과외를 선택하고 있는지, 그리고 실제로 어떤 점이 다른지 구체적으로 짚어드릴게요. 상담 사례를 바탕으로 실제 변화까지 함께 정리했으니 끝까지 참고해보시면 좋을 것 같아요.</p>
    <h2>신현중학교·신현초등학교 학부모님이 요즘 이런 고민을 많이 하세요</h2>
    <p>상담을 하다 보면 신현중학교, 신현초등학교에 다니는 자녀를 둔 학부모님들에게서 공통적으로 듣는 이야기가 있어요. 바로 '아이한테 맞는 선생님을 구하기가 생각보다 어렵다'는 점이에요. 근처 학원을 보내자니 아이 성향과 안 맞는 것 같고, 개인과외 선생님을 구하자니 시간대나 조건이 맞는 분을 찾기가 쉽지 않다는 거예요. 특히 아이가 특정 과목에서 유독 약점을 보이거나, 반대로 또래보다 앞서 나가고 싶어하는 경우라면 더더욱 그래요. 일반적인 학원 커리큘럼으로는 이런 세밀한 부분까지 챙기기 어렵기 때문에, 결국 1:1로 봐줄 수 있는 선생님이 필요하다는 결론에 도달하시는 경우가 많습니다. 문제는 그런 선생님을 신현 지역 안에서만 찾으려고 하면 선택지가 확 줄어든다는 거예요. 경력이나 전공, 지도 스타일까지 고려하면 조건에 맞는 분을 찾는 데 시간도 오래 걸리고, 어렵게 찾아도 시간대가 안 맞아서 포기하는 경우도 종종 있어요. 이런 고민을 반복해서 듣다 보니, 티치핏거제에서는 처음부터 아예 화상과외 하나에만 집중하는 방식을 택하게 됐습니다. 방문 과외나 여러 프로그램을 한꺼번에 운영하기보다, 화상이라는 한 가지 방식 안에서 매칭의 정확도를 최대한 끌어올리는 편이 학부모님과 아이 모두에게 더 실질적인 도움이 된다고 판단했기 때문이에요. 실제로 처음 상담을 요청하시는 분들 중 상당수가 이미 여러 곳에 문의를 넣어봤지만 시간대나 조건이 맞지 않아 포기했던 경험이 있는 경우가 많았어요. 그런 분들일수록 '넓은 범위에서 조건에 맞는 선생님을 찾을 수 있다'는 점 하나만으로도 마음이 한결 놓인다는 반응을 자주 보이십니다. 또 하나 자주 나오는 이야기는, 아이가 특정 과목만 부분적으로 도움이 필요한데 학원은 전 과목 패키지로만 운영돼서 불필요한 비용까지 지불해야 했다는 점이에요. 화상과외는 필요한 과목만 골라서 1:1로 진행할 수 있기 때문에, 이런 부분에서도 훨씬 효율적이라는 반응을 많이 듣습니다.</p>
    <h2>신현 지역 학생들에게 왜 이 고민이 유독 클까요</h2>
    <p>신현동은 거제 안에서도 아파트 단지가 많고 학령기 자녀를 둔 가구가 밀집해 있는 지역이에요. 그러다 보니 학원 수요는 많은데, 정작 한 명 한 명에게 맞춰 지도해줄 수 있는 개인 선생님은 상대적으로 부족한 편입니다. 학원들은 대부분 정해진 커리큘럼과 반 편성으로 운영되기 때문에, 신현중학교나 신현초등학교처럼 특정 학교의 시험 유형이나 진도에 딱 맞춰 지도받고 싶은 학생 입장에서는 아쉬운 부분이 생길 수밖에 없어요. 또한 맞벌이 가정이 많은 지역 특성상, 저녁 시간대에 아이를 학원까지 데려다주고 데려오는 게 부담스럽다는 이야기도 많이 들어요. 이런 상황에서 방문 과외 선생님을 구하려고 해도, 신현 지역까지 와줄 수 있는 선생님 자체가 한정적이라 조건에 맞는 분을 찾기가 더 어려워지는 악순환이 반복되곤 합니다. 결국 많은 학부모님들이 '이 동네에서만 찾으려니 답이 안 나온다'는 결론에 이르게 되고, 자연스럽게 지역 제약이 없는 방법을 찾아보게 되는 거예요. 특히 아파트 단지가 밀집한 신현동 특성상 비슷한 시간대에 여러 집이 동시에 선생님을 구하려고 하다 보니, 인기 있는 시간대는 금방 마감되고 남은 선택지 중에서 어쩔 수 없이 고르게 되는 경우도 흔합니다. 이런 경쟁 구조 자체가 학부모님 입장에서는 스트레스가 될 수밖에 없어요. 여기에 더해 신현동은 새 아파트 단지 입주가 이어지면서 인구 유입이 꾸준한 지역이라, 선생님을 구하려는 수요는 계속 늘어나는데 그만큼 공급이 따라가지 못하는 구조적인 문제도 있습니다. 이런 지역 특성을 알고 나면, 왜 유독 신현 지역 학부모님들이 선생님 구하기의 어려움을 더 크게 느끼시는지 이해가 되실 거예요. 이런 상황에서 학부모님들이 흔히 선택하는 차선책은 '일단 아무 학원이나 보내고 나중에 바꾸자'는 방식인데, 이 방식은 결국 아이가 맞지 않는 환경에서 시간을 허비하게 만드는 경우가 많습니다. 학원을 몇 달 다니다가 다시 다른 곳을 알아보는 과정이 반복되면, 그만큼 아이의 학습 흐름도 자주 끊기게 되고 부모님의 피로도도 함께 쌓여갑니다.</p>
    <h2>화상과외가 이 문제를 어떻게 해결해줄 수 있을까요</h2>
    <p>화상과외의 가장 큰 장점은 <strong>지역이라는 제약이 아예 사라진다는 것</strong>이에요. 신현 지역 안에서만 선생님을 찾을 필요 없이, 거제 전체는 물론 전국 단위로 조건에 맞는 선생님을 비교하고 선택할 수 있게 됩니다. 그만큼 아이 성향이나 학습 목표, 원하는 시간대에 정확히 맞는 선생님을 만날 확률이 훨씬 높아져요. 이동 시간이 없다는 것도 실질적으로 큰 차이를 만들어요. 학원이나 과외 장소까지 오가는 시간을 아낄 수 있으니, 그 시간만큼 아이가 쉬거나 다른 활동을 할 수 있는 여유가 생기고, 저녁 늦은 시간대에도 부담 없이 수업을 잡을 수 있어요. 맞벌이 가정이라면 부모님이 퇴근하고 돌아오는 시간에 맞춰 수업 시간을 조정하기도 훨씬 수월합니다. 또한 화상 수업은 대부분 녹화가 가능하기 때문에, 아이가 수업 중 놓친 부분이 있어도 나중에 다시 돌려보면서 복습할 수 있다는 것도 큰 장점이에요. 학부모님 입장에서도 아이가 어떤 방식으로 수업을 받는지 나중에 확인해볼 수 있어 안심이 된다는 반응이 많습니다. 여기에 더해, 화상과외는 선생님과 학생을 연결하는 과정 자체가 훨씬 체계적으로 이뤄질 수 있다는 것도 잘 알려지지 않은 장점이에요. 대면 과외는 소개나 지인 추천에 의존하는 경우가 많아 검증 과정이 느슨해지기 쉬운 반면, 화상과외 플랫폼을 통하면 학력·경력·신원 확인 절차를 거친 선생님들 중에서 선택할 수 있어 훨씬 안심하고 시작하실 수 있습니다. 아이 혼자 낯선 선생님과 처음 만나는 자리도, 온라인이라는 완충 공간이 있으면 심리적 부담이 훨씬 줄어든다는 점도 은근히 중요한 부분이에요. 처음 몇 번은 어색해하던 아이도 화면 너머로 관계를 쌓아가며 자연스럽게 마음을 여는 경우가 많습니다. 부모님이 옆에서 지켜볼 수 있다는 점도 화상과외이기 때문에 가능한 부분이에요. 대면 수업이라면 다른 방에서 진행되거나 학원에 보내고 나면 실제로 어떤 방식으로 수업이 이뤄지는지 확인하기 어려운 경우가 많은데, 화상 수업은 필요하다면 부모님도 함께 화면을 볼 수 있어 훨씬 투명하게 진행 상황을 파악할 수 있습니다. 이렇게 여러 장점이 겹치다 보니, 한 번 화상과외를 경험해본 학부모님들은 처음의 우려와 달리 오히려 대면 수업보다 만족도가 높다고 말씀하시는 경우가 많아요.</p>
    <h2>실제 상담에서 확인한 변화</h2>
    <p>상담을 진행하다 보면, 처음에는 화상 수업에 대해 반신반의하시던 학부모님들도 30분 무료체험수업을 한 번 경험해보시고 나면 생각이 많이 바뀌는 경우를 자주 봐요. 한 학부모님은 아이가 집중력이 짧아 대면 수업에서도 산만해지는 게 고민이었는데, 오히려 화면을 사이에 두고 1:1로 진행하다 보니 아이가 선생님 얼굴과 화면에 더 집중하게 되더라는 이야기를 해주셨어요. 또 다른 경우에는, 신현중학교 시험 범위에 맞춰 처음부터 학교 이름을 알려드리고 시작했더니, 선생님이 그 학교의 문제 유형을 미리 파악하고 수업을 준비해줘서 첫 수업부터 훨씬 효율적이었다는 후기도 있었습니다. 물론 모든 아이에게 똑같은 방식이 정답은 아니에요. 그래서 저희는 상담 단계에서 아이의 성향과 학습 습관을 먼저 충분히 파악하고, 그에 맞는 선생님을 연결해 드리는 것을 가장 중요하게 생각하고 있어요. <strong>일방적으로 화상과외를 권하기보다는, 아이에게 정말 맞는 방식인지부터 함께 확인하는 과정</strong>을 거치는 거예요. 상담 초반에 아이의 평소 학습 태도나 집중 시간, 좋아하는 학습 방식까지 여쭤보는 것도 이런 이유 때문이에요. 이 정보를 바탕으로 선생님을 연결해 드리면, 첫 수업부터 아이가 어색해하지 않고 훨씬 자연스럽게 적응하는 경우가 많습니다. 한 학부모님은 아이가 낯을 많이 가리는 성향이라 걱정이 크셨는데, 상담 때 이 부분을 미리 말씀해주신 덕분에 아이를 편하게 이끌어주는 스타일의 선생님을 연결해 드릴 수 있었고, 몇 주 지나지 않아 아이가 먼저 수업 시간을 기다리게 됐다는 후기를 들었어요. 이런 변화는 결국 선생님과 아이 사이의 궁합이 얼마나 중요한지를 잘 보여주는 사례예요. 성적이나 실력만 보고 매칭하는 것이 아니라, 아이의 성향까지 함께 고려해야 진짜 좋은 결과로 이어질 수 있다는 걸 이런 사례들을 통해 계속 확인하고 있습니다. 그래서 티치핏거제는 매칭 이후에도 첫 몇 주간은 아이 반응을 계속 살펴보고, 필요하다면 선생님을 조정해 드리는 것도 마다하지 않아요. 처음 연결이 완벽하지 않더라도, 계속 조율해나가면서 최선의 조합을 찾아가는 과정 자체를 중요하게 생각하기 때문입니다. 이런 사후 관리가 있고 없고의 차이는, 시간이 지날수록 학부모님이 체감하시는 만족도에서 크게 갈리는 부분이에요. 단순히 선생님을 연결해주는 것에서 끝나는 것이 아니라, 그 이후까지 함께 책임지는 자세가 결국 신뢰로 이어진다고 저희는 믿고 있습니다. 신현중학교·신현초등학교 학부모님들도 이런 세심한 관리를 직접 경험해보시면 왜 화상과외를 계속 이어가시는지 이해가 되실 거예요. 매칭은 시작일 뿐, 진짜 중요한 건 그 이후의 꾸준한 관리라는 걸 늘 마음에 새기고 있습니다.</p>
    <h2>화상과외 선생님을 고를 때 꼭 확인해야 할 것들</h2>
    <p>화상과외를 알아보실 때는 몇 가지를 꼭 확인해보시는 걸 추천드려요. 첫째, 선생님이 아이가 다니는 학교의 시험 유형이나 진도를 미리 파악하고 있는지예요. 신현중학교, 신현초등학교처럼 학교마다 시험 스타일이 다르기 때문에, 이 부분을 소홀히 하면 아무리 실력 있는 선생님이어도 효율이 떨어질 수 있어요. 둘째, 학력과 경력, 신원이 제대로 검증된 선생님인지 확인하는 것도 중요합니다. 온라인으로 진행되는 만큼, 처음 만나는 선생님에 대한 신뢰가 더욱 중요할 수밖에 없어요. 셋째, 정식으로 계약하기 전에 체험 수업으로 아이와의 궁합을 먼저 확인할 수 있는지도 꼭 물어보세요. 아무리 스펙이 좋은 선생님이어도 아이와 성향이 안 맞으면 오래가기 어렵거든요. 마지막으로, 수업 녹화나 진도 관리 같은 사후 관리 시스템이 있는지도 확인해보시면 좋아요. 이런 부분들을 꼼꼼히 따져보고 시작하시면, 화상과외를 선택했을 때 후회할 가능성을 크게 줄일 수 있습니다. 특히 처음 화상과외를 알아보시는 분이라면, 무료 상담이나 체험 수업을 제공하는지도 꼭 확인해보세요. 정식 계약 전에 아이가 직접 경험해볼 수 있는 기회가 있어야, 나중에 '생각했던 것과 다르다'는 아쉬움을 미리 막을 수 있습니다. 이렇게 여러 조건을 하나씩 따져보다 보면 시간이 꽤 걸릴 수 있는데, 처음부터 검증 절차와 체험 수업 제도를 갖춘 곳을 찾으면 이 과정 자체를 훨씬 단축할 수 있어요. 반대로 이런 기본적인 확인 절차 없이 시작하면, 나중에 문제가 생겼을 때 책임 소재가 불분명해지거나 환불·변경이 까다로워지는 경우도 있으니 계약 전에 관련 정책을 미리 물어보시는 것도 잊지 마세요. 이 네 가지만 꼼꼼히 짚어보셔도, 신현중학교·신현초등학교 학생에게 잘 맞는 선생님을 훨씬 안전하게 고르실 수 있을 거예요. 처음 한 번만 꼼꼼히 확인해두면, 그다음부터는 훨씬 편안한 마음으로 수업을 이어가실 수 있습니다.</p>
    <h2>티치핏거제와 함께라면 이런 점이 다릅니다</h2>
    <p>티치핏거제는 방문 과외나 입시 컨설팅 없이, <strong>오직 화상과외 하나에만 집중</strong>하고 있어요. 그 대신 그 안에서만큼은 정확도를 최대한 높이는 데 집중합니다. 상담 시 재학 중인 학교, 최근 학습 상태, 아이 성향까지 먼저 확인하고, 그에 맞는 선생님을 연결해 드려요. 모든 선생님은 학력·신원·경력 확인을 거친 뒤에만 매칭에 참여할 수 있고, 정식 신청 전에는 30분 무료체험수업으로 먼저 궁합을 확인해보실 수 있습니다. 체험 수업이 마음에 들 때만 정식으로 시작하시면 되기 때문에 부담 없이 시작해보실 수 있어요. 신청 후에는 24시간 이내에 담당자가 직접 연락드리고, 학습 진단부터 선생님 추천, 체험 수업까지 순서대로 안내해 드립니다. 신현중학교·신현초등학교뿐 아니라 거제 관내 초·중·고 72곳 전체 학생을 대상으로 매칭이 가능하니, 지금 다니는 학교를 알려주시면 그에 맞춰 상담해 드릴게요. 지금까지 여러 방법을 시도해보셨지만 만족스럽지 않으셨다면, 이번에는 화상과외로 한 번 다르게 접근해보시는 것도 좋은 선택이 될 수 있습니다. 신현동에 살면서도 신현 밖 지역까지 발품 팔며 선생님을 찾아다니실 필요 없이, 이제는 화면 하나로 훨씬 넓은 선택지를 만나보실 수 있어요. 아이에게 맞는 선생님을 찾는 일이 더 이상 어렵고 막막한 숙제가 아니라, 편안하게 시작할 수 있는 첫걸음이 되기를 바랍니다.</p>
    <p><strong>Q. 신현중학교, 신현초등학교 학생 모두 매칭 가능한가요?</strong><br>
    네, 두 학교 모두 매칭 가능하고 거제 관내 초·중·고 72곳 전체 학생을 대상으로 안내해 드려요.</p>
    <p><strong>Q. 화상 수업이 처음인데 아이가 잘 적응할 수 있을까요?</strong><br>
    생각보다 빠르게 적응하는 경우가 많아요. 30분 무료체험수업으로 먼저 아이 반응을 확인해보실 수 있습니다.</p>
    <p><strong>Q. 상담과 체험 수업도 비용이 드나요?</strong><br>
    아니요, 상담과 30분 체험 수업은 모두 무료이며, 체험 수업이 마음에 들 때만 정식으로 결정하시면 됩니다.</p>
    ''',
})

BLOG_POSTS.append({
    "slug": "geoje-jangpyeong-gimalgosa-daebi",
    "title": "장평중학교·장평고등학교 2학기 기말고사 대비, 화상과외로 준비하는 법",
    "date": "2026-09-24",
    "category": "중고등 시험대비",
    "teaser": "장평중학교·장평고등학교 학생 기준으로, 2학기 기말고사를 남은 기간 동안 어떻게 준비하면 좋을지 화상과외 활용법과 함께 정리했어요.",
    "body": '''
    <p>장평중학교나 장평고등학교에 다니는 자녀를 둔 학부모님이라면, 2학기 기말고사가 다가올수록 마음이 바빠지실 거예요. 2학기 기말고사는 한 해 학교생활을 마무리하는 시험이면서 동시에 다음 학년, 다음 학기 내신에도 영향을 미치기 때문에 부담이 클 수밖에 없습니다. 특히 장평중학교에서 장평고등학교로 이어지는 학생이라면, 중학교 마지막 시험과 고등학교 첫 학기 내신이 서로 이어진다는 느낌을 받는 경우도 많아요. 이 글에서는 장평중학교·장평고등학교 학생 기준으로, 2학기 기말고사를 남은 기간 동안 어떻게 준비하면 좋을지, 그리고 화상과외가 이 시기에 어떤 도움을 줄 수 있는지 구체적으로 정리해봤어요. 시험 준비 순서부터 실제 상담 사례까지 함께 담았으니 지금부터 계획을 세우는 데 참고해보세요.</p>
    <h2>장평중학교·장평고등학교 학생들이 2학기 기말고사를 유독 어려워하는 이유</h2>
    <p>2학기 기말고사는 1학기 기말고사보다 준비가 까다롭다고 느끼는 학생이 많아요. 우선 시험 범위 자체가 넓어지는 경우가 많고, 2학기 들어 배우는 단원들은 난이도가 한 단계 올라가는 경우가 대부분이라 이해가 부족한 상태로 시험을 맞이하면 당황하기 쉽습니다. 장평중학교 학생이라면 중학교 마지막 시험이라는 부담감까지 더해지고, 장평고등학교 학생이라면 고등학교 내신이 대학 입시에 미치는 영향을 실감하기 시작하는 시기라 심리적 부담이 더 커지는 편이에요. 게다가 2학기는 학교 행사나 수행평가가 몰리는 시기이기도 해서, 시험 공부에만 온전히 집중하기 어려운 환경이 만들어지기도 합니다. 이런 여러 요인이 겹치다 보니, 막상 시험 2~3주 전이 돼서야 부랴부랴 준비를 시작하는 경우가 많고, 그 결과 원하는 만큼 성과를 내지 못한 채 시험을 마치는 학생들도 적지 않아요. 그래서 2학기 기말고사는 다른 시험보다 더 이른 시점부터 계획적으로 준비하는 것이 특히 중요합니다. 게다가 겨울방학을 앞두고 있다 보니 아이들도 은근히 마음이 풀어지는 시기라, 집중력을 유지하기가 1학기보다 더 어렵다는 점도 무시할 수 없는 요인이에요. 방학이 얼마 남지 않았다는 생각에 긴장감이 떨어지면, 계획했던 만큼 진도를 못 나가고 시험 직전까지 밀리는 경우도 자주 발생합니다. 게다가 겨울방학 직전에는 학교에서도 다양한 행사와 활동이 늘어나는 시기라, 평소보다 공부에 쓸 수 있는 절대적인 시간 자체가 줄어드는 경향이 있어요. 이런 환경적 요인까지 고려하면, 2학기 기말고사는 다른 어떤 시험보다도 시간 관리가 중요한 시험이라고 볼 수 있습니다. 특히 장평고등학교 1학년이라면 이번 시험이 고등학교 첫 해를 마무리하는 시험이라, 앞으로의 내신 관리 습관을 결정짓는 중요한 분기점이 될 수 있어요. 이 시기에 만들어진 공부 방식이 2학년, 3학년까지 그대로 이어지는 경우가 많기 때문에 더욱 신중하게 접근할 필요가 있습니다.</p>
    <h2>지금부터 시작해야 하는 이유</h2>
    <p>기말고사 준비는 보통 시험 2주 전부터 본격적으로 시작하는 경우가 많지만, 2학기 기말고사만큼은 그보다 조금 더 여유 있게 준비를 시작하는 걸 추천드려요. 범위가 넓은 만큼 한 번에 몰아서 정리하기가 쉽지 않고, 특히 서술형 문항 비중이 높은 학교라면 개념을 정확한 문장으로 설명하는 연습까지 필요하기 때문에 시간이 더 걸릴 수밖에 없어요. 미리 시작하면 좋은 이유는 또 있어요. 시험 범위 전체를 여유 있게 한 바퀴 돌아본 다음, 마지막 1~2주는 취약한 부분만 집중적으로 다시 볼 수 있는 시간을 확보할 수 있다는 거예요. 반대로 늦게 시작하면 범위를 처음부터 끝까지 훑는 데만 시간을 다 써버려서, 정작 중요한 취약 단원을 깊이 있게 다질 시간이 부족해지는 경우가 많습니다. 장평중학교·장평고등학교처럼 시험 범위가 넓은 학교일수록, <strong>지금 이 시점에 미리 계획을 세우는 것 자체가 큰 차이</strong>를 만들어낼 수 있어요. 계획을 세울 때는 단순히 '하루에 몇 시간 공부하기'식으로 접근하기보다, 과목별로 시험 범위를 나누고 단원별 소요 시간을 예상해보는 것이 훨씬 효과적이에요. 이렇게 하면 남은 기간 동안 무엇을 우선순위로 둬야 할지 훨씬 명확해집니다. 계획을 세운 뒤에는 매주 진행 상황을 점검하는 시간을 따로 갖는 것도 중요해요. 처음 세운 계획대로 정확히 진행되지 않더라도, 중간중간 점검하면서 속도를 조절하면 시험 직전에 갑자기 당황하는 상황을 훨씬 줄일 수 있습니다. 계획표를 짤 때는 하루 이틀 여유분을 미리 남겨두는 것도 좋은 방법이에요. 예상치 못하게 진도가 늦어지거나 컨디션이 안 좋은 날이 생기더라도, 이 여유분 덕분에 전체 계획이 무너지지 않고 유지될 수 있습니다. 계획을 세우는 것 자체를 어려워하는 학생이라면, 처음에는 선생님이나 부모님이 큰 틀을 잡아주고 점차 스스로 계획을 조정해보게 하는 방식으로 넘어가는 것도 좋은 방법이에요. 이렇게 미리 계획을 세우고 시작하는 것만으로도, 시험을 대하는 아이의 마음가짐 자체가 한결 여유로워지는 걸 자주 확인하게 됩니다.</p>
    <h2>화상과외로 기말고사를 준비하면 좋은 점</h2>
    <p>화상과외의 장점은 아이의 현재 상태에 맞춰 진도를 자유롭게 조정할 수 있다는 데 있어요. 학원처럼 정해진 커리큘럼을 따라가는 게 아니라, 아이가 취약한 단원만 골라서 집중적으로 복습할 수 있기 때문에 한정된 시간을 훨씬 효율적으로 쓸 수 있습니다. 또한 장평 지역 안에서만 선생님을 찾으려면 선택지가 제한적일 수밖에 없는데, 화상과외라면 지역 제약 없이 장평중학교·장평고등학교 같은 학교를 지도해본 경험이 있는 선생님을 더 폭넓게 찾아볼 수 있어요. 이동 시간이 없다는 것도 시험 기간에는 특히 큰 도움이 돼요. 학원을 오가는 데 쓰던 시간을 그대로 공부 시간으로 확보할 수 있고, 저녁 늦은 시간대에도 유연하게 수업을 잡을 수 있어 학교 보충수업이나 수행평가 일정과 겹치지 않게 조정하기도 편합니다. 수업이 녹화된다는 점도 기말고사 준비에는 특히 유용해요. 한 번 배운 내용을 시험 직전까지 반복해서 다시 볼 수 있기 때문에, 벼락치기 복습에도 훨씬 효과적입니다. 또한 화상과외는 수업 시간 외에도 카카오톡이나 메신저로 간단한 질문을 주고받을 수 있는 경우가 많아서, 막힌 문제가 있을 때 다음 수업까지 기다리지 않고 바로 도움을 받을 수 있다는 점도 시험 기간에는 큰 힘이 됩니다. 학원이라면 다음 수업 시간까지 며칠을 기다려야 하는 경우가 많은데, 화상과외는 이런 시간 지연 없이 즉각적으로 궁금증을 해소할 수 있다는 것도 시험 직전에는 특히 체감되는 차이예요. 또한 시험 기간에는 평소보다 수업 횟수나 시간을 유동적으로 늘리는 것도 가능해서, 마지막 며칠은 매일 짧게라도 만나 최종 점검을 하는 식으로 밀도 있게 준비할 수 있다는 것도 화상과외만의 장점입니다. 이렇게 유연하게 수업 밀도를 조절할 수 있다는 점은, 정해진 시간표를 그대로 따라야 하는 학원 수업과 비교했을 때 시험 기간에 특히 크게 체감되는 차이예요. 여기에 더해 화상과외는 과목별로 필요한 만큼만 시간을 배분할 수 있어서, 취약 과목에는 시간을 더 쓰고 자신 있는 과목은 가볍게 점검하는 식으로 효율적으로 시간을 쓸 수 있습니다.</p>
    <h2>상담에서 자주 나오는 이야기</h2>
    <p>상담을 하다 보면 '지금 시작해도 늦지 않았을까요'라는 질문을 정말 많이 받아요. 결론부터 말씀드리면, 남은 기간이 얼마가 됐든 그 안에서 가장 효율적인 계획을 세우는 게 중요하지, 시작 시점 자체가 늦고 빠르고를 너무 걱정하실 필요는 없어요. 다만 남은 기간이 짧을수록 범위를 넓게 훑기보다는, 시험에 자주 나오는 핵심 단원과 아이가 유독 약한 부분부터 우선순위를 정해서 좁혀 들어가는 전략이 필요해집니다. 티치핏거제에서는 상담 시 재학 중인 학교와 남은 기간, 최근 학습 상태를 먼저 확인한 다음, 그에 맞는 현실적인 계획을 함께 세워드려요. 무리하게 전체 범위를 다 훑으려고 하기보다, 시험에서 실제로 점수 차이를 만들 수 있는 부분부터 짚어드리는 방식으로 접근하고 있습니다. <strong>막연히 열심히 하는 것보다, 어디에 시간을 써야 하는지 아는 것</strong>이 기말고사 준비에서는 훨씬 중요해요. 실제로 상담 중에 '아이가 열심히는 하는데 성적이 안 오른다'고 걱정하시는 학부모님들을 자주 만나는데, 대부분 시간을 쏟는 부분과 시험에서 실제로 중요한 부분이 어긋나 있는 경우였어요. 이 부분만 조정해도 눈에 띄게 달라지는 걸 자주 확인합니다. 그래서 상담 초반에는 성적표보다 오히려 아이가 평소 시험을 어떻게 준비해왔는지, 어떤 방식으로 공부하는 걸 편하게 느끼는지부터 여쭤보는 경우가 많아요. 이 정보가 이후 커리큘럼을 짜는 데 훨씬 중요한 기준이 되기 때문입니다. 남은 기간이 짧다고 해서 무조건 불리한 것도 아니에요. 오히려 짧은 기간 동안 명확한 목표를 갖고 집중하면, 애매하게 긴 시간을 들이는 것보다 더 좋은 결과로 이어지는 경우도 종종 있습니다. 중요한 건 기간의 길이가 아니라 그 시간을 얼마나 효율적으로 쓰느냐예요. 이런 이유로 상담을 망설이시는 학부모님들께는, 남은 기간이 짧다고 미리 포기하지 마시고 일단 현재 상황을 함께 점검해보시길 권해드리고 있어요. 생각보다 할 수 있는 게 많다는 걸 확인하시는 경우가 대부분입니다.</p>
    <h2>기말고사 준비, 이 순서로 진행하면 좋아요</h2>
    <p>먼저 시험 범위 전체를 훑으면서 아이가 이미 잘 아는 부분과 헷갈려하는 부분을 구분하는 것부터 시작하는 게 좋아요. 그 다음 헷갈려하는 부분 위주로 개념을 다시 짚고, 관련 문제를 풀면서 이해도를 확인합니다. 서술형 문항 비중이 높은 학교라면 이 단계에서 개념을 직접 문장으로 설명해보는 연습도 함께 하는 게 좋아요. 문제 풀이 단계에서는 학교 기출 스타일과 비슷한 유형의 문제를 반복해서 풀어보면서 실전 감각을 익히고, 시험 직전 1주일은 새로운 내용을 넓히기보다 지금까지 정리한 내용을 다시 확인하는 데 집중하는 게 효과적이에요. 이 흐름을 혼자 계획하고 실행하기가 쉽지 않기 때문에, 화상과외 선생님과 함께 이 순서를 따라가면 훨씬 수월하게 준비할 수 있습니다. 특히 아이 혼자서는 자신이 어디를 헷갈려하는지 정확히 파악하기 어려운 경우가 많은데, 옆에서 봐주는 선생님이 있으면 이 부분을 훨씬 빠르게 짚어낼 수 있어요. 이 순서대로 진행하되, 중간중간 모의 시험 형식으로 시간을 재고 풀어보는 연습도 함께 넣어주면 실전 감각을 키우는 데 도움이 됩니다. 시험장에서 시간 배분에 실패해 아는 문제를 못 푸는 경우도 생각보다 많기 때문이에요. 이런 실전 연습은 특히 서술형 문항이 있는 시험에서 더욱 중요한데, 시간에 쫓기면 아는 내용도 문장으로 정리하지 못하고 급하게 답을 적다가 감점되는 경우가 흔하기 때문입니다. 이 다섯 단계를 그대로 따라가지 못하더라도 괜찮아요. 중요한 건 순서 자체보다, 지금 내가 어느 단계에 있는지를 스스로 인식하면서 공부하는 습관이에요. 이 인식이 있는 학생과 없는 학생은 같은 시간을 공부해도 효율에서 큰 차이를 보입니다. 처음에는 이 흐름을 선생님이 옆에서 잡아주다가, 시험을 몇 번 거치면서 아이 스스로 이 순서를 체득하게 되는 것이 가장 이상적인 모습이라고 볼 수 있어요. 이렇게 한 번 익힌 공부 순서는 다음 시험, 그다음 시험에도 그대로 적용할 수 있는 든든한 자산이 됩니다.</p>
    <h2>티치핏거제와 함께 기말고사를 준비하면</h2>
    <p>티치핏거제는 상담 시 재학 중인 학교와 현재 학습 상태를 먼저 확인하고, 장평중학교·장평고등학교 같은 학교의 시험 스타일을 반영해서 선생님을 연결해 드려요. 모든 선생님은 학력·신원·경력 확인을 거친 뒤에만 매칭에 참여하고, 정식 신청 전에는 30분 무료체험수업으로 먼저 아이와의 궁합을 확인해보실 수 있습니다. 체험 수업이 마음에 들 때만 정식으로 시작하시면 되기 때문에 부담 없이 시작해보실 수 있어요. 신청 후 24시간 이내에 담당자가 직접 연락드리고, 남은 기간에 맞춰 현실적인 학습 계획부터 함께 세워드립니다. 장평중학교·장평고등학교뿐 아니라 거제 관내 초·중·고 72곳 전체 학생을 대상으로 매칭이 가능하니, 지금 다니는 학교를 알려주시면 그에 맞춰 상담해 드릴게요. 시험이 끝난 뒤에도 결과를 함께 돌아보고 다음 시험을 위한 방향을 다시 잡아드리기 때문에, 이번 한 번의 시험으로 끝나는 게 아니라 학기 전체를 놓고 꾸준히 관리받을 수 있다는 것도 티치핏거제만의 특징이에요. 시험 결과에 따라 다음 학기 커리큘럼도 함께 조정해 드리니, 한 번의 상담으로 끝나는 관계가 아니라 꾸준히 이어지는 학습 파트너로 생각해주시면 좋겠습니다. 장평중학교·장평고등학교 학생이라면 지금 바로 상담을 신청해서, 이번 기말고사부터 달라진 준비 과정을 경험해보시길 바랍니다.</p>
    <p><strong>Q. 장평중학교, 장평고등학교 모두 매칭 가능한가요?</strong><br>
    네, 두 학교 모두 매칭 가능하고 거제 관내 초·중·고 72곳 전체 학생을 대상으로 안내해 드려요.</p>
    <p><strong>Q. 기말고사가 얼마 안 남았는데 지금 신청해도 될까요?</strong><br>
    네, 신청 후 24시간 이내 담당자가 연락드리고 30분 무료체험수업부터 빠르게 진행해 드릴 수 있어요.</p>
    <p><strong>Q. 서술형 문항 비중이 높은 학교인데 화상으로도 잘 준비할 수 있을까요?</strong><br>
    네, 화면을 함께 보면서 개념을 직접 설명해보는 연습을 진행할 수 있어 서술형 대비에도 효과적이에요.</p>
    ''',
})

BLOG_POSTS.append({
    "slug": "geoje-hacheong-gwaoe-seonsaengnim",
    "title": "하청초등학교·하청중학교 과외 선생님 구하기 어려우셨죠? 화상과외로 해결하세요",
    "date": "2026-09-24",
    "category": "화상과외 소개",
    "teaser": "방문 선생님 구하기 어려운 하청 지역, 화상과외로 지역 제약 없이 선생님을 찾는 방법을 하청초등학교·하청중학교 기준으로 정리했어요.",
    "body": '''
    <p>하청초등학교나 하청중학교에 아이를 보내고 계신 학부모님이라면, 과외 선생님을 구하는 것 자체가 쉽지 않다는 걸 누구보다 잘 아실 거예요. 하청은 거제 안에서도 상대적으로 외곽에 위치한 지역이라, 방문 과외 선생님을 구하려고 해도 조건에 맞는 분을 찾기가 도심 지역보다 훨씬 어렵습니다. 학원도 선택지가 많지 않다 보니, 아이에게 맞는 학습 방법을 찾는 것 자체가 하나의 숙제처럼 느껴지실 수도 있어요. 이 글에서는 하청초등학교·하청중학교 학부모님들이 자주 겪는 이런 고민을, 화상과외로 어떻게 해결할 수 있는지 구체적으로 짚어드릴게요. 지역 때문에 선택지가 좁아진다고 느끼셨다면, 이 글이 실질적인 도움이 될 거예요. 실제 상담 사례를 바탕으로 정리했으니 끝까지 참고해보시고, 그동안 미뤄왔던 고민이 있으셨다면 이번 기회에 함께 해결해보셨으면 좋겠습니다.</p>
    <h2>하청 지역 학부모님들이 겪는 현실적인 고민</h2>
    <p>하청은 거제 시내와는 어느 정도 거리가 있는 지역이라, 방문 과외 선생님을 구하려고 하면 '거기까지 와줄 선생님이 있을까'라는 걱정부터 앞서는 경우가 많아요. 실제로 방문 과외 플랫폼이나 지역 커뮤니티에 글을 올려봐도, 조건에 맞는 선생님을 찾기까지 시간이 오래 걸리거나, 어렵게 구해도 교통비 부담 때문에 수업료가 높아지는 경우도 있습니다. 학원 역시 시내 지역에 비해 선택지가 한정적이다 보니, 아이 성향이나 학습 수준에 딱 맞는 곳을 찾기보다는 그나마 다닐 수 있는 곳을 선택하게 되는 경우가 많아요. 이런 상황이 반복되다 보면, 학부모님 입장에서는 '우리 아이는 사는 곳 때문에 선택지가 좁을 수밖에 없나'라는 아쉬움을 느끼게 되곤 합니다. 특히 하청초등학교에서 하청중학교로 올라가는 시기, 혹은 중학교 진학을 앞둔 시기처럼 학습 방향을 새로 잡아야 하는 시점에는 이런 고민이 더 크게 다가올 수밖에 없어요. 이 시기를 놓치면 다음 단계에서 필요한 준비를 제때 하지 못하고 넘어가게 되는 경우도 많기 때문에, 학부모님 입장에서는 더욱 답답하게 느껴지실 수밖에 없습니다. 게다가 어렵게 방문 선생님을 구했다 하더라도, 선생님 사정으로 갑자기 수업이 어려워지면 다시 처음부터 선생님을 찾아야 하는 상황이 반복되기도 해요. 이런 불안정함이 쌓이다 보면 아이의 학습 흐름 자체가 자주 끊기게 되는 것도 큰 문제입니다. 게다가 한 번 끊긴 학습 흐름을 다시 이어가려면, 새로운 선생님이 아이 수준을 파악하는 데만도 시간이 꽤 걸리기 때문에 결과적으로 시간과 비용 모두 낭비하게 되는 경우가 많아요. 이런 불안정한 상황이 반복되면 아이도 '또 선생님이 바뀌는구나'라는 생각에 새로운 사람에게 마음을 여는 것 자체를 조심스러워하게 되고, 결국 매번 처음부터 관계를 다시 쌓아야 하는 부담까지 더해집니다. 이런 경험이 쌓이다 보면 학부모님도 '이번엔 또 얼마나 갈까'라는 불안한 마음으로 새 선생님을 맞이하게 되고, 이런 불안정함 자체가 아이의 학습 동기에도 좋지 않은 영향을 줄 수 있어요.</p>
    <h2>지역이 학습 선택지를 제한해서는 안 되는 이유</h2>
    <p>아이가 어느 지역에 사는지는 학습 의지나 잠재력과는 아무 상관이 없어요. 하지만 현실적으로는 사는 곳에 따라 만날 수 있는 선생님의 수와 질이 크게 달라지는 게 사실입니다. 도심 지역 학생들은 다양한 선생님 중에서 비교하고 선택할 수 있는 반면, 하청처럼 상대적으로 외곽에 있는 지역 학생들은 애초에 선택할 수 있는 폭 자체가 좁아요. 이런 격차는 시간이 지날수록 학습 결과의 차이로 이어질 수 있기 때문에, 단순히 '어쩔 수 없는 일'로 받아들이기보다는 다른 방법을 찾아보는 게 필요합니다. 티치핏거제가 화상과외라는 방식에 집중하게 된 이유도 여기에 있어요. 사는 지역과 상관없이 모든 학생이 똑같이 넓은 범위에서 좋은 선생님을 만날 수 있어야 한다고 생각했기 때문이에요. <strong>지역이 아이의 학습 기회를 제한하는 요인이 되어서는 안 된다</strong>는 게 저희가 화상과외를 중심에 둔 가장 근본적인 이유입니다. 실제로 도심과 외곽 지역의 교육 격차는 여러 조사에서도 꾸준히 지적되는 문제이고, 이 격차를 줄이는 가장 현실적인 방법 중 하나가 바로 온라인·화상 기반의 학습 서비스라는 이야기도 많아요. 하청처럼 지리적으로 조금 떨어진 지역일수록 이런 변화의 혜택을 더 크게 체감하실 수 있습니다. 실제로 화상 기반 학습 서비스를 이용해본 지방 학부모님들 사이에서는 '이제야 사는 곳과 상관없이 공평하게 선택할 수 있게 됐다'는 반응이 많이 나오고 있어요. 티치핏거제가 굳이 방문 과외를 함께 운영하지 않고 화상과외 하나에만 집중하는 것도, 이런 지역 격차를 해소하는 데 조금이라도 더 힘을 싣기 위해서예요. 한 가지 방식에 집중함으로써 그 안에서의 매칭 정확도를 최대한 끌어올리는 것이, 결과적으로 하청처럼 여건이 어려운 지역 학생들에게 더 큰 도움이 된다고 믿고 있습니다. 여러 서비스를 어중간하게 운영하기보다, 한 가지를 제대로 해내는 것이 결국 학생들에게 더 실질적인 가치를 준다고 생각하기 때문이에요.</p>
    <h2>화상과외가 하청 지역 학생들에게 특히 유리한 이유</h2>
    <p>화상과외는 지역이라는 물리적 제약을 완전히 없애줘요. 하청에 살든 거제 시내에 살든, 화면 너머로 만나는 선생님의 질에는 차이가 없습니다. 오히려 방문이 어려운 지역일수록 화상과외를 통해 만날 수 있는 선생님의 폭이 훨씬 넓어진다는 장점이 있어요. 지역 제약이 없어지니 교통비 부담도 자연스럽게 사라지고, 그만큼 수업료도 더 합리적인 수준에서 결정될 수 있습니다. 이동 시간이 없다는 것도 하청처럼 거리가 있는 지역에서는 더 크게 체감되는 장점이에요. 방문 선생님이라면 이동 시간 때문에 수업 시간대가 제한될 수밖에 없는데, 화상이라면 그런 제약 없이 아이와 선생님 모두에게 편한 시간대를 자유롭게 정할 수 있습니다. 수업 녹화 기능도 유용해요. 학원이 멀어서 자주 오가기 어려운 지역일수록, 녹화된 수업을 다시 보면서 스스로 복습할 수 있다는 점이 학습 효과를 유지하는 데 큰 도움이 됩니다. 여기에 더해 화상과외는 날씨나 계절의 영향도 거의 받지 않아요. 눈이 오거나 비바람이 심한 날에도 이동 걱정 없이 정해진 시간에 수업을 진행할 수 있다는 것도, 지리적으로 여건이 덜 좋은 지역에서는 은근히 크게 체감되는 장점이에요. 방문 수업이었다면 날씨나 도로 사정으로 수업이 취소되거나 미뤄지는 일이 잦았을 텐데, 화상과외는 이런 외부 변수에 흔들리지 않고 꾸준한 학습 리듬을 유지할 수 있게 해줍니다. 겨울철 폭설이나 태풍철처럼 이동이 특히 어려운 시기에도, 화상과외라면 수업 공백 없이 꾸준히 이어갈 수 있다는 점이 하청처럼 지리적 여건이 상대적으로 불리한 지역에서는 더욱 큰 의미를 가집니다. 수업이 자주 취소되고 미뤄지면 결국 아이의 학습 리듬이 깨지기 마련인데, 이런 변수를 줄일 수 있다는 것만으로도 장기적으로는 큰 차이를 만들어낼 수 있어요. 꾸준함이야말로 학습에서 가장 중요한 요소 중 하나이기 때문에, 이런 안정성은 생각보다 훨씬 큰 의미를 갖습니다.</p>
    <h2>실제로 이런 변화가 있었어요</h2>
    <p>하청 지역 학부모님들과 상담을 하다 보면, 처음에는 '정말 화상으로도 제대로 배울 수 있을까'라는 의구심을 갖고 시작하시는 경우가 많아요. 그런데 30분 무료체험수업을 한 번 진행해보고 나면 반응이 확실히 달라지는 걸 자주 봐요. 한 학부모님은 그동안 방문 선생님을 구하지 못해 몇 달째 아이 학습을 미뤄왔는데, 화상과외로 전환한 뒤에는 오히려 조건에 딱 맞는 선생님을 빠르게 만날 수 있었다며 만족해하셨어요. 또 다른 사례에서는, 하청중학교 시험 범위에 맞춰 선생님이 미리 준비해온 자료로 수업을 진행하다 보니, 아이가 학교 수업에서 이해가 안 됐던 부분을 훨씬 수월하게 따라잡을 수 있었다는 후기도 있었습니다. 물론 모든 아이와 모든 상황에 정답처럼 맞는 방법은 없어요. 그래서 저희는 상담 단계에서 아이의 상황을 충분히 듣고, 화상과외가 정말 맞는 방법인지부터 함께 확인해 드리고 있습니다. 이런 사례들을 반복해서 접하다 보니, '지역이 멀어서 안 될 것 같다'는 걱정으로 상담을 망설이시는 분들께는 오히려 한 번 경험해보시길 권해드리고 싶어요. 생각보다 훨씬 자연스럽게 적응하는 아이들이 많습니다. 한 학부모님은 처음 문의하실 때 '거리가 있어서 안 될 것 같은데 혹시 가능하냐'고 조심스럽게 물어보셨는데, 상담 후 화상과외로 진행하면서는 오히려 방문 선생님을 구할 때보다 더 다양한 선생님을 비교해볼 수 있어 만족스러워하셨어요. 이런 이야기를 들을 때마다, 처음의 막연한 걱정이 실제로는 크게 문제 되지 않는다는 걸 다시 한번 확인하게 됩니다. 중요한 건 얼마나 신중하게 선생님을 매칭해 드리느냐이지, 물리적인 거리가 아니라는 걸 상담을 거듭할수록 더 확신하게 돼요. 이런 사례들이 하나둘 쌓이면서, 저희 역시 지역과 상관없이 모든 학생에게 동일한 수준의 매칭을 제공할 수 있다는 확신을 갖고 서비스를 이어가고 있습니다. 앞으로도 하청을 비롯한 거제 곳곳의 학생들에게 이런 경험을 꾸준히 전해드리고 싶습니다. 사는 곳이 어디든 아이가 필요로 하는 도움을 제때 받을 수 있어야 한다는 원칙을, 앞으로도 계속 지켜나가려고 합니다. 이 원칙이 지켜지는 한, 지역이라는 이유로 망설이실 필요는 전혀 없습니다.</p>
    <h2>하청 지역에서 과외를 알아볼 때 확인하면 좋은 것들</h2>
    <p>먼저 선생님이 온라인 수업 경험이 충분한지 확인해보세요. 화상 수업은 대면 수업과는 다른 노하우가 필요하기 때문에, 처음 화상 수업을 시도하는 선생님보다는 어느 정도 경험이 쌓인 선생님이 더 안정적으로 진행할 수 있어요. 둘째, 아이가 다니는 학교의 시험 유형이나 진도를 파악하고 있는 선생님인지도 중요합니다. 하청초등학교, 하청중학교처럼 학교마다 특성이 다르기 때문에, 이 부분을 미리 확인하고 시작하는 선생님과 그렇지 않은 선생님 사이에는 수업 효율 차이가 클 수밖에 없어요. 셋째, 정식 계약 전에 체험 수업으로 아이와의 궁합을 먼저 확인할 수 있는지도 꼭 확인해보세요. 마지막으로, 인터넷 환경이나 수업용 기기 세팅에 대한 안내를 미리 받을 수 있는지도 체크해보시면 좋아요. 처음 화상 수업을 시작할 때는 이런 기본적인 준비가 잘 되어 있어야 수업 자체에 아이가 더 집중할 수 있습니다. 이 외에도 수업 중 문제가 생겼을 때 빠르게 대응해줄 수 있는 담당자가 따로 있는지도 확인해보시면 좋아요. 선생님과 직접 연결만 해주고 끝나는 방식보다는, 중간에서 계속 관리해주는 창구가 있는 편이 문제가 생겼을 때 훨씬 든든합니다. 특히 하청처럼 방문 상담이 쉽지 않은 지역일수록, 전화나 메신저로도 충분히 소통할 수 있는 담당자가 있는지 확인해보시면 훨씬 안심하고 진행하실 수 있어요. 이런 확인 절차가 번거롭게 느껴지실 수도 있지만, 처음에 조금만 꼼꼼히 살펴보면 이후 몇 달, 몇 년을 훨씬 편안하게 이용하실 수 있으니 아깝지 않은 시간 투자라고 생각해주시면 좋겠습니다. 이런 기준들을 하나씩 확인해가다 보면, 자연스럽게 믿을 수 있는 곳과 그렇지 않은 곳이 구분되실 거예요. 처음 시작할 때 조금만 신경 써서 확인하시면, 이후 과정은 훨씬 안심하고 맡기실 수 있습니다. 이 네 가지 기준을 기억해두셨다가, 어떤 화상과외 서비스든 상담받으실 때 하나씩 확인해보시길 권해드려요.</p>
    <h2>티치핏거제와 함께라면</h2>
    <p>티치핏거제는 하청처럼 방문 선생님을 구하기 어려운 지역의 학생들도 거제 시내 학생과 동일한 조건에서 선생님을 만날 수 있도록, 처음부터 화상과외 하나에 집중해왔어요. 상담 시 재학 중인 학교와 사는 지역, 아이 성향까지 먼저 확인하고 그에 맞는 선생님을 연결해 드립니다. 모든 선생님은 학력·신원·경력 확인을 거친 뒤에만 매칭에 참여하고, 정식 신청 전에는 30분 무료체험수업으로 먼저 궁합을 확인해보실 수 있어요. 신청 후 24시간 이내 담당자가 직접 연락드리고, 학습 진단부터 선생님 추천, 체험 수업까지 순서대로 안내해 드립니다. 하청초등학교·하청중학교뿐 아니라 거제 관내 초·중·고 72곳 전체 학생을 대상으로 매칭이 가능하니, 지금 다니는 학교를 알려주시면 그에 맞춰 상담해 드릴게요. 사는 지역이 어디든 관계없이 똑같은 조건에서 상담받으실 수 있으니, 그동안 지역 때문에 미뤄왔던 고민이 있으셨다면 이번 기회에 편하게 문의해보시길 권해드려요. 아이의 학습만큼은 사는 곳으로 인해 뒤처지지 않도록, 저희가 곁에서 꾸준히 함께하겠습니다. 지역이라는 벽 없이, 아이에게 정말 필요한 선생님을 만나는 경험을 하청 지역 학부모님들께도 똑같이 전해드리고 싶습니다. 지금까지 여건 때문에 망설이셨다면, 이번엔 한번 편하게 문의해보세요.</p>
    <p><strong>Q. 하청초등학교, 하청중학교 학생 모두 매칭 가능한가요?</strong><br>
    네, 두 학교 모두 매칭 가능하고 거제 관내 초·중·고 72곳 전체 학생을 대상으로 안내해 드려요.</p>
    <p><strong>Q. 인터넷 환경이 안 좋은 편인데 화상 수업이 가능할까요?</strong><br>
    상담 시 사용 환경을 먼저 확인해 드리고, 필요한 준비사항을 미리 안내해 드리니 걱정 안 하셔도 돼요.</p>
    <p><strong>Q. 방문 과외보다 비용 부담이 줄어드나요?</strong><br>
    지역에 따른 교통비 부담이 없어지기 때문에, 상황에 따라 더 합리적인 조건으로 진행할 수 있어요. 정확한 비용은 상담 시 안내해 드립니다.</p>
    ''',
})

BLOG_POSTS.append({
    "slug": "geoje-yeoncho-naeshin-gwanli",
    "title": "연초중학교·연초고등학교 내신관리, 시험 한 달 전부터 이렇게 준비하세요",
    "date": "2026-09-24",
    "category": "중고등 내신관리",
    "teaser": "연초중학교·연초고등학교 학생 기준으로, 내신관리를 시험 한 달 전부터 어떻게 계획적으로 준비하면 좋을지 정리했어요.",
    "body": '''
    <p>연초중학교나 연초고등학교에 다니는 자녀를 둔 학부모님이라면, 내신관리라는 말이 주는 부담감을 누구보다 잘 아실 거예요. 특히 연초고등학교처럼 대학 입시와 직결되는 시기에 접어든 학생이라면, 시험 하나하나가 그냥 지나가는 시험이 아니라 앞으로의 진로와 연결된다는 생각에 부담이 더 클 수밖에 없습니다. 그런데 막상 '내신관리를 어떻게 시작해야 하냐'고 물으면, 명확한 답을 갖고 계신 학부모님은 생각보다 많지 않아요. 이 글에서는 연초중학교·연초고등학교 학생 기준으로, 내신관리를 시험 한 달 전부터 어떻게 계획적으로 준비하면 좋을지 구체적으로 정리해봤어요. 서술형 대비부터 수행평가 일정 조율까지, 실제 상담에서 다루는 내용을 바탕으로 정리했으니 꼭 끝까지 참고해보시고 지금부터 계획을 세워보시길 바랍니다.</p>
    <h2>내신관리, 왜 시험 한 달 전부터 시작해야 할까요</h2>
    <p>많은 학생들이 내신관리를 '시험 기간에 열심히 공부하는 것'으로 생각하는 경우가 많아요. 하지만 진짜 내신관리는 시험 범위가 발표되기 전, 평소 수업 시간부터 시작됩니다. 그럼에도 현실적으로 본격적인 준비는 시험 한 달 전부터 시작하는 게 효과적이에요. 한 달이라는 시간이 있으면 범위 전체를 한 번 훑어보고, 취약한 부분을 파악한 다음, 그 부분을 집중적으로 보완할 시간까지 확보할 수 있기 때문입니다. 반대로 2주 전에 시작하면 범위를 훑는 데만 시간을 다 쓰게 되고, 정작 취약한 부분을 깊이 있게 다질 시간은 부족해지는 경우가 많아요. 연초중학교, 연초고등학교처럼 시험 범위가 넓거나 서술형 비중이 높은 학교라면 이 차이가 더 크게 나타납니다. 한 달 전부터 계획적으로 준비한 학생과 2주 전부터 급하게 시작한 학생은, 같은 시간을 공부해도 결과에서 차이가 날 수밖에 없어요. 특히 여러 과목을 동시에 준비해야 하는 중간·기말고사 특성상, 한 달이라는 여유가 있어야 과목별로 시간을 적절히 배분할 수 있습니다. 시간이 촉박하면 결국 좋아하는 과목이나 자신 있는 과목 위주로만 공부하게 되고, 정작 취약한 과목은 손도 못 대고 시험을 맞이하는 경우가 많아요. 이런 패턴이 몇 번 반복되면 특정 과목에 대한 자신감 자체가 떨어지고, 그 과목을 점점 더 피하게 되는 악순환으로 이어질 수 있기 때문에 초반에 이 흐름을 끊어주는 게 중요합니다. 한 달이라는 기간을 확보하면 이런 악순환이 생기기 전에 미리 손을 쓸 수 있다는 점에서도 의미가 커요. 취약 과목에 조금이라도 더 시간을 투자할 여유가 생기기 때문에, 자신감을 잃기 전에 격차를 줄일 수 있는 기회가 되는 셈입니다. 결국 내신관리는 시험 점수를 잘 받는 것을 넘어서, 아이가 특정 과목에 대한 자신감을 잃지 않도록 지켜주는 과정이기도 합니다. 이런 시각으로 접근하면 내신관리가 단순히 성적을 위한 것이 아니라, 아이의 전반적인 학습 태도를 지켜주는 일이라는 걸 알 수 있어요.</p>
    <h2>연초중학교·연초고등학교 학생들이 내신관리에서 자주 놓치는 부분</h2>
    <p>상담을 하다 보면 학생들이 내신관리를 할 때 가장 많이 놓치는 부분이 '서술형 대비'예요. 객관식 문제는 어느 정도 반복 학습으로 대비가 되지만, 서술형은 개념을 정확하게 이해하고 그것을 문장으로 표현할 수 있어야 하기 때문에 준비 방식이 달라야 해요. 특히 연초고등학교처럼 고등학교 내신은 중학교보다 서술형 비중이 높아지는 경우가 많아서, 중학교 때 방식 그대로 준비하다가는 낭패를 보기 쉽습니다. 또 하나 자주 놓치는 부분은 '수행평가와 지필고사의 균형'이에요. 지필고사 공부에만 집중하다가 수행평가를 놓치거나, 반대로 수행평가에 신경 쓰다가 지필고사 준비 시간을 놓치는 경우가 생각보다 많아요. 두 가지를 동시에 챙기려면 미리 학기 전체 일정을 파악하고, 시기별로 우선순위를 정해서 움직이는 게 중요합니다. 이런 부분들은 아이 혼자 챙기기 어려운 경우가 많아서, 옆에서 함께 계획을 세워주는 사람이 있으면 훨씬 수월해져요. 실제로 상담을 해보면, 성적이 잘 안 나오는 이유가 이해력 부족이 아니라 이런 일정 관리 실패인 경우도 생각보다 많았어요. 개념은 충분히 이해하고 있는데 시험 직전에 몰아서 준비하다 보니 실수가 잦아지고, 결과적으로 아는 문제도 틀리는 안타까운 상황이 반복되는 거예요. 이런 경우일수록 일정 관리 자체를 함께 짚어주는 것만으로도 성적이 눈에 띄게 안정되는 걸 자주 확인하게 됩니다. 아이 스스로는 문제라고 인식하지 못하는 부분을 옆에서 짚어주는 것만으로도 큰 변화가 시작되는 경우가 많아요. 서술형과 수행평가, 두 가지 모두 결국 '미리 계획하고 준비하는 습관'이 핵심이라는 공통점이 있어요. 이 습관을 한 번 제대로 잡아두면, 이후 시험에서는 훨씬 수월하게 같은 흐름을 반복할 수 있게 됩니다. 반대로 이 습관이 잡히지 않은 채 학년이 올라가면, 시험 범위와 과목 수가 늘어날수록 관리해야 할 것들이 기하급수적으로 많아져 더 큰 어려움을 겪게 될 수 있어요.</p>
    <h2>화상과외로 내신관리하면 좋은 점</h2>
    <p>화상과외의 가장 큰 장점은 아이의 학교, 학년, 현재 상태에 딱 맞춰 커리큘럼을 짤 수 있다는 거예요. 학원처럼 정해진 진도를 따라가는 게 아니라, 연초중학교·연초고등학교의 시험 범위와 스타일에 맞춰 그때그때 필요한 부분을 집중적으로 다룰 수 있습니다. 서술형 대비가 필요하다면 개념을 직접 설명해보는 연습을 함께 하고, 수행평가 준비가 필요한 시기라면 그에 맞춰 학습 비중을 조정할 수도 있어요. 지역 제약이 없다는 것도 큰 장점이에요. 연초 지역 안에서만 선생님을 찾으려면 선택지가 한정적일 수밖에 없는데, 화상과외라면 연초중학교·연초고등학교 같은 학교를 지도해본 경험이 있는 선생님을 더 폭넓게 만나볼 수 있습니다. 게다가 수업이 녹화되기 때문에, 시험 직전까지 배운 내용을 반복해서 복습할 수 있다는 것도 내신관리에는 특히 유용한 부분이에요. 학원처럼 정해진 시간표에 아이를 맞추는 게 아니라, 아이의 학교·학원 일정에 맞춰 수업 시간을 조정할 수 있다는 점도 내신관리 기간에는 큰 도움이 됩니다. 특히 시험 직전에는 과목별로 짧게라도 여러 번 수업을 넣어 집중적으로 점검하는 방식도 가능해요. 이렇게 유연하게 시간을 쪼개 쓸 수 있다는 것 자체가, 정해진 틀 안에서만 움직이는 학원 수업과 가장 크게 다른 점이라고 볼 수 있습니다. 여기에 더해 화상과외는 과목별로 다른 선생님을 연결받는 것도 자유로워서, 국어는 서술형에 강한 선생님, 수학은 개념 설명이 꼼꼼한 선생님처럼 과목 특성에 맞춰 조합할 수 있다는 것도 내신관리에는 실질적인 도움이 됩니다. 이렇게 과목별 강점이 다른 선생님들을 자유롭게 조합할 수 있다는 것 자체가, 한 곳에서 모든 과목을 해결해야 하는 학원과 비교했을 때 화상과외가 가진 뚜렷한 강점이라고 볼 수 있어요. 아이에게 맞는 조합을 찾는 데는 시간이 조금 걸릴 수 있지만, 한 번 잘 맞는 조합을 찾으면 그 효과는 꽤 오래 지속됩니다. 이런 유연함이 결국 내신관리의 효율을 크게 끌어올리는 핵심 요소가 됩니다.</p>
    <h2>내신관리, 이렇게 계획을 세워보세요</h2>
    <p>시험 한 달 전에는 먼저 전체 범위를 훑으면서 이미 아는 부분과 헷갈리는 부분을 구분하는 것부터 시작하세요. 3주 전부터는 헷갈리는 부분 위주로 개념을 다시 짚고, 관련 문제를 풀면서 이해도를 점검합니다. 서술형 비중이 높은 과목이라면 이 시기에 개념을 문장으로 설명해보는 연습도 함께 진행하는 게 좋아요. 2주 전부터는 학교 기출 스타일과 비슷한 문제를 반복해서 풀어보면서 실전 감각을 키우고, 마지막 1주는 새로운 내용을 넓히기보다 지금까지 정리한 내용을 확실히 다지는 데 집중하세요. 이 흐름을 아이 혼자 계획하고 실행하기는 생각보다 어려운데, <strong>옆에서 방향을 잡아주는 선생님이 있으면 훨씬 안정적으로 따라갈 수 있어요</strong>. 티치핏거제에서는 상담 시 이 계획을 아이 상황에 맞춰 함께 세워드리고 있습니다. 계획표는 한 번 세우고 끝나는 게 아니라, 중간중간 진행 상황을 점검하면서 조정하는 과정도 중요해요. 처음 세운 계획대로 100% 진행되는 경우는 드물기 때문에, 유연하게 우선순위를 재조정할 수 있는 사람이 옆에 있는 것 자체가 큰 도움이 됩니다. 특히 학교 진도가 예상보다 빠르거나 느리게 나가는 경우도 종종 있는데, 이런 변화에 맞춰 계획을 실시간으로 조정할 수 있어야 시험 직전에 허둥대지 않을 수 있어요. 계획을 세우는 습관 자체가 처음에는 낯설고 번거롭게 느껴질 수 있지만, 몇 번 반복하다 보면 아이 스스로도 다음 시험을 어떻게 준비해야 할지 감을 잡아가는 경우가 많습니다. 이런 자기주도적인 계획 습관은 결국 대학에 가서도, 사회에 나가서도 계속 쓰이는 능력이기 때문에 지금 시기에 잘 만들어두는 것이 장기적으로 큰 자산이 됩니다. 당장의 시험 점수보다 이런 습관을 만드는 과정 자체에 더 큰 가치를 두고 접근해주시면 좋겠습니다. 시험이 끝난 뒤에도 이 습관은 그대로 남아 다음 학기, 다음 학년까지 계속 힘을 발휘하게 됩니다. 결국 지금 들이는 노력이 앞으로의 모든 시험에 조금씩 이자처럼 쌓여 돌아온다고 생각해주시면 좋겠어요.</p>
    <h2>연초고등학교 학생이라면 특히 신경 써야 할 것</h2>
    <p>고등학교 내신은 중학교와 달리 대학 입시와 직접 연결되기 때문에, 등급 하나하나에 대한 부담이 훨씬 커요. 그렇다고 해서 매 시험마다 과도하게 긴장하며 준비하는 것도 장기적으로는 좋은 방법이 아닙니다. 중요한 건 한 시험 한 시험에 일희일비하기보다, 학기 전체를 놓고 꾸준히 관리하는 자세예요. 연초고등학교 학생이라면 특히 1학년 때부터 내신관리 습관을 잘 잡아두는 게 중요한데, 이 시기에 만들어진 공부 방식이 2학년, 3학년까지 그대로 이어지는 경우가 많기 때문이에요. 또한 수능을 함께 준비해야 하는 시기가 다가올수록, 내신 공부와 수능 공부를 어떻게 병행할지도 미리 고민해두는 게 좋습니다. 티치핏거제는 상담 시 학년과 목표를 함께 확인해서, 지금 당장의 내신관리뿐 아니라 앞으로의 방향까지 고려한 커리큘럼을 제안해 드려요. 1학년 때부터 이런 흐름을 잡아두면 2학년, 3학년으로 올라갈수록 오히려 더 여유 있게 준비할 수 있게 되는 경우가 많으니, 지금 이 시기를 놓치지 않는 게 중요합니다. 학년이 올라갈수록 내신과 수능을 함께 챙겨야 하는 부담이 커지기 때문에, 미리 좋은 습관을 만들어두는 학생과 그렇지 않은 학생의 차이는 시간이 갈수록 더 벌어지는 경향이 있어요. 그래서 저희는 상담 시 단순히 이번 시험만 보는 게 아니라, 앞으로 몇 학기를 어떻게 끌고 갈지까지 함께 그려보는 것을 중요하게 생각하고 있습니다. 연초고등학교 학생이라면 지금부터라도 이런 장기적인 시각으로 내신관리를 시작해보시길 권해드려요. 매 학기 조금씩 쌓이는 이런 관리가 결국 큰 차이를 만들어낸다는 걸 잊지 않으셨으면 합니다. 연초고등학교뿐 아니라 연초중학교 학생이라면 지금부터 미리 이런 습관을 잡아두는 것도 좋은 방법이 될 수 있어요. 학년에 상관없이, 지금이 바로 시작하기 가장 좋은 시점이라는 걸 꼭 말씀드리고 싶습니다. 오늘 시작한 작은 습관 하나가 3년 뒤 입시 결과를 바꿀 수도 있다는 마음으로 함께해주시면 좋겠어요.</p>
    <h2>티치핏거제와 함께 내신관리를 시작해보세요</h2>
    <p>티치핏거제는 상담 시 재학 중인 학교와 최근 시험 결과, 학습 습관까지 확인하고, 연초중학교·연초고등학교 같은 학교의 시험 스타일을 반영해서 선생님을 연결해 드려요. 모든 선생님은 학력·신원·경력 확인을 거친 뒤에만 매칭에 참여하고, 정식 신청 전에는 30분 무료체험수업으로 먼저 궁합을 확인해보실 수 있습니다. 체험 수업이 마음에 들 때만 정식으로 시작하시면 되기 때문에 부담 없이 시작해보실 수 있어요. 신청 후 24시간 이내에 담당자가 직접 연락드리고, 남은 기간과 목표에 맞춰 현실적인 계획부터 함께 세워드립니다. 연초중학교·연초고등학교뿐 아니라 거제 관내 초·중·고 72곳 전체 학생을 대상으로 매칭이 가능하니, 지금 다니는 학교를 알려주시면 그에 맞춰 상담해 드릴게요. 내신관리는 한 번의 시험이 아니라 학기 전체, 나아가 고등학교 3년 전체를 놓고 보는 관리라는 생각으로 함께 준비해 드리겠습니다. 지금 시험 준비가 막막하게 느껴지신다면, 우선 상담을 통해 아이의 현재 상태부터 편하게 확인해보시길 추천드려요. 한 달이라는 시간을 제대로 활용하는 것만으로도 결과는 충분히 달라질 수 있습니다. 지금 이 글을 읽고 계신다면, 이미 절반은 준비가 시작된 셈이니 나머지는 저희와 함께 채워나가시면 됩니다. 연초중학교·연초고등학교 학생 모두, 지금 바로 편하게 상담을 신청해보세요.</p>
    <p><strong>Q. 연초중학교, 연초고등학교 모두 매칭 가능한가요?</strong><br>
    네, 두 학교 모두 매칭 가능하고 거제 관내 초·중·고 72곳 전체 학생을 대상으로 안내해 드려요.</p>
    <p><strong>Q. 내신관리는 몇 학년부터 시작하는 게 좋을까요?</strong><br>
    빠를수록 좋지만, 지금 학년이 몇 학년이든 현재 상태를 먼저 진단한 뒤 그에 맞는 계획을 세워드리니 늦었다고 걱정하지 않으셔도 돼요.</p>
    <p><strong>Q. 수행평가 준비도 함께 도와주나요?</strong><br>
    네, 상담 시 학기 일정을 확인해서 지필고사와 수행평가 준비 시기를 함께 조율해 드려요.</p>
    ''',
})

BLOG_POSTS.append({
    "slug": "geoje-neungpo-jungang-seonhaeng",
    "title": "능포초등학교·거제중앙초등학교 선행학습, 무리하지 않고 시작하는 방법",
    "date": "2026-09-24",
    "category": "초등 선행학습",
    "teaser": "능포초등학교·거제중앙초등학교 학생 기준으로, 선행학습을 무리하지 않고 아이 속도에 맞게 시작하는 방법을 정리했어요.",
    "body": '''
    <p>능포초등학교나 거제중앙초등학교에 아이를 보내고 계신 학부모님 중에는, 선행학습을 언제 어떻게 시작해야 할지 고민하시는 분들이 많아요. 주변에서 선행학습 이야기가 들리기 시작하면 조급한 마음이 들기 마련이지만, 무작정 진도만 빨리 나간다고 해서 아이에게 좋은 결과로 이어지는 건 아니에요. 오히려 준비 없이 서두른 선행학습이 아이에게 부담만 주고 끝나는 경우도 적지 않습니다. 이 글에서는 능포초등학교·거제중앙초등학교 학생 기준으로, 선행학습을 무리하지 않고 시작하는 방법을 구체적으로 정리해봤어요. 시작 시점을 판단하는 기준부터 실제 상담 사례까지 함께 담았으니, 선행학습을 고민 중이시라면 꼭 참고해보시고 아이에게 맞는 시점을 여유롭게 함께 찾아보시길 바랍니다. 조급해하지 않으셔도 괜찮아요.</p>
    <h2>선행학습, 무작정 시작하면 오히려 역효과가 날 수 있어요</h2>
    <p>선행학습의 목적은 다음 학년 내용을 미리 익혀서 여유를 갖는 거예요. 그런데 현재 학년 내용도 제대로 소화하지 못한 상태에서 선행부터 시작하면, 오히려 두 가지를 동시에 어려워하는 상황이 생길 수 있습니다. 지금 배우는 내용도 헷갈리는데 다음 학년 내용까지 얹으면, 아이 입장에서는 이해하지 못한 채로 진도만 나가는 셈이 되고, 결국 선행한 내용도 실제로 그 학년이 됐을 때 다시 배워야 하는 경우가 많아요. 게다가 준비 없이 시작한 선행학습은 아이에게 '나는 공부를 못하는구나'라는 부정적인 인식을 심어줄 위험도 있습니다. 이해가 안 되는 상태로 진도만 계속 나가다 보면, 아이는 점점 자신감을 잃고 공부 자체에 흥미를 잃을 수 있어요. 그래서 선행학습을 시작하기 전에는 반드시 현재 학년 개념이 얼마나 탄탄한지부터 점검하는 과정이 필요합니다. 주변 이야기만 듣고 조급하게 시작하기보다, 우리 아이만의 속도와 상태를 먼저 객관적으로 파악하는 게 순서예요. 같은 학년이라도 아이마다 이해 속도와 흥미를 느끼는 부분이 다르기 때문에, 옆집 아이의 진도를 기준으로 삼는 것 자체가 애초에 맞지 않는 비교일 수 있습니다. 다른 아이와 비교하기보다, 지난달의 우리 아이와 지금의 우리 아이를 비교하는 것이 훨씬 건강한 기준이 될 수 있어요. 이 순서를 건너뛰고 진도부터 나가면, 나중에 다시 되돌아가서 기초를 채워야 하는 이중 작업이 발생할 수 있습니다. 결국 시간과 비용을 두 번 들이는 셈이 되는 거예요. 그래서 조급한 마음이 들수록 오히려 한 박자 늦추고, 아이의 현재 상태를 먼저 냉정하게 점검해보는 여유가 필요합니다. 주변 아이들의 진도에 휘둘리기보다, 우리 아이가 지금 무엇을 확실히 이해하고 있고 무엇을 어려워하는지부터 파악하는 것이 선행학습의 진짜 출발점이라는 걸 꼭 기억해주셨으면 해요. 이 점검 과정을 건너뛰지 않는 것이 결국 선행학습을 성공적으로 이어가는 첫 단추라고 볼 수 있습니다.</p>
    <h2>능포초등학교·거제중앙초등학교 학생이라면 이 순서를 추천해요</h2>
    <p>먼저 아이의 현재 학년 이해도를 정확히 파악하는 것부터 시작하세요. 단순히 성적으로만 판단하기보다, 개념을 스스로 설명할 수 있는지 확인해보는 게 좋아요. 만약 현재 학년 개념에 구멍이 있다면, 선행보다는 그 부분을 먼저 채우는 게 우선입니다. 현재 학년 개념이 탄탄하다고 판단되면, 그때부터 다음 학년 내용을 조금씩 얹어가는 방식으로 진행하세요. 이때도 한 번에 많은 진도를 나가기보다는, 아이가 소화할 수 있는 만큼 천천히 진행하는 게 중요합니다. 능포초등학교, 거제중앙초등학교처럼 학교마다 학습 분위기와 진도 체감이 다르기 때문에, 재학 중인 학교를 먼저 확인하고 그에 맞춰 속도를 조절하는 것도 중요한 부분이에요. 저학년이라면 선행보다 학습 습관을 먼저 잡는 데 집중하고, 고학년이라면 중학교와 연결되는 개념을 의식하면서 선행을 진행하는 게 좋습니다. 예를 들어 수학이라면 분수와 소수 개념이 확실히 잡혀 있어야 이후 비와 비율, 방정식으로 자연스럽게 넘어갈 수 있어요. 이런 연결 고리를 미리 알고 있는 선생님과 함께라면, 어느 시점에 무엇을 먼저 다져야 할지 훨씬 명확하게 계획할 수 있습니다. 반대로 이런 흐름을 모르고 무작정 진도만 나가는 선행학습은, 당장은 앞서가는 것처럼 보여도 나중에 개념 사이의 연결이 끊긴 채로 남아있을 위험이 있어요. 국어나 영어도 마찬가지예요. 읽기 독립이 안 된 상태에서 어려운 지문으로 선행을 시키면 오히려 책 읽기 자체를 싫어하게 될 수 있으니, 과목마다 꼭 필요한 선행 조건을 먼저 갖췄는지 확인하는 과정이 중요합니다. 이렇게 과목별 선행 조건을 미리 파악해두면, 아이가 어느 시점에 무엇을 준비해야 하는지 훨씬 체계적으로 계획할 수 있게 됩니다. 이런 순서를 지키면서 진행하면, 아이는 '어려운 걸 억지로 하는' 느낌이 아니라 '조금씩 성장하고 있다'는 느낌을 받으면서 선행학습을 이어갈 수 있어요. 이 심리적인 차이가 장기적으로는 학습 동기에 큰 영향을 미칩니다.</p>
    <h2>화상과외가 선행학습에 유리한 이유</h2>
    <p>선행학습은 아이 속도에 맞춰 진도를 유연하게 조절할 수 있는 선생님을 만나는 게 핵심이에요. 학원은 정해진 커리큘럼과 반 편성으로 운영되기 때문에, 아이 개인의 속도에 맞추기가 어려운 경우가 많습니다. 반면 화상과외는 1:1로 진행되기 때문에, 아이가 이해한 정도에 따라 진도를 빠르게 나가기도 하고, 필요하면 다시 돌아가서 짚어주기도 하는 유연한 조정이 가능해요. 지역 제약이 없다는 것도 큰 장점입니다. 능포, 거제중앙 지역 안에서만 찾을 때보다 훨씬 넓은 범위에서, 선행 지도 경험이 많은 선생님을 연결받을 수 있어요. 수업이 녹화되기 때문에 부모님이 나중에 수업 분위기를 확인해보실 수 있다는 것도 안심이 되는 부분이에요. 아이가 정말 이해하면서 진도를 나가고 있는지, 아니면 그냥 따라가기만 하는 건지 부모님도 함께 파악할 수 있습니다. 또한 화상과외는 진도를 늦추거나 앞당기는 조정이 대면 수업보다 훨씬 부담 없이 이뤄질 수 있어요. 정해진 학원 커리큘럼을 따라야 한다는 압박 없이, 순전히 아이 상태에 맞춰 유연하게 움직일 수 있다는 게 선행학습에서는 특히 중요한 부분입니다. 진도가 너무 빠르다 싶으면 바로 속도를 늦추고, 아이가 잘 따라온다 싶으면 조금씩 더 얹어주는 식으로 계속 조율할 수 있다는 게 화상과외만의 큰 장점이에요. 학원처럼 정해진 반 편성이 없다 보니, 다른 아이들과 진도를 비교하며 조급해질 필요도 없다는 것도 심리적으로 큰 안정감을 줍니다. 아이가 온전히 자기 속도로 배울 수 있는 환경 자체가, 선행학습을 부담이 아닌 자연스러운 성장 과정으로 받아들이게 해주는 중요한 요소라고 생각해요. 이런 환경에서 배운 아이일수록 이후에도 새로운 내용을 배우는 것 자체를 즐기는 태도를 갖게 되는 경우가 많습니다. 결국 화상과외가 선행학습에 유리한 이유는 속도의 문제가 아니라, 아이 중심으로 유연하게 조정할 수 있는 구조 자체에 있다고 볼 수 있어요.</p>
    <h2>선행학습 시작 전 꼭 확인해야 할 3가지</h2>
    <p>첫째, 현재 학년 개념에 빠진 부분이 없는지 먼저 확인하세요. 이 확인 없이 선행부터 시작하면 앞서 말씀드린 것처럼 역효과가 날 수 있어요. 둘째, 아이가 선행학습에 대해 심리적으로 부담을 느끼지는 않는지 살펴보세요. 억지로 시작한 선행학습은 오래가지 못하는 경우가 많습니다. 셋째, 선생님이 아이 속도에 맞춰 유연하게 진도를 조절해줄 수 있는 분인지 확인하세요. 정해진 속도로만 진도를 나가는 방식이라면, 오히려 아이에게 안 맞을 수 있어요. 이 세 가지를 먼저 점검한 다음 선행학습을 시작하면, 훨씬 안정적으로 진행할 수 있습니다. 티치핏거제는 상담 시 이 부분들을 하나씩 함께 확인해 드리고, 아이에게 정말 필요한 시점과 방식인지부터 판단해 드려요. 이 세 가지 중 어느 하나라도 확실하지 않다면, 선행학습을 무리하게 서두르기보다는 조금 더 준비 기간을 가지시는 걸 추천드려요. 조급하게 시작해서 중간에 포기하는 것보다, 조금 늦더라도 제대로 된 방식으로 시작하는 게 장기적으로 훨씬 유리합니다. 이 세 가지 기준은 특별히 어려운 게 아니라, 상담 과정에서 몇 가지 질문만으로도 충분히 확인할 수 있는 부분들이니 너무 부담스럽게 생각하지 않으셔도 돼요. 오히려 이런 확인 과정을 거치지 않고 바로 진도부터 시작하는 곳이라면, 시작 전에 한 번 더 신중하게 생각해보시길 권해드립니다. 이 세 가지 기준을 미리 알고 상담에 임하시면, 짧은 시간 안에도 훨씬 알찬 이야기를 나누실 수 있을 거예요. 준비된 상태로 상담을 받으시면 그만큼 아이에게 더 잘 맞는 방향을 빠르게 찾을 수 있습니다. 이 세 가지를 하나의 체크리스트처럼 생각하시고, 상담 전에 미리 한 번씩 스스로 점검해보시는 것도 좋은 방법이에요. 준비를 마치고 상담에 임하시면, 저희와 훨씬 밀도 있는 대화를 나누실 수 있습니다. 이 세 가지만 기억해두셔도, 선행학습을 둘러싼 대부분의 시행착오는 미리 피하실 수 있을 거예요.</p>
    <h2>실제 상담에서 확인한 사례</h2>
    <p>상담을 하다 보면, 처음에는 '옆집 아이도 선행한다는데 우리 아이도 시켜야 하나'라는 조급한 마음으로 문의하시는 학부모님들이 많아요. 그런데 막상 아이의 현재 학년 이해도를 확인해보면, 선행보다 현재 학년 내용을 다지는 게 먼저인 경우가 생각보다 많습니다. 한 학부모님은 아이에게 무리하게 선행을 시켰다가 오히려 아이가 수학에 흥미를 잃는 걸 보고 걱정이 크셨는데, 상담 후 현재 학년 개념부터 다시 다지는 방향으로 바꾸고 나서 아이가 훨씬 편안하게 수업에 참여하게 됐다는 이야기를 해주셨어요. 반대로 현재 학년 개념이 이미 탄탄한 아이의 경우에는, 적절한 시점에 선행을 시작해서 중학교 진학을 훨씬 여유 있게 준비할 수 있었던 사례도 있었습니다. <strong>중요한 건 선행 여부 자체가 아니라, 아이 상태에 맞는 시점과 속도를 찾는 것</strong>이라는 걸 이런 상담들을 통해 계속 확인하고 있어요. 이런 사례들을 보면서 저희도 매번 느끼는 건, 학부모님이 조급함을 조금만 내려놓고 아이 속도를 존중해주실 때 오히려 더 좋은 결과로 이어진다는 점이에요. 선행학습의 목적은 결국 아이가 다음 단계를 덜 힘들어하며 맞이하게 해주는 것이지, 남들보다 앞서 나가는 것 자체가 목적이 되어서는 안 된다는 걸 이런 경험들을 통해 계속 확인하게 됩니다. 그래서 상담을 할 때마다 저희는 '얼마나 빨리 나갈 수 있는지'보다 '얼마나 편안하게 이해하며 나갈 수 있는지'를 더 중요한 기준으로 삼고 있어요. 이런 원칙을 지키다 보니 자연스럽게 아이도, 부모님도 만족하시는 결과로 이어지는 경우가 많았습니다. 조급함보다 여유를 가지고 접근할 때 오히려 더 좋은 결과가 따라온다는 걸 앞으로도 계속 이야기해드리고 싶어요. 이런 사례들이 쌓일수록, 저희가 처음에 세운 원칙이 틀리지 않았다는 확신도 함께 쌓여가고 있습니다. 앞으로도 이런 상담 경험을 바탕으로, 더 많은 능포·거제중앙 지역 학생들에게 맞는 선행학습 방향을 제안해드리고 싶습니다.</p>
    <h2>티치핏거제와 함께 선행학습을 시작해보세요</h2>
    <p>티치핏거제는 상담 시 아이의 현재 학년 이해도와 성향을 먼저 확인하고, 능포초등학교·거제중앙초등학교 같은 학교 분위기를 고려해서 선생님을 연결해 드려요. 선행이 필요한 시점인지부터 함께 판단해 드리기 때문에, 무작정 선행을 권하지 않아요. 모든 선생님은 학력·신원·경력 확인을 거친 뒤에만 매칭에 참여하고, 정식 신청 전에는 30분 무료체험수업으로 먼저 궁합을 확인해보실 수 있습니다. 신청 후 24시간 이내에 담당자가 직접 연락드리고, 학습 진단부터 선생님 추천, 체험 수업까지 순서대로 안내해 드려요. 능포초등학교·거제중앙초등학교뿐 아니라 거제 관내 초·중·고 72곳 전체 학생을 대상으로 매칭이 가능하니, 지금 다니는 학교를 알려주시면 그에 맞춰 상담해 드릴게요. 아이 속도에 맞춘 선행학습으로 중학교 진학을 여유 있게 준비하고 싶으시다면, 지금 편하게 상담을 신청해보세요. 무리한 진도보다 아이에게 맞는 속도를 함께 찾아가는 것, 그것이 저희가 생각하는 진짜 선행학습입니다. 능포와 거제중앙 지역 학부모님들도 이런 방식으로 아이의 다음 단계를 여유 있게 준비해보시길 바랍니다. 지금 아이의 상태가 궁금하시다면, 부담 없이 먼저 상담부터 신청해보세요. 아이에게 맞는 속도를 함께 찾아가는 여정을 저희가 곁에서 든든하게 함께하겠습니다. 오늘 상담 한 번이 아이의 다음 몇 년을 훨씬 편안하게 만들어줄 수 있습니다.</p>
    <p><strong>Q. 능포초등학교, 거제중앙초등학교 모두 매칭 가능한가요?</strong><br>
    네, 두 학교 모두 매칭 가능하고 거제 관내 초등학교 41곳 전부 안내해 드려요.</p>
    <p><strong>Q. 아직 선행이 필요한지 판단이 안 서요, 상담만 받아도 되나요?</strong><br>
    물론이에요. 상담 시 현재 학습 상태를 먼저 확인해 드리고, 선행이 필요한 시점인지도 함께 안내해 드립니다.</p>
    <p><strong>Q. 선행학습 진도는 어느 정도 속도로 나가나요?</strong><br>
    아이가 소화할 수 있는 속도에 맞춰 유연하게 조정하며, 무리하게 빠른 진도를 강요하지 않아요.</p>
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
           lastbuild=rss_pubdate(max(p["date"] for p in BLOG_POSTS)) if BLOG_POSTS else rss_pubdate("2026-01-01"))
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
