#!/usr/bin/python
from pony import orm
from entities import PonyDBConn as dbConnector
from langchain_core.tools import tool
from utils_module import log_factory

# init db step
db = dbConnector.getDB()

class Mail(db.Entity):
    MESSAGE_ID = orm.Required(str)
    SUBJECT = orm.Required(str)
    MAIL_FROM = orm.Required(str)
    MAIL_TO = orm.Required(str)
    MAIL_BODY = orm.Optional(str)
    REFERENCE_LIST = orm.Optional(str)
    REPLY_TO = orm.Optional(str)
    TICKET_ID = orm.Optional(str)

# before this need to def entity
db.generate_mapping(create_tables=True)

# insert
@tool
@orm.db_session
def save_mail_message(msd_id, subject, m_from, m_to, body, ref, reply, ticket_id=""):
    """save the mail message in db

    :param msd_id: mail message id field in header
    :param subject: mail subject
    :param m_from: mail sender address in header
    :param m_to: mail receiver address in header
    :param body: mail body
    :param ref: mail references field in header
    :param reply: mail in-reply-to field in header
    :param ticket_id: ticket id of which ticket related with the mail
    :return: save result mail
    """
    logger = log_factory.get_logger()
    logger.info("save mail message in db: message id: %s, subject: %s, from: %s, to: %s, body: %s, ref: %s, reply: %s",
                msd_id, subject, m_from, m_to, body, ref, reply)
    mail = Mail(MESSAGE_ID=msd_id, SUBJECT=subject, MAIL_FROM=m_from,
                MAIL_TO=m_to, MAIL_BODY=body, REFERENCE_LIST=ref, REPLY_TO=reply)
    logger.info("saved done...")
    return mail

@tool
@orm.db_session
def get_mail_by_id(message_id):
    """get processed mail in database by mail message id

    :param message_id: mail message id field in header
    :return: result mail
    """
    logger = log_factory.get_logger()
    logger.info("get mail by mail id: %s", id)
    mail = Mail.select(lambda m: m.MESSAGE_ID == message_id)[:1]
    logger.info("query result: "+str(mail))
    return mail

# fuzzy match query by mail subject
@tool
@orm.db_session
def get_mail_by_subject(subject):
    """get processed mail in database by mail subject

    :param subject: mail subject
    :return: result mails
    """
    logger = log_factory.get_logger()
    logger.info("get mail by mail subject: %s", subject)
    mails = Mail.select(lambda m: subject in m.SUBJECT or m.SUBJECT in subject).get()
    logger.info("query result: "+str(mails))
    return mails

# get mail by raw sql
@tool
@orm.db_session
def get_mails_by_sql(sql):
    """get mails in database by sql

    :param sql: sql
    :return: mail result
    """
    logger = log_factory.get_logger()
    sql = "select * from mail " + sql
    logger.info("get mail by mail sql: %s", sql)

    mails = Mail.select_by_sql(sql)
    logger.info("query result: "+str(mails))

    return mails

@tool
@orm.db_session
def update_mail_related_ticket(message_id, ticket_id):
    """update mail's related ticket id by mail's message id

    :param message_id: mail's message id
    :param ticket_id: the ticket id need to saved in the mail record
    :return: mails
    """
    logger = log_factory.get_logger()
    logger.info("start updating mail's related ticket is, message id: %s, ticket id: %s",
                message_id, ticket_id)
    mails = list(Mail.select(lambda m: m.MESSAGE_ID == message_id))
    for mail in mails:
        mail.set(TICKET_ID=ticket_id)
    logger.info("update done...")
    return mails
