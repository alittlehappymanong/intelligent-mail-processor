from win32com import client
from mailbox_module import MailMessage
from extract_module import MailInfoExtractor
import pythoncom

def retrieve_first():
    pythoncom.CoInitialize()
    outlook = client.dynamic.Dispatch('outlook.application').GetNamespace("MAPI")
    pythoncom.CoInitialize()
    root_folder = outlook.Folders('zhongnora@outlook.com')

    mail_item = root_folder.Folders.Item('new mail').Items.GetFirst() # get the first mail in the folder
    if not mail_item:
        return None

    header = process_mail_header(mail_item)

    header_info = MailInfoExtractor.extract_basic_info(header)

    mail = MailMessage.MailMessage(mail_item.Subject, mail_item.SenderName, mail_item.SenderEmailAddress, mail_item.ReceivedByName,
                        mail_item.To, mail_item.Recipients,mail_item.ReceivedTime,mail_item.Body, header_info["message_id"],header_info["references"])
    mail_dict = MailMessage.mail_to_dict(mail)

    # remove the space in string
    mail_body = str(mail_dict.get("email body"))
    mail_body =  (mail_body.replace("\\n","").replace("\\r","")
                  .replace("\n","").replace("\r",""))
    mail_dict.__setitem__("email body",mail_body)

    # 清理资源
    del outlook

    return mail_dict

def process_mail_header(mail_item):
    internet_header = mail_item.PropertyAccessor.GetProperty("http://schemas.microsoft.com/mapi/proptag/0x007D001F")
    return internet_header
        
def move_first():
    pythoncom.CoInitialize()
    outlook = client.dynamic.Dispatch('outlook.application').GetNamespace("MAPI")
    pythoncom.CoInitialize()
    root_folder = outlook.Folders('zhongnora@outlook.com')
    mail_list = root_folder.Folders.Item('new mail').Items
    success_folder = root_folder.Folders.Item('processed')
    mail = mail_list.GetFirst()
    mail.move(success_folder)

    # 清理资源
    del outlook

# move_first()
# print(retrieve_first())