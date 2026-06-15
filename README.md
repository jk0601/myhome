# 🌤️ 나의 웹앱 - 오늘의 날씨와 코디 추천

매일 아침 6시에 자동으로 업데이트되는 날씨 기반 코디 추천 웹앱입니다!

## ✨ 특징

- 🌡️ **실시간 날씨 정보** - 네이버 날씨에서 스크래핑 (API 키 불필요!)
- 👔 **스마트 코디 추천** - 기온, 날씨, 바람을 고려한 맞춤 추천
- 🤖 **자동 업데이트** - GitHub Actions로 매일 아침 6시 자동 갱신
- 📱 **반응형 디자인** - 모바일, 태블릿, PC 모두 지원
- 🎨 **날씨별 테마** - 기온에 따라 다른 색상 테마
- 🔑 **API 키 불필요** - 별도 가입이나 설정 없이 바로 사용!

## 🚀 배포 방법 (매우 간단!)

### 1단계: 리포지토리 포크/클론

```bash
git clone https://github.com/YOUR_USERNAME/myhome.git
cd myhome
```

### 2단계: GitHub Pages 활성화

1. GitHub 리포지토리 → Settings → Pages
2. Source: **Deploy from a branch** 선택
3. Branch: **main** 선택, 폴더: **/ (root)** 선택
4. **Save** 클릭

### 3단계: 완료! 🎉

몇 분 후 다음 주소에서 확인 가능:
```
https://YOUR_USERNAME.github.io/myhome/
```

**API 키 설정이 필요 없습니다!** GitHub Pages만 활성화하면 바로 작동합니다! 🎊

## 📅 자동 업데이트

- **매일 아침 6시 (한국 시간)** 자동 업데이트
- GitHub Actions가 자동으로 실행
- 날씨 정보 갱신 및 코디 추천 업데이트

## 🎨 코디 추천 기준

### 기온별 분류
- ❄️ **5°C 미만**: 한겨울 코디 (패딩, 두꺼운 코트)
- 🧥 **5-10°C**: 초겨울/초봄 (코트, 야상, 니트)
- 🧥 **10-15°C**: 환절기 (가디건, 얇은 자켓)
- 👕 **15-20°C**: 봄/가을 (긴팔, 얇은 셔츠)
- ☀️ **20-25°C**: 초여름 (반팔, 얇은 옷)
- 🌞 **25°C 이상**: 한여름 (민소매, 반바지)

### 날씨별 추가 아이템
- 🌧️ **비**: 우산, 방수 재킷
- 🌨️ **눈**: 장갑, 목도리, 방한화
- 💨 **강풍**: 바람막이

## 🛠️ 수동 실행

GitHub Actions를 수동으로 실행하려면:

1. GitHub 리포지토리 → Actions
2. **Update Weather and Outfit** 워크플로우 선택
3. **Run workflow** 클릭

## 📁 파일 구조

```
myhome/
├── .github/
│   └── workflows/
│       └── update-weather.yml   # GitHub Actions 워크플로우
├── weather_outfit.py             # 날씨 & 코디 추천 스크립트
├── requirements.txt              # Python 의존성
├── index.html                    # 생성된 웹페이지 (자동 생성)
└── README.md                     # 이 파일
```

## 🔧 커스터마이징

### 도시 변경

`weather_outfit.py` 파일에서:

```python
CITY = 'Seoul'  # 원하는 도시로 변경
COUNTRY_CODE = 'KR'  # 국가 코드
```

### 업데이트 시간 변경

`.github/workflows/update-weather.yml` 파일에서:

```yaml
cron: '0 21 * * *'  # UTC 시간 (한국 시간 - 9시간)
```

예시:
- 아침 6시 (한국) = `0 21 * * *` (UTC 21시, 전날)
- 아침 7시 (한국) = `0 22 * * *` (UTC 22시, 전날)
- 아침 8시 (한국) = `0 23 * * *` (UTC 23시, 전날)
- 아침 9시 (한국) = `0 0 * * *` (UTC 0시)

## 🌐 데모

아직 배포 전이라면, 로컬에서 테스트:

```bash
# 의존성 설치
pip install -r requirements.txt

# API 키 환경변수 설정 (Windows)
set OPENWEATHER_API_KEY=your_api_key_here

# API 키 환경변수 설정 (Mac/Linux)
export OPENWEATHER_API_KEY=your_api_key_here

# 스크립트 실행
python weather_outfit.py

# index.html 파일이 생성되면 브라우저로 열기
```

## 📝 라이선스

MIT License

## 🤝 기여

이슈와 PR을 환영합니다!

---

Made with ❤️ using GitHub Actions and OpenWeatherMap API
