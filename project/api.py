import json
import urllib.request
import uuid
import time
import random

# ComfyUI 서버 주소
server_address = "http://127.0.0.1:8000"
client_id = str(uuid.uuid4())

def queue_prompt(prompt: str):
    with open("good.json", "r", encoding="utf-8") as f:
        workflow = json.load(f)

    # ✅ 랜덤 시드 생성
    random_seed = random.randint(0, 9223372036854775807)
    workflow["3"]["inputs"]["seed"] = random_seed

    # ✅ 사용자 입력 Positive Prompt 설정
    workflow["6"]["inputs"]["text"] = prompt

    # ✅ 고정된 Negative Prompt 설정
    workflow["7"]["inputs"]["text"] = (
        """nsfw, nude, naked, nipples, sex, sexual, genital, pubic, breast, cleavage, 
            lowres, bad anatomy, bad hands, missing fingers, extra limbs, extra fingers, 
            blurry, watermark, signature, censored, text, logo, ugly, poorly drawn face, 
            bad proportions, deformed, mutated hands, cartoonish, low quality"""
    )

    # 요청 바디 생성 및 전송
    body = {"prompt": workflow, "client_id": client_id}
    data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(
        f"{server_address}/prompt", data=data)
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read())
        return res.get("prompt_id")

def get_history(prompt_id: str):
    url = f"{server_address}/history/{prompt_id}"
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read())

def get_prompt_images(prompt: str, max_wait=50, interval=1):
    prompt_id = queue_prompt(prompt)
    if not prompt_id:
        return None

    print("프롬프트 전송 완료:", prompt_id)

    for _ in range(int(max_wait / interval)):
        history = get_history(prompt_id)

        if prompt_id in history:
            prompt_data = history[prompt_id]
            if "outputs" in prompt_data and prompt_data["outputs"]:
                try:
                    node_output = next(iter(prompt_data["outputs"].values()))
                    image_list = node_output["images"]

                    image_urls = []
                    for image_info in image_list:
                        filename = urllib.parse.quote(image_info["filename"])
                        subfolder = urllib.parse.quote(image_info["subfolder"])
                        folder_type = urllib.parse.quote(image_info["type"])

                        url = f"{server_address}/view?filename={filename}&subfolder={subfolder}&type={folder_type}"
                        image_urls.append(url)

                    return image_urls
                except Exception as e:
                    print("이미지 추출 중 에러:", e)
                    return None

        time.sleep(interval)

    print("시간 초과: 이미지 생성이 완료되지 않음")
    return None
