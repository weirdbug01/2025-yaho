import json
import random

import pickle
import numpy as np
import gradio as gr
from PIL import Image

from api import get_prompt_images
from settings import COMFYUI_PATH


STYLE_LIST = [
    {"name": "Cinematic",
    "prompt": "cinematic still {prompt} . emotional, harmonious, vignette, highly detailed, high budget, bokeh, cinemascope, moody, epic, gorgeous, film grain, grainy"},
     {"name": "Gothic", 
    "prompt": "Gothic still {prompt} . dark, gloomy, eerie, foreboding, haunting, melancholic, mysterious, ominous, bleak, macabre, arched, cathedral-like, vaulted, towering, ornate, gargoyle-covered, pointed arches, spires, buttresses, stone-carved, desolate, tragic, somber, chilling, ethereal, supernatural, vampiric, mystic, decaying, abandoned, high contrast, monochrome, shadowy, dusty, weathered, cracked stone, blood-stained, candlelit, foggy, ashen"},
]


def get_styled_prompt(style_name: str, base_prompt: str) -> str:
    for style in STYLE_LIST:
        if style["name"].lower() == style_name.lower():
            return style["prompt"].replace("{prompt}", base_prompt)
    raise ValueError(f"Style '{style_name}' not found.")


def save_input_image(image):
    input_image = f"{COMFYUI_PATH}/input/sketch.png"
    pillow_image = Image.fromarray(np.array(image["composite"]))
    pillow_image.save(input_image)


def process(
    positive_prompt, 
    image,
    style,
    seed,
    guidance
    ):
    with open("good.json", "r", encoding="utf-8") as f:
        prompt = json.load(f)

    prompt["6"]["inputs"]["text"] = get_styled_prompt(style, positive_prompt)
    prompt["3"]["inputs"]["seed"] = seed
    prompt["12"]["inputs"]["strength"] = guidance

    save_input_image(image)
    images = get_prompt_images(prompt)
    return images


demo = gr.Interface(
    fn=process,
    inputs=[
        # prompt
        gr.Textbox(label="Positive Prompt"),
        # sketch image
        gr.Sketchpad(
            type="pil",
            height=512,
            width=512,
            min_width=512,
            image_mode="RGBA",
            show_label=False,
            mirror_webcam=False,
            show_download_button=True,
            elem_id='input_image',
            brush=gr.Brush(colors=["#000000"], color_mode="fixed", default_size=4),
            canvas_size=(1024, 1024),
            layers=False
        ),
        # style
        gr.Dropdown(
            label="Style",
            choices=[style["name"] for style in STYLE_LIST],
            value="Cinematic",
            scale=1,
        ),
        # seed
        gr.Textbox(label="Seed", value='42', scale=1, min_width=50),
        # guidance
        gr.Slider(
            label="Sketch guidance",
            show_label=True,
            minimum=0,
            maximum=1,
            value=0.4,
            step=0.01,
            scale=3,
        )

    ],
    outputs=[gr.Gallery(label="Result")],
)


if __name__ == "__main__":

    demo.queue()
    demo.launch()
