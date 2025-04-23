from process_module import email_processor
import json
from entities import  MailORM

mails = MailORM.get_mail_by_sql("SELECT * FROM mail WHERE SUBJECT = 'Normal flow 4.18-3'")
mail = "{'email subject': 'Re:Normal flow 4.18-3', 'sender Name': '钟婉儿', 'sender Address': '1403585646@qq.com', 'received Name': 'waner zhong', 'received Address': 'zhongnora', 'Recipients': <COMObject <unknown>>, 'received Time': pywintypes.datetime(2025, 4, 18, 12, 4, 11, 130000, tzinfo=TimeZoneInfo('GMT Standard Time', True)), 'email body': 'Normal flow reply2 Original________________________________From:钟婉儿 <1403585646@qq.com>Sent Time:2025-04-18- 11:56To:zhongnora <zhongnora@outlook.com>Subject:Normal flow 4.18-3Normal flow email-1', 'message id': '<tencent_8E0F06177AFDB44E57F36F4338F1A36D6409@qq.com>', 'references': '<tencent_5995D111B2368339BDD75AD9AB3CB7F59C08@qq.com>'}"
# get the query result, and tell if those two email are related email
if len(mails) != 0:
    print(mails)
    mail_entity = mails.pop(0)
    related_mail = json.dumps(mail_entity.to_dict())
    print("Find mail in db: \n" + str(related_mail))
    mail_relation = email_processor.is_related_mail(mail, str(related_mail))
    print("Relationship Result: \n" + mail_relation)
else:
    print("Can not find related mail in db...")
