import hashlib

def generate_chat_hash(post_slug, author_slug, viewer_slug):
    combined_string = f"{post_slug}-{author_slug}-{viewer_slug}"
    return hashlib.sha256(combined_string.encode()).hexdigest()
