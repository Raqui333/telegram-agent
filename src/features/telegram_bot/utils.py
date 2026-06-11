from telegram import Message
from telegramify_markdown import ContentType, telegramify


async def handle_llm_response(message: Message, llm_response: str):
    parts = await telegramify(llm_response)
    for part in parts:
        if part.content_type == ContentType.TEXT:
            await message.reply_text(
                text=part.text,
                entities=[e.to_dict() for e in part.entities],
                disable_web_page_preview=True,
            )
        elif part.content_type == ContentType.PHOTO:
            await message.reply_photo(
                photo=part.file_data,
                filename=part.file_name,
                caption=part.caption_text or None,
                caption_entities=[e.to_dict() for e in part.caption_entities] or None,
            )
        elif part.content_type == ContentType.FILE:
            await message.reply_document(
                document=part.file_data,
                filename=part.file_name,
                caption=part.caption_text or None,
                caption_entities=[e.to_dict() for e in part.caption_entities] or None,
            )
