import opencc

s2t_converter = opencc.OpenCC('s2t.json')
t2s_converter = opencc.OpenCC('t2s.json')


def get_role_and_content(response):
    role = response['choices'][0]['message']['role']
    content = response['choices'][0]['message']['content'].strip()
    response = s2t_converter.convert(content)
    return role, response
