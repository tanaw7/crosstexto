import random

WORD_LIST = [
    "house", "bedroom", "living", "room", "family", "kitchen", "apartment", "chair", "home", "stove",
    "sleep", "residence", "table", "door", "ring", "bathroom", "garage", "dog", "furniture", "window",
    "queen", "king", "prince", "princess", "royal", "crown", "lady", "london", "parade", "victoria",
    "god", "religion", "lord", "jesus", "heaven", "angel",
    # Thai words
    "บ้าน", "ห้องนอน", "ครอบครัว", "ห้องครัว", "อพาร์ตเมนต์", "ประตู", "ห้องน้ำ", "สุนัข", "หน้าต่าง", "เก้าอี้",
    "พระราชินี", "กษัตริย์", "เจ้าชาย", "เจ้าหญิง", "มงกุฎ", "ขบวนพาเหรด", "พระเจ้า", "ศาสนา", "สวรรค์", "เทวทูต"
]

def get_random_target_word():
    return random.choice(WORD_LIST)

def get_word_list():
    return WORD_LIST