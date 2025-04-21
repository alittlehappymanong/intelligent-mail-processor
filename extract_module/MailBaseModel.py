######## schema
from typing import Optional

from pydantic import BaseModel, Field

class MailMessageBM(BaseModel) :
    """Information about an email message."""
    subject: Optional[str] = Field(default=None, description="The subject of the mail message")
    message_id: Optional[str] = Field(default=None, description="The message id of the mail message")
    sender_name: Optional[str] = Field(default=None, description="The sender name of the mail message")
    from_address: Optional[str] = Field(default=None, description="The sender address of the mail message")
    recipient: Optional[str] = Field(default=None, description="The recipient of the mail message")
    received_timestamp: Optional[str] = Field(default=None, description="The received date of the mail message")
    references: Optional[str] = Field(default=None, description="The references of the mail message")
    mail_body: Optional[str] = Field(default=None, description="The mail message body of the maill message")
    reply: Optional[str] = Field(default=None, description="The reply message id of the maill message")