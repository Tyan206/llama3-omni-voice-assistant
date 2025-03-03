from groq import Groq
from PIL import ImageGrab
import google.generativeai as genai
import pyperclip
import cv2



web_cam = cv2.VideoCapture(1)

generative_config = {
    'temperature': 0.7,
    'top_p': 1,
    'top_k': 1,
    'max_output_tokens': 2048
}

safety_settings = [
    {
        'category': 'HARM_CATEGORY_HARASSMENT',
        'threshold': 'BLOCK_NONE'
    },
    {
        'category': 'HARM_CATEGORY_HATE_SPEECH',
        'threshold': 'BLOCK_NONE'
    },
    {
        'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
        'threshold': 'BLOCK_NONE'
    },
    {
        'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
        'threshold': 'BLOCK_NONE'
    }
]

model = genai.GenerativeModel('gemini-1.5-flash-latest',
                              generation_config=generative_config,
                              safety_settings=safety_settings)

def groq_prompt(prompt):
    convo = [{'role': 'user', 'content': prompt}]

    chat_completion = groq_client.chat.completions.create(messages=convo, model = 'llama3-70b-8192')

    response = chat_completion.choices[0].message

    return response.content


def function_call(prompt):
    sys_msg = (
        'You are an AI function calling model. You will determine whether extracting the users clipboard content, '
        'taking a screenshot, capturing the webcam or calling no functions is best for a voice assistant to respond '
        'to the users prompt. The webcam can be assumed to be a normal laptop webcam facing the user. You will '
        'respond with only one selection from this list: ["extracting clipboard", "take screenshot", "capture webcam", "None"] \n'
        'Do not respond with anything but the most logical selection from that list with no explanations. Format the '
        'function call name exactly as I listed.'
    )

    function_convo = [{'role': 'system', 'content': sys_msg},
                      {'role': 'user', 'content': prompt}]
    
    chat_completion = groq_client.chat.completions.create(messages=function_convo, model = 'llama3-70b-8192')

    response = chat_completion.choices[0].message

    return response.content


def take_screenshot():
    path = 'screenshot.jpg'
    screenshot = ImageGrab.grab()
    rgb_screenshot = screenshot.convert('RGB')
    rgb_screenshot.save(path, quality=15)


def web_cam_capture():
    if not web_cam.isOpened():
        print('Error: Camera did not open successfully')
        exit()

    path = 'webcam.jpg'
    ret, frame = web_cam.read()
    cv2.imwrite(path, frame)


def get_clipboard_text():
    clipboard_content = pyperclip.paste()
    if isinstance(clipboard_content, str):
        return clipboard_content
    else:
        print('No clipboard text to copy')
        return None


def vision_prompt(prompt, photo_path):
    pass

prompt = input('USER: ')
function_response = function_call(prompt)
print(f'Function call: {function_response}')
response = groq_prompt(prompt)
print(response)
