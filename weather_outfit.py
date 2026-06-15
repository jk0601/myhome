import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

CITY = '서울'

def get_weather():
    """네이버 날씨에서 정보 가져오기 (API 키 불필요!)"""
    try:
        # 네이버 날씨 페이지 (서울)
        url = 'https://weather.naver.com/today/09140101'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # 현재 기온
        temp_element = soup.select_one('.temperature_text strong')
        temp = float(temp_element.text.replace('°', '').replace('현재 온도', '').strip()) if temp_element else 18.0

        # 날씨 상태
        weather_element = soup.select_one('.weather_main .summary')
        description = weather_element.text.strip() if weather_element else '맑음'

        # 최저/최고 기온
        temp_list = soup.select('.temperature_inner .temperature_text')
        temp_min = temp
        temp_max = temp

        if len(temp_list) >= 2:
            try:
                temp_max_text = temp_list[0].text.strip()
                temp_min_text = temp_list[1].text.strip()
                temp_max = float(re.findall(r'-?\d+', temp_max_text)[0])
                temp_min = float(re.findall(r'-?\d+', temp_min_text)[0])
            except:
                pass

        # 습도
        info_items = soup.select('.info_list .item_wrap .item')
        humidity = 60
        wind_speed = 2.0

        for item in info_items:
            label = item.select_one('.label')
            value = item.select_one('.value')
            if label and value:
                if '습도' in label.text:
                    humidity_text = value.text.strip().replace('%', '')
                    try:
                        humidity = int(humidity_text)
                    except:
                        pass
                elif '바람' in label.text or '풍속' in label.text:
                    wind_text = value.text.strip()
                    wind_match = re.findall(r'\d+\.?\d*', wind_text)
                    if wind_match:
                        wind_speed = float(wind_match[0])

        # 날씨 아이콘 결정
        icon = '01d'  # 기본: 맑음
        description_lower = description.lower()
        if '비' in description or 'rain' in description_lower:
            icon = '09d'
        elif '눈' in description or 'snow' in description_lower:
            icon = '13d'
        elif '흐림' in description or 'cloud' in description_lower:
            icon = '03d'
        elif '구름' in description:
            icon = '02d'

        weather_info = {
            'temp': round(temp, 1),
            'feels_like': round(temp, 1),  # 체감온도는 현재 온도와 동일하게
            'temp_min': round(temp_min, 1),
            'temp_max': round(temp_max, 1),
            'humidity': humidity,
            'description': description,
            'icon': icon,
            'wind_speed': round(wind_speed, 1),
            'city': CITY
        }

        print(f"날씨 정보 가져오기 성공: {temp}°C, {description}")
        return weather_info

    except Exception as e:
        print(f"날씨 정보를 가져오는데 실패했습니다: {e}")
        print("기본 데이터를 사용합니다.")
        # 데모 데이터 반환
        return {
            'temp': 18.0,
            'feels_like': 17.0,
            'temp_min': 15.0,
            'temp_max': 20.0,
            'humidity': 65,
            'description': '맑음',
            'icon': '01d',
            'wind_speed': 3.5,
            'city': CITY
        }

def recommend_outfit(weather):
    """날씨에 따른 코디 추천"""
    temp = weather['temp']
    description = weather['description']

    # 기온별 기본 추천
    if temp < 5:
        outfit = {
            'category': '한겨울 코디',
            'emoji': '🧥',
            'top': ['패딩', '두꺼운 코트', '기모 후드'],
            'bottom': ['기모 청바지', '두꺼운 슬랙스'],
            'outer': ['롱패딩', '울 코트'],
            'accessories': ['목도리', '장갑', '귀마개', '털모자'],
            'color': '#1e3a8a',
            'tip': '체온 유지가 중요합니다. 레이어드를 활용하세요!'
        }
    elif temp < 10:
        outfit = {
            'category': '초겨울/초봄 코디',
            'emoji': '🧥',
            'top': ['니트', '맨투맨', '후드'],
            'bottom': ['청바지', '면바지', '슬랙스'],
            'outer': ['코트', '야상', '자켓'],
            'accessories': ['머플러', '비니'],
            'color': '#3b82f6',
            'tip': '아침저녁으로 쌀쌀할 수 있으니 겉옷을 챙기세요!'
        }
    elif temp < 15:
        outfit = {
            'category': '환절기 코디',
            'emoji': '👔',
            'top': ['긴팔 티셔츠', '얇은 니트', '셔츠'],
            'bottom': ['청바지', '면바지', '치노팬츠'],
            'outer': ['가디건', '바람막이', '얇은 자켓'],
            'accessories': ['스카프', '가벼운 모자'],
            'color': '#10b981',
            'tip': '일교차가 클 수 있으니 가벼운 겉옷을 준비하세요!'
        }
    elif temp < 20:
        outfit = {
            'category': '봄/가을 코디',
            'emoji': '👕',
            'top': ['긴팔 티셔츠', '얇은 셔츠', '맨투맨'],
            'bottom': ['청바지', '면바지', '슬랙스'],
            'outer': ['얇은 가디건', '바람막이'],
            'accessories': ['선글라스', '가벼운 모자'],
            'color': '#14b8a6',
            'tip': '쾌적한 날씨입니다. 편안한 옷차림을 즐기세요!'
        }
    elif temp < 25:
        outfit = {
            'category': '초여름 코디',
            'emoji': '👕',
            'top': ['반팔 티셔츠', '얇은 셔츠', '블라우스'],
            'bottom': ['반바지', '면바지', '치마'],
            'outer': ['얇은 가디건 (실내용)'],
            'accessories': ['선글라스', '모자', '선크림'],
            'color': '#f59e0b',
            'tip': '햇볕이 강할 수 있으니 자외선 차단에 신경 쓰세요!'
        }
    else:
        outfit = {
            'category': '한여름 코디',
            'emoji': '👙',
            'top': ['민소매', '반팔 티셔츠', '시원한 블라우스'],
            'bottom': ['반바지', '얇은 면바지', '원피스'],
            'outer': [],
            'accessories': ['선글라스', '모자', '선크림', '부채'],
            'color': '#ef4444',
            'tip': '무더위에 시원한 옷차림과 수분 섭취를 잊지 마세요!'
        }

    # 날씨 상태별 추가 아이템
    if '비' in description or 'rain' in description.lower():
        outfit['accessories'].extend(['우산', '방수 재킷', '방수 신발'])
        outfit['tip'] = '비가 예상되니 우산을 꼭 챙기세요! ' + outfit['tip']

    if '눈' in description or 'snow' in description.lower():
        outfit['accessories'].extend(['장갑', '목도리', '방한화'])
        outfit['tip'] = '눈이 오니 따뜻하게 입고 미끄럼에 주의하세요! ' + outfit['tip']

    if weather['wind_speed'] > 5:
        outfit['tip'] = f"바람이 강합니다 ({weather['wind_speed']}m/s). 바람막이를 추천합니다! " + outfit['tip']

    return outfit

def generate_html(weather, outfit):
    """HTML 파일 생성"""
    now = datetime.now()

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>오늘의 날씨와 코디 추천</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', 'Malgun Gothic', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .container {{
            max-width: 800px;
            width: 100%;
            background: white;
            border-radius: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
            animation: fadeIn 0.5s ease;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .header {{
            background: linear-gradient(135deg, {outfit['color']} 0%, {outfit['color']}dd 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        .date {{
            font-size: 1.1em;
            opacity: 0.9;
            margin-top: 10px;
        }}

        .weather-section {{
            padding: 40px;
            background: linear-gradient(to bottom, #f8f9fa 0%, white 100%);
        }}

        .weather-main {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 30px;
            padding: 30px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .weather-icon {{
            font-size: 5em;
        }}

        .weather-info {{
            flex: 1;
            margin-left: 30px;
        }}

        .temperature {{
            font-size: 4em;
            font-weight: bold;
            color: {outfit['color']};
            margin-bottom: 10px;
        }}

        .description {{
            font-size: 1.5em;
            color: #666;
            margin-bottom: 15px;
        }}

        .weather-details {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            color: #666;
        }}

        .detail-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .outfit-section {{
            padding: 40px;
        }}

        .outfit-title {{
            font-size: 2em;
            color: {outfit['color']};
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .outfit-category {{
            font-size: 2.5em;
        }}

        .outfit-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .outfit-card {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .outfit-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        }}

        .outfit-card h3 {{
            color: {outfit['color']};
            margin-bottom: 15px;
            font-size: 1.2em;
        }}

        .outfit-items {{
            list-style: none;
        }}

        .outfit-items li {{
            padding: 8px 0;
            color: #333;
            border-bottom: 1px solid #dee2e6;
        }}

        .outfit-items li:last-child {{
            border-bottom: none;
        }}

        .outfit-items li:before {{
            content: "✓ ";
            color: {outfit['color']};
            font-weight: bold;
            margin-right: 8px;
        }}

        .tip-box {{
            background: linear-gradient(135deg, {outfit['color']}22 0%, {outfit['color']}11 100%);
            border-left: 4px solid {outfit['color']};
            padding: 25px;
            border-radius: 10px;
            margin-top: 30px;
        }}

        .tip-box h3 {{
            color: {outfit['color']};
            margin-bottom: 10px;
            font-size: 1.3em;
        }}

        .tip-box p {{
            color: #333;
            line-height: 1.6;
            font-size: 1.1em;
        }}

        .footer {{
            text-align: center;
            padding: 30px;
            background: #f8f9fa;
            color: #666;
            border-top: 1px solid #dee2e6;
        }}

        .update-time {{
            font-size: 0.9em;
            opacity: 0.8;
        }}

        @media (max-width: 768px) {{
            .weather-main {{
                flex-direction: column;
                text-align: center;
            }}

            .weather-info {{
                margin-left: 0;
                margin-top: 20px;
            }}

            .outfit-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌤️ 오늘의 날씨와 코디</h1>
            <div class="date">{now.strftime('%Y년 %m월 %d일 %A')}</div>
        </div>

        <div class="weather-section">
            <div class="weather-main">
                <div class="weather-icon">
                    <img src="https://openweathermap.org/img/wn/{weather['icon']}@4x.png" alt="날씨 아이콘" style="width: 150px;">
                </div>
                <div class="weather-info">
                    <div class="temperature">{weather['temp']}°C</div>
                    <div class="description">{weather['description']}</div>
                    <div class="weather-details">
                        <div class="detail-item">
                            <span>🌡️</span>
                            <span>체감: {weather['feels_like']}°C</span>
                        </div>
                        <div class="detail-item">
                            <span>📊</span>
                            <span>습도: {weather['humidity']}%</span>
                        </div>
                        <div class="detail-item">
                            <span>🌡️</span>
                            <span>최저/최고: {weather['temp_min']}°C / {weather['temp_max']}°C</span>
                        </div>
                        <div class="detail-item">
                            <span>💨</span>
                            <span>바람: {weather['wind_speed']} m/s</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="outfit-section">
            <h2 class="outfit-title">
                <span class="outfit-category">{outfit['emoji']}</span>
                <span>{outfit['category']}</span>
            </h2>

            <div class="outfit-grid">
                <div class="outfit-card">
                    <h3>👕 상의</h3>
                    <ul class="outfit-items">
"""

    for item in outfit['top']:
        html_content += f"                        <li>{item}</li>\n"

    html_content += """                    </ul>
                </div>

                <div class="outfit-card">
                    <h3>👖 하의</h3>
                    <ul class="outfit-items">
"""

    for item in outfit['bottom']:
        html_content += f"                        <li>{item}</li>\n"

    html_content += """                    </ul>
                </div>
"""

    if outfit['outer']:
        html_content += """
                <div class="outfit-card">
                    <h3>🧥 겉옷</h3>
                    <ul class="outfit-items">
"""
        for item in outfit['outer']:
            html_content += f"                        <li>{item}</li>\n"
        html_content += """                    </ul>
                </div>
"""

    html_content += """
                <div class="outfit-card">
                    <h3>🎒 액세서리</h3>
                    <ul class="outfit-items">
"""

    for item in outfit['accessories'][:5]:  # 최대 5개만 표시
        html_content += f"                        <li>{item}</li>\n"

    html_content += f"""                    </ul>
                </div>
            </div>

            <div class="tip-box">
                <h3>💡 오늘의 팁</h3>
                <p>{outfit['tip']}</p>
            </div>
        </div>

        <div class="footer">
            <p>매일 아침 6시에 자동으로 업데이트됩니다 ☀️</p>
            <p class="update-time">마지막 업데이트: {now.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p style="margin-top: 10px; font-size: 0.9em;">Made with ❤️ using GitHub Actions</p>
        </div>
    </div>
</body>
</html>
"""

    return html_content

if __name__ == '__main__':
    print("날씨 정보를 가져오는 중...")
    weather = get_weather()

    print(f"위치: {weather['city']}")
    print(f"기온: {weather['temp']}°C")
    print(f"날씨: {weather['description']}")

    print("\n코디를 추천하는 중...")
    outfit = recommend_outfit(weather)

    print(f"추천: {outfit['category']}")

    print("\nHTML 파일을 생성하는 중...")
    html = generate_html(weather, outfit)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("index.html 파일이 생성되었습니다!")
