from collections import Counter
import re

def extract_keywords(text):
    text = text.lower()

    words = re.findall(r'\b\w+\b', text)
    words = [w for w in words if len(w) > 3]
    keywords = [w for w, _ in Counter(words).most_common(5)]

    return keywords

def parse_user(request_user, user):
    return {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'password': user.password,
        'birthday': user.birthday,
        'bio': user.bio,
        'picture': user.picture,
        'is_followed': request_user.is_following(user)
    }
