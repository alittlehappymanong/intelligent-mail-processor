from win32com import client
from mailbox_module import MailMessage
from extract_module import MailInfoExtractor
import pythoncom
from langchain_core.tools import tool
from utils_module import log_factory

@tool
def retrieve_first():
    """get the first email in mailbox

    :return: mail dict
    """
    logger = log_factory.get_logger()
    logger.info("connect to the mail box.....")
    pythoncom.CoInitialize()
    outlook = client.dynamic.Dispatch('outlook.application').GetNamespace("MAPI")
    pythoncom.CoInitialize()
    root_folder = outlook.Folders('zhongnora@outlook.com')

    mail_item = root_folder.Folders.Item('new mail').Items.GetFirst()  # get the first mail in the folder
    if not mail_item:
        logger.info("mail box is empty...")
        return None
    logger.info("get one mail.."+str(mail_item))
    header = process_mail_header(mail_item)

    header_info = MailInfoExtractor.extract_basic_info(header)

    mail = MailMessage.MailMessage(mail_item.Subject, mail_item.SenderName, mail_item.SenderEmailAddress,
                                   mail_item.ReceivedByName,
                                   mail_item.To, mail_item.Recipients, mail_item.ReceivedTime, mail_item.Body,
                                   header_info["message_id"], header_info["references"])
    mail_dict = MailMessage.mail_to_dict(mail)

    # remove the space in string
    mail_body = str(mail_dict.get("email body"))
    mail_body = (mail_body.replace("\\n", "").replace("\\r", "")
                 .replace("\n", "").replace("\r", ""))
    mail_dict.__setitem__("email body", mail_body)

    # 清理资源
    del outlook

    return mail_dict

def process_mail_header(mail_item):
    logger = log_factory.get_logger()
    logger.info("mail header processing...")
    internet_header = mail_item.PropertyAccessor.GetProperty("http://schemas.microsoft.com/mapi/proptag/0x007D001F")
    logger.info("mail header processing done...")
    return internet_header

@tool
def move_first():
    """move the first email to processed folder

    :return: none
    """
    logger = log_factory.get_logger()
    logger.info("try to move first mail to processed folder...")
    pythoncom.CoInitialize()
    outlook = client.dynamic.Dispatch('outlook.application').GetNamespace("MAPI")
    pythoncom.CoInitialize()
    root_folder = outlook.Folders('zhongnora@outlook.com')
    mail_list = root_folder.Folders.Item('new mail').Items
    success_folder = root_folder.Folders.Item('processed')
    mail = mail_list.GetFirst()
    if not mail:
        logger.info("mail box empty...")
    else:
        logger.info("move the mail to processed folder...")
        mail.move(success_folder)
    # 清理资源
    del outlook