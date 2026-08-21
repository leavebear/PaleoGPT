import json

# 假设这是你从模型得到的实体标注数据
input_data = """
Shallowing O O
of O O
the O O
reef O O
crest O O
is O O
also O O
indicated O O
by O O
the O O
presence O O
of O B-FACE
the O I-FACE
shallow-water O I-FACE
benthic O O
Foraminifera O B-LOC
Baculogypsina O I-LOC
sphaerulata O I-FOS
tests O O
after O O
2000 O O
yr O O
BP. O O
"""

# 预定义的标签映射
tag_mapping = {
    "B-FACE": "FACE",
    "I-FACE": "FACE",
    "B-LOC": "LOC",
    "I-LOC": "LOC",
    "B-FOS": "FOSSIL",
    "I-FOS": "FOSSIL",
    "B-STR": "STR",
    "I-STR": "STR",
}

# 实体 ID 映射
entity_tag_map = {
    "shallow-water": "tag_id1",
    "Foraminifera": "tag_id2",
    "Baculogypsina": "tag_id3",
    "sphaerulata": "tag_id4",
}

# 初始化结果
result = {
    "status_code": 0,
    "status_msg": "success",
    "data": {
        "pdf_id": 123,
        "textList": [],
        "ttag": []
    }
}

# 处理每一行文本
lines = input_data.strip().split("\n")
text = []
text_tags = []
current_entity = None

# 遍历所有单词和标记
for i, line in enumerate(lines):
    word, _, tag = line.split()
    
    # 如果当前标签不是 "O"，则是一个实体
    if tag != "O":
        # 如果是新的实体，创建新的标签
        if tag in tag_mapping:
            # 添加标记到文本标记列表
            entity_tag = tag_mapping[tag]
            if word not in entity_tag_map:
                entity_tag_map[word] = f"tag_id{len(entity_tag_map) + 1}"
            text_tags.append({
                "tag_id": entity_tag_map[word],
                "start": len(" ".join(text)),  # 起始位置
                "end": len(" ".join(text)) + len(word),  # 结束位置
                "mark_content": word
            })
    
    # 添加单词到文本
    text.append(word)

# 添加处理后的文本和标签
result["data"]["textList"].append({
    "text": " ".join(text),
    "text_tag": text_tags
})

# 添加 ttag 数据
for tag_name in tag_mapping.values():
    tag_id = f"tag_id{list(tag_mapping.values()).index(tag_name) + 1}"
    result["data"]["ttag"].append({
        "tag_name": tag_name,
        "tag_color": "#FF5733FF",  # 随便给定一个颜色
        "tag_id": tag_id
    })

# 输出结果
print(json.dumps(result, indent=4, ensure_ascii=False))
