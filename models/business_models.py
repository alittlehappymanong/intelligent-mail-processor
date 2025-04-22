class Ticket:
    ticket_id = ""
    subject = ""
    assignee = ""
    transaction_type = ""
    message_id = ""

    def __init__(self, ticket_id, subject, assignee, transaction_type, message_id):
        self.ticket_id = ticket_id
        self.subject = subject
        self.assignee = assignee
        self. transaction_type = transaction_type
        self.message_id = message_id


class MailMessage:
    def __init__(self, subject, sender_name, sender_adr, received_name, received_adr, recipients, received_time, body,
                 message_id, references):
        # def __init__(self,  subject, senderName, senderAdr, receivedAdr, body):

        # self.messageId = messageId
        self.subject = subject
        self.sender_name = sender_name
        self.sender_adr = sender_adr
        self.received_name = received_name
        self.received_adr = received_adr
        self.recipients = recipients
        self.received_time = received_time
        self.body = body
        self.message_id = message_id
        self.references = references


    def mail_to_dict(mail):
        return {
            "email subject": mail.subject,
            "sender Name": mail.sender_name,
            "sender Address": mail.sender_adr,
            "received Name": mail.received_name,
            "received Address": mail.received_adr,
            "Recipients": mail.recipients,
            "received Time": mail.received_time,
            "email body": mail.body,
            "message id": mail.message_id,
            "references": mail.references
        }


