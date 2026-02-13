import requests
from bs4 import BeautifulSoup

def crawl():
    url = "https://www.work24.go.kr/wk/wan/empSrch/retriveWorkNeEmpSrchList.do"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        jobs = soup.select(".table-wrap tbody tr")
        results = []
        for job in jobs[:10]:
            title_tag = job.select_one(".subject a")
            if title_tag:
                title = title_tag.text.strip()
                link = "https://www.work24.go.kr" + title_tag['href']
                results.append(f"제목: {title} | 링크: {link}")
        with open("job_list.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(results))
        print("성공!")
    except:
        print("에러!")

if __name__ == "__main__":
    crawl()
