import requests
import json
import sys

def translate_with_ollama(text, model="translator:en-kr-2"):
    """Ollama API를 사용하여 텍스트 번역"""
    url = "http://localhost:11434/api/generate"

    # 마크다운 형식을 유지하도록 프롬프트 작성


    payload = {
        "model": model,
        "prompt": text,
        "stream": False
    }

    try:
        print(F"번역 요청 중 : {payload}")
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        print(f"번역 응답 받음: {result}")
        return result.get('response', '')
    except requests.exceptions.RequestException as e:
        print(f"API 호출 오류: {e}", file=sys.stderr)
        return None

def translate_file(input_path, output_path, model="translator:en-kr-2", max_chunk_chars=2000):
    """파일을 읽어서 번역 후 저장"""
    try:
        # 입력 파일 읽기
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        print(f"번역 중... (모델: {model}, 총 {len(lines)}줄)")

        # 출력 파일을 쓰기 모드로 열기
        with open(output_path, 'w', encoding='utf-8') as out_file:
            i = 0
            chunk_count = 0

            while i < len(lines):
                # max_chunk_chars 이하가 되도록 줄을 모으기
                chunk_lines = []
                chunk_chars = 0

                while i < len(lines):
                    line = lines[i].rstrip('\n')
                    line_length = len(line)

                    # 현재 줄을 추가하면 max_chunk_chars를 초과하는 경우
                    if chunk_chars > 0 and chunk_chars + line_length > max_chunk_chars:
                        break

                    chunk_lines.append(line)
                    chunk_chars += line_length
                    i += 1

                    # 빈 줄이면 청크를 구분하는 좋은 지점
                    if not line.strip() and chunk_chars > max_chunk_chars // 2:
                        break

                if not chunk_lines:
                    break

                chunk_text = '\n'.join(chunk_lines)
                chunk_count += 1

                # 빈 청크는 그대로 저장
                if not chunk_text.strip():
                    out_file.write(chunk_text + '\n')
                    continue

                print(f"[청크 {chunk_count}, {len(chunk_text)}자] 번역 중...")

                # 청크 번역 수행
                translated_text = translate_with_ollama(chunk_text, model)

                if translated_text:
                    # 번역된 텍스트를 즉시 파일에 저장
                    out_file.write(translated_text + '\n')
                    out_file.flush()  # 버퍼 비우기
                    print(f"[청크 {chunk_count}] 저장 완료")
                else:
                    print(f"[청크 {chunk_count}] 번역 실패, 원본 유지")
                    out_file.write(chunk_text + '\n')
                    out_file.flush()

        print(f"번역 완료: {output_path}")

    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {input_path}", file=sys.stderr)
    except Exception as e:
        print(f"오류 발생: {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("사용법: python translator.py <입력파일> <출력파일> [모델명] [최대문자수]")
        print("예시: python translator.py input.md output.md translator:en-kr-2 2000")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    model_name = sys.argv[3] if len(sys.argv) > 3 else "translator:en-kr-2"
    max_chars = int(sys.argv[4]) if len(sys.argv) > 4 else 2000

    translate_file(input_file, output_file, model_name, max_chars)
