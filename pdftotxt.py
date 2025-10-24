# 필요한 라이브러리 설치
# pip install pdfplumber markdownify

import pdfplumber
from markdownify import markdownify as md

def pdf_to_markdown(pdf_path, md_path):
    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            # 페이지 텍스트 추출
            text = page.extract_text()

            if text:
                # 불필요한 줄바꿈 제거
                lines = text.split('\n')
                processed_lines = []
                temp_paragraph = ""

                for line in lines:
                    line = line.strip()
                    if line:  # 빈 줄이 아니면
                        # 하이픈으로 끝나는 경우 처리 (단어 분할)
                        if temp_paragraph and temp_paragraph.endswith('-'):
                            temp_paragraph = temp_paragraph[:-1] + line
                        else:
                            temp_paragraph += (" " if temp_paragraph else "") + line
                    else:  # 빈 줄이면 문단 구분
                        if temp_paragraph:
                            processed_lines.append(temp_paragraph)
                            temp_paragraph = ""

                # 마지막 문단 추가
                if temp_paragraph:
                    processed_lines.append(temp_paragraph)

                # 문단 구분을 유지하며 결합
                full_text += '\n\n'.join(processed_lines) + "\n\n"

    # Markdown 파일 저장
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(full_text.strip())

    print(f"Markdown 파일로 변환 완료: {md_path}")

# 사용 예시
pdf_to_markdown("Drive.pdf", "Drive.md")
# 사용 예시
pdf_to_markdown("Drive.pdf", "Drive.md")
