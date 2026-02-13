import requests
from bs4 import BeautifulSoup

def crawl():
    # 실제 검색 데이터가 담기는 URL입니다.
    url = "https://www.work24.go.kr/wk/wan/empSrch/retriveWorkNeEmpSrchList.do"
    
    # 🕵️ 더 정교한 사람 흉내 (Headers 보강)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.work24.go.kr/"
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 고용24의 현재 리스트 구조에 맞게 선택자를 보강했습니다.
        jobs = soup.select(".table-wrap tbody tr")
        
        results = []
        for job in jobs:
            title_tag = job.select_one(".subject a")
            if title_tag:
                title = title_tag.text.strip()
                # 🔗 형님이 그토록 원하시던 '진짜 상세 링크' 주소
                link = "https://www.work24.go.kr" + title_tag['href']
                results.append(f"제목: {title} | 링크: {link}")
        
        # 만약 아무것도 못 긁었다면 에러 확인용 메시지를 남깁니다.
        if not results:
            results.append("데이터를 찾지 못했습니다. 사이트 점검 중이거나 구조가 변경되었을 수 있습니다.")

        with open("job_list.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(results))
        print("✅ 수집 성공!")
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")

if __name__ == "__main__":
    crawl()
