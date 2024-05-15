import opencc
import re

s2t_converter = opencc.OpenCC('s2t')
t2s_converter = opencc.OpenCC('t2s')

def get_response_data(response) -> dict:
    for item in response['data']:
        if item['role'] == 'assistant' and item['content'] and item['content'][0]['type'] == 'text':
            return item
    return None

def get_content_and_reference(response, file_dict) -> str:
    data = get_response_data(response)
    if not data:
        return ''
    text = data['content'][0]['text']['value']
    annotations = data['content'][0]['text']['annotations']
    text = s2t_converter.convert(text)
    # 替換註釋文本
    ref_mapping = {}
    for i, annotation in enumerate(annotations, 1):
        original_text = annotation['text']
        file_id = annotation['file_citation']['file_id']
        replacement_text = f"[{i}]"
        text = text.replace(original_text, replacement_text)
        ref_mapping[replacement_text] = f"{replacement_text}: {file_dict.get(file_id)}"

    # 添加文件識別碼引用
    reference_text = '\n'.join(ref_mapping.values())
    final_text = f"{text}\n\n{reference_text}"

    return final_text

def replace_file_name(content, file_dict) -> str:
    sorted_file_dict = sorted(file_dict.items(), key=lambda x: -len(x[0]))

    # 對每個鍵進行替換
    for key, value in sorted_file_dict:
        # 使用 re.escape 避免鍵中可能包含的任何正則表達式特殊字符影響匹配
        text = re.sub(re.escape(key), value, text) 
    return text

def check_token_valid(model) -> bool:
    model = OpenAIModel(api_key=openai_api_key, assistant_id=openai_assistant_id)
    is_successful, _, _ = model.check_token_valid()
    if not is_successful:
        raise ValueError('Invalid API token')
    return is_successful

def get_file_dict(model) -> dict:
    is_successful, response, error_message = model.list_files()
    if not is_successful:
        raise Exception(error_message)
    file_dict = { file['id']: file['filename'].replace('.txt', '').replace('.json', '') for file in response['data'] }
    return file_dict

def detect_none_references(text):
    if re.search(r'\[\d+\]: None', text):
        return True
    else:
        return False
