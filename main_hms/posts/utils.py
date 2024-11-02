import hashlib
import logging

logger = logging.getLogger(__name__)


def generate_chat_hash(post_slug, author_slug, viewer_slug):
    logger.info("Генерация хэша чата")
    combined_string = f"{post_slug}-{author_slug}-{viewer_slug}"
    return (
        hashlib.sha256(combined_string.encode()).hexdigest()
        + "devisor"
        + str(post_slug)
    )
