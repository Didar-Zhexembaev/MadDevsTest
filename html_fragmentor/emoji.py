import unicodedata

def emoji_to_unicode_escape_short(emoji):
    code_point = ord(emoji)
    if code_point > 0xFFFF:
        code_point -= 0x10000
        high_surrogate = 0xD800 + (code_point >> 10)
        low_surrogate = 0xDC00 + (code_point & 0x3FF)
        return [high_surrogate, low_surrogate]
    else:
        return [code_point]

def is_emoji(character):
    # Get the Unicode category of the character
    category = unicodedata.category(character)
    # Check if the category indicates it's an emoji
    return category in ['So', 'Cs']  # 'So' is for symbols, 'Cs' is for other symbols