import llm_config.LLMConnector as llmConn
from langchain_core.prompts import ChatPromptTemplate
from mailbox_module import Mailbox
from db_module import MailORM
from extract_module import MailInfoExtractor
import json
from datetime import datetime
from utils_module import log_factory
import logging
import sys

def process_email():
    # log_date = datetime.today().strftime('%m-%d')
    # # config the logger
    # logger.basicConfig(filename="email_process_" + log_date + ".log",
    #                     filemode='a',
    #                     level=logger.INFO,
    #                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logger = logger.getLogger(__name__)
    logger  = get_logger()
    # todo: till nest wes
    # 1. structure image /upload project to github
    # 2. put extractor/ kick off identifier/ relationship validator/ sql (where) generator in to python class
    # 3. add mail model class and response model class
    # 4. integrate agent-core tool, add ticket process tool
    # 5. remove the if else in process mail
    # 6. optimize the prompt referring agent-core example
    #


    logger.info("-----------------------------------------------------------------------------")
    logger.info("----------MAIL PROCESS START--------------------------------------------------")
    logger.info("------------------------------------------------------------------------------")

    # get first email in "new email" folder
    mail = Mailbox.retrieve_first()
    if not mail:
        logger.info("No new mail in mail box... \n")
        return

    logger.info("Email Extract Rescult: \n" + str(mail))

    # extract the transaction information in the email
    business_info = MailInfoExtractor.extract_business_info(
        "{email subject: " + mail.get("email subject") + ", email body:" + mail.get("email body") + "}")
    logger.info("Business Info Extract Result: \n" + business_info)

    # identify email case
    mail_type = is_kick_off_mail(str(mail))
    is_kick_off = json.loads(mail_type)['kick off mail']
    logger.info("Mail Type Identify Result: \n" + mail_type)

    # if not the first email, then call tool to generate query sql
    if is_kick_off == "false":
        logger.info("Transaction process action : \n update ticket...")
        related_mail_result = get_related_email_sql(str(mail))
        logger.info("SQL generate for getting related email in db : \n" + related_mail_result)
        # search for related email
        mails = MailORM.get_mail_by_sql(str(json.loads(related_mail_result)['sql']))

        # get the query result, and tell if those two email are related email
        if len(mails) != 0:
            mail_entity = mails.pop(0)
            related_mail = json.dumps(mail_entity.to_dict())
            logger.info("Find mail in db: \n" + str(related_mail))
            mail_relation = is_related_mail(str(mail), related_mail)
            logger.info("Relationship Result: \n" + mail_relation)
        else:
            logger.info("Can not find related mail in db...")
        # identify user intention by two mail
    else:
        # create action
        logger.info("Transaction process action : \n create ticket...")

    # save the mail information in the database
    logger.info("save the processed mail message into db...")

    MailORM.save_mail_message(mail.get("message id"), mail.get("email subject"),
                              mail.get("sender Address"), mail.get("received Address"),
                              mail.get("email body"), mail.get("references"), "")

    # move the email to processed mail folder
    Mailbox.move_first()
    logger.info("moving the processed mail message into processed folder...")


def is_kick_off_mail(mail_text):
    # Define a custom prompt to provide instructions and any additional context.
    # 1) You can add examples into the prompt template to improve extraction quality
    # 2) Introduce additional parameters to take context into account (e.g., include metadata
    #    about the document from which the text was extracted.)
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert email processor. "

                "Tell if one email is the kick off email during mail thread according to the mail properties. "
                "If the email is the kick off email, then output 'kick off mail': 'true' "
                "If not the kick off email, then output 'kick off mail': 'false'"
                
                "please transform the output to json without json type tag"
                
                "Below is the mail properties definition: "
                "1. The header field In-Reply-To contains the message ID of the email that the current message is a response to."
                "2. The header field References contains links to previous related emails by including their unique message ID numbers."
                "3. The header field References indicates the mail thread process."
                "4. The header field Message-ID is generated by mail system to identify email"  
                "5.1 A mail thread, also known as an email thread or email chain, is a series of related emails grouped together as part of the same conversation."
                "5.2 Mail thread starts with an original email and includes all subsequent replies and forwards, allowing users to follow the discussion easily."
                "5.3 Essentially, mail thread organizes the communication around a specific topic or subject line, making it easier to track responses."
                
                "Below is some business definition: "
                "1. If two email are related email, then they are in same mail thread."
                "2. First email is the first mail of one mail thread, we can tell it by empty In-Reply-To field."
                "3. In one mail thread, only have one kick off email."
                "4. If one email is the first email send in to 'zhongnora@outlook.com' of all the email in the mail thread, then it's the kick off email. "
                "5. Kick off email may not be the first email."
                ,
            ),
            # Please see the how-to about improving performance with
            # reference examples.
            # MessagesPlaceholder('examples'),
            ("human", "{text}"),
        ]
    )

    # get llm connection
    llm = llmConn.get_llm()
    # structured_llm = llm.with_structured_output(schema=MailMessageBM)

    # if (mailText == None): mailText = "MIME-Version: 1.0\nDate: Thu, 6 Feb 2025 16:50:56 +0800\nMessage-ID: <CAKHC1N6-KcTmtjzJ+k906qNX5nPcR7H8123ERBmSszQ_KAPLBQ@mail.gmail.com>\nSubject: Greeting email from Nora\nFrom: ZHONG waner <zhongwaner91@gmail.com>\nTo: 1403585646@qq.com\nContent-Type: multipart/alternative; boundary=\"0000000000002859e9062d755748\"\n\n\n--0000000000002859e9062d755748\nContent-Type: text/plain; charset=\"UTF-8\"\n\nHi there,\n\nThe weather is very nice today, hope everything is going well for you!\n\nYours,\nNora\n\n--0000000000002859e9062d755748\nContent-Type: text/html; charset=\"UTF-8\"\n\n<div dir=\"ltr\">Hi there,<div><br><div>The weather is very nice today, hope everything is going well for you!</div><div><br></div><div>Yours,</div><div>Nora</div></div></div>\n\n--0000000000002859e9062d755748--"
    prompt = prompt_template.invoke({"text": mail_text})
    # mail = structured_llm.invoke(prompt)
    mail = llm.invoke(prompt)
    result = mail.model_dump()
    return result.get("content")

def is_related_mail(mail_text1, mail_text2):
    # Define a custom prompt to provide instructions and any additional context.
    # 1) You can add examples into the prompt template to improve extraction quality
    # 2) Introduce additional parameters to take context into account (e.g., include metadata
    #    about the document from which the text was extracted.)
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert email processor. "

                "Tell if mail1 and mail2 are related email "
                "If then are related email, then output 'related': true"
                "If then are related email, then output 'related': false"

                "please transform the output to json without json type tag"
                
                "Below is mail properties definition: "
                "1. The header field In-Reply-To contains the message ID of the email that the current message is a response to."
                "2. The header field References contains links to previous related emails by including their unique message ID numbers."
                "3. The header field Message-ID is generated by mail system to identify email"
                "4.1 A mail thread, also known as an email thread or email chain, is a series of related emails grouped together as part of the same conversation."
                "4.2 Mail thread starts with an original email and includes all subsequent replies and forwards, allowing users to follow the discussion easily."
                "4.3 Essentially, mail thread organizes the communication around a specific topic or subject line, making it easier to track responses."
                
                "Below is business definition, if one of the condition satisfied below, then two emails might be related emails "
                "1. If two emails are related email, then they are in same mail thread."
                "2. If two emails are related email, then their References might contain some of the same Message ID parts."
                "3. If two emails are related email, then their Subject might be the same or contains the same key information."
                "4. If two emails are related email, then their email content might be smooth as context."
                ,
            ),
            # Please see the how-to about improving performance with
            # reference examples.
            # MessagesPlaceholder('examples'),
            ("human", "{text}"),
        ]
    )

    # get llm connection
    llm = llmConn.get_llm()
    # structured_llm = llm.with_structured_output(schema=MailMessageBM)
    # if (mailText == None): mailText = "MIME-Version: 1.0\nDate: Thu, 6 Feb 2025 16:50:56 +0800\nMessage-ID: <CAKHC1N6-KcTmtjzJ+k906qNX5nPcR7H8123ERBmSszQ_KAPLBQ@mail.gmail.com>\nSubject: Greeting email from Nora\nFrom: ZHONG waner <zhongwaner91@gmail.com>\nTo: 1403585646@qq.com\nContent-Type: multipart/alternative; boundary=\"0000000000002859e9062d755748\"\n\n\n--0000000000002859e9062d755748\nContent-Type: text/plain; charset=\"UTF-8\"\n\nHi there,\n\nThe weather is very nice today, hope everything is going well for you!\n\nYours,\nNora\n\n--0000000000002859e9062d755748\nContent-Type: text/html; charset=\"UTF-8\"\n\n<div dir=\"ltr\">Hi there,<div><br><div>The weather is very nice today, hope everything is going well for you!</div><div><br></div><div>Yours,</div><div>Nora</div></div></div>\n\n--0000000000002859e9062d755748--"
    prompt = prompt_template.invoke({"text": "{ mail1: "+mail_text1+", mail2: "+mail_text2+" }"})
    # mail = structured_llm.invoke(prompt)
    mail = llm.invoke(prompt)
    result = mail.model_dump()
    return result.get("content")

# import
# from langchain_chroma import Chroma
# from langchain_community.document_loaders import TextLoader
# from langchain_community.embeddings.sentence_transformer import (
#     SentenceTransformerEmbeddings,
# )
# from langchain_text_splitters import CharacterTextSplitter
#
# def vector_store_processor():
#     # load the document and split it into chunks
#     loader = TextLoader("./mail-thread.txt")
#     documents = loader.load()
#
#     # split it into chunks
#     text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     docs = text_splitter.split_documents(documents)
#
#     # create the open-source embedding function
#     embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
#
#     # load it into Chroma
#     db = Chroma.from_documents(docs, embedding_function)
#
#     # query it
#     query = "What did the president say about Ketanji Brown Jackson"
#     docs = db.similarity_search(query)
#
#     # print results
#     return docs[0].page_content

def get_related_email_sql(mail_text):
    # Define a custom prompt to provide instructions and any additional context.
    # 1) You can add examples into the prompt template to improve extraction quality
    # 2) Introduce additional parameters to take context into account (e.g., include metadata
    #    about the document from which the text was extracted.)
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert email system manager. "

                "please transform the output to json without json type tag"

                "Below is the email basic knowledge: "
                "1. The email header field In-Reply-To contains the message ID of the email that the current message is a response to."
                "2. The email header field References contains links to previous related emails by including their unique message ID numbers."
                "3. The email header field Message-ID is generated by mail system to identify email"
                "4.1 A email thread, also known as an email thread or email chain, is a series of related emails grouped together as part of the same conversation."
                "4.2 It starts with an original email and includes all subsequent replies and forwards, allowing users to follow the discussion easily."
                "4.3 Essentially, it organizes the communication around a specific topic or subject line, making it easier to track responses."
                "4.4 If two email are related email, then they are in same mail thread."
                "5. First email is the first mail of one mail thread, we can tell it by empty In-Reply-To field."

                "Below is the business knowledge related with email: "
                "1. Kick off email is the first email send to 'zhongnora@outlook.com' in one mail thread."
                "2. Kick off email may not be the first email."

                "Below is the system structure and function knowledge: "
                "1. All the email send to system mail box 'zhongnora@outlook.com' will be processed by email system."
                "2. The email header info including message-id, references, send address, received address, in-reply-to, message body, subject will be saved in the database. "
                "3. One email corresponds to one transaction action, and the transaction changed by the email will be recorded in the mail record in db."
                "4. Ticket action including: create transaction, update transaction, close transaction, reopen transaction."
                "5. First, need to determine the position number the email in the mail thread. "
                "5.1 If the email is the first email in the mail thread and sent to system mail box, then create transaction."
                "5.2 If not, then will find the same subject and latest related mail saved in db, "
                "5.3 if find then get the related transaction in the related mail's record, get the all the ticket not closed and do update."
                
                "Below are five solution, choose one and output 'solution': solution content."
                "Also output the actual parameter in the solution like 'param1': value."
                "1. Query kick off email with email subject <param1>."
                "2. Fuzzy match kick off email with email subject <param1>."
                "3. Fuzzy Match kick off email with header field References <param1>. "
                "4. Query kick off email with email body content <param1>. "
                "5. Fuzzy match kick off email with body content <param1>. "
                
                "If need to find related mail, then give a raw sql to query one mail's related mail in database according to the chose solution, output 'sql': sql, remove ';' in the end of the sql."
                "Correspondence rules between attributes and database column, please use these column name and mail real property to generate sql:"
                "The table for email is named 'mail'"
                "'message id': MESSAGE_ID, "
                "'email subject': SUBJECT,"
                "'sender Address': MAIL_FROM,"
                "'received Address': MAIL_TO,"
                "'email body': MAIL_BODY,"
                "'references': REFERENCE_LIST."
                ,
            ),
            # Please see the how-to about improving performance with
            # reference examples.
            # MessagesPlaceholder('examples'),
            ("human", "{text}"),
        ]
    )

    # get llm connection
    llm = llmConn.get_llm()
    # structured_llm = llm.with_structured_output(schema=MailMessageBM)

    # if (mailText == None): mailText = "MIME-Version: 1.0\nDate: Thu, 6 Feb 2025 16:50:56 +0800\nMessage-ID: <CAKHC1N6-KcTmtjzJ+k906qNX5nPcR7H8123ERBmSszQ_KAPLBQ@mail.gmail.com>\nSubject: Greeting email from Nora\nFrom: ZHONG waner <zhongwaner91@gmail.com>\nTo: 1403585646@qq.com\nContent-Type: multipart/alternative; boundary=\"0000000000002859e9062d755748\"\n\n\n--0000000000002859e9062d755748\nContent-Type: text/plain; charset=\"UTF-8\"\n\nHi there,\n\nThe weather is very nice today, hope everything is going well for you!\n\nYours,\nNora\n\n--0000000000002859e9062d755748\nContent-Type: text/html; charset=\"UTF-8\"\n\n<div dir=\"ltr\">Hi there,<div><br><div>The weather is very nice today, hope everything is going well for you!</div><div><br></div><div>Yours,</div><div>Nora</div></div></div>\n\n--0000000000002859e9062d755748--"
    prompt = prompt_template.invoke({"text": mail_text})
    # mail = structured_llm.invoke(prompt)
    mail = llm.invoke(prompt)
    result = mail.model_dump()
    return result.get("content")

def get_logger():
    log_date = datetime.today().strftime('%m-%d')
    # logging.basicConfig(filename="email_process_" + log_date + ".log",
    #                     filemode='a',
    #                     level=logging.INFO,
    #                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler("email_process_" + log_date + ".log", mode='a', encoding="GB18030")
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(module)s %(name)s:\t%(message)s'
    ))
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(
        '[%(asctime)s %(levelname)s] %(message)s',
        datefmt="%Y/%m/%d %H:%M:%S"
    ))
    console_handler.setLevel(logging.DEBUG)

    logging.basicConfig(
        level=min(logging.INFO, logging.DEBUG),
        handlers=[file_handler, console_handler],
    )

    return logging.getLogger(__name__)

if __name__ == '__main__':
    process_email()