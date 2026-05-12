import json
import random

random.seed(42) # For reproducibility

regions = [
    ("서울/경기", 37.2, 126.7, 0.4, 0.4, ["소래포구", "인천 남항", "시화", "대부도", "영흥도", "궁평항", "강화도", "제부도", "전곡항", "오이도", "연안부두", "월곶", "화성", "안산", "평택항", "아산만"]),
    ("충남/충북", 36.4, 126.4, 0.5, 0.3, ["태안", "안면도", "신진도", "오천항", "홍원항", "대천", "무창포", "마량항", "장고항", "도비도", "삼길포", "당진", "서산", "보령", "서천", "천수만"]),
    ("전북/전남", 35.5, 126.4, 0.7, 0.4, ["군산 비응항", "격포항", "새만금", "야미도", "선유도", "부안", "고창", "영광", "무안", "신안", "목포", "진도", "해남", "완도", "흑산도", "홍도", "가거도"]),
    ("전남/경남", 34.6, 127.5, 0.3, 1.0, ["여수", "돌산도", "금오도", "거문도", "남해", "미조항", "삼천포", "통영", "욕지도", "사량도", "거제", "해금강", "지세포", "장승포", "구조라", "매물도", "고흥", "녹동"]),
    ("부산/울산/경북", 35.5, 129.3, 0.7, 0.2, ["가덕도", "다대포", "태종대", "송도", "해운대", "청사포", "기장", "대변항", "일광", "울산 방어진", "간절곶", "주전", "정자항", "경주 감포", "포항", "구룡포", "호미곶", "영일만", "칠포", "월포"]),
    ("강원/경북", 37.5, 129.1, 1.0, 0.3, ["영덕 강구항", "축산항", "후포항", "죽변항", "삼척", "임원항", "장호항", "동해 묵호항", "망상", "강릉", "정동진", "안목", "주문진", "양양", "수산항", "남애항", "속초", "대포항", "동명항", "고성", "거진항", "대진항", "아야진"]),
    ("제주도", 33.3, 126.5, 0.2, 0.4, ["제주항", "도두항", "애월", "한림", "비양도", "고산", "차귀도", "모슬포", "마라도", "가파도", "서귀포", "범섬", "섶섬", "문섬", "위미", "남원", "표선", "성산", "우도", "김녕", "함덕", "추자도"]),
]

suffixes = ["방파제", "갯바위", "선착장", "내항", "외항", "앞바다", "해상", "수중여", "뜬방파제", "해수욕장"]
fish_types = [
    ["우럭", "광어", "망둥어", "주꾸미", "갑오징어", "농어", "삼치"], # West
    ["참돔", "감성돔", "돌돔", "볼락", "무늬오징어", "갑오징어", "문어", "갈치", "전어"], # South
    ["가자미", "대구", "도다리", "노래미", "방어", "부시리", "임연수", "무늬오징어", "고등어"], # East
    ["벵에돔", "돌돔", "참돔", "무늬오징어", "한치", "방어", "다금바리", "볼락", "갈치"] # Jeju
]

pts = []
id_counter = 1

for r in regions:
    prov, lat_c, lng_c, lat_r, lng_r, prefixes = r
    
    region_type = 0
    if prov in ["서울/경기", "충남/충북"]: region_type = 0
    elif prov in ["전북/전남", "전남/경남"]: region_type = 1
    elif prov in ["부산/울산/경북", "강원/경북"]: region_type = 2
    elif prov == "제주도": region_type = 3
    
    for _ in range(35): # 35 points * 7 regions = 245 points
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        nm = f"{prefix} {suffix}"
        
        lat = lat_c + random.uniform(-lat_r, lat_r)
        lng = lng_c + random.uniform(-lng_r, lng_r)
        sp = random.sample(fish_types[region_type], 3)
        tp = "방파제" if "방파제" in suffix else ("갯바위" if "갯바위" in suffix else ("선상" if "해상" in suffix or "수중여" in suffix else "항구"))
        mo = [random.randint(0, 50) for _ in range(12)]
        
        pts.append({
            "id": f"p{id_counter}",
            "nm": nm,
            "rg": prov.split("/")[0] + (" " + prefix.split(" ")[0] if " " in prefix else ""),
            "ds": 0,
            "dp": f"{random.randint(5, 15)}–{random.randint(16, 40)}m",
            "sp": sp,
            "rt": round(random.uniform(3.8, 4.9), 1),
            "tp": tp,
            "lat": round(lat, 4),
            "lng": round(lng, 4),
            "mo": mo
        })
        id_counter += 1

js_content = "var PTS=[\n"
for p in pts:
    # Ensure javascript object without quoting keys if possible, but JSON is fine
    # Make it tight to save bytes
    js_content += "  " + json.dumps(p, ensure_ascii=False).replace('"', "'") + ",\n"
js_content += "];"

import re
with open('/Users/hyuni/01-배포용프로그램/01-낚시포인트관리/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace var PTS=[ ... ]; with the new massive array
html = re.sub(r'var PTS=\[.*?\];', js_content, html, flags=re.DOTALL)

with open('/Users/hyuni/01-배포용프로그램/01-낚시포인트관리/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Successfully generated {len(pts)} points and injected into index.html")
