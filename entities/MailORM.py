#!/usr/bin/python
from pony import orm
from entities import PonyDBConn as dbConnector

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

# before this need to def entity
db.generate_mapping(create_tables=True)

# insert 
@orm.db_session
def save_mail_message(msd_id,subject,m_from,m_to,body,ref,reply) :
    mail = Mail(MESSAGE_ID=msd_id,SUBJECT=subject,MAIL_FROM=m_from,
             MAIL_TO=m_to,MAIL_BODY=body,REFERENCE_LIST=ref,REPLY_TO=reply)
    return mail

# self.subject = subject
#         self.senderName = senderName
#         self.senderAdr = senderAdr
#         self.receivedName = receivedName
#         self.receivedAdr = receivedAdr
#         self.Recipients = Recipients
#         self.receivedTime = receivedTime
#         self.body = body
# query by mail id
@orm.db_session
def get_mail_by_id(id) :
    mail = Mail[id]
    return mail

# fuzzy match query by mail subject
# @orm.db_session
# def get_mail_by_id(subject) :
#     mails = Mail.select(lambda m: subject in m.SUBJECT).get()
#     return mails

# get mail by raw sql
@orm.db_session
def get_mail_by_sql(sql) :
    mails = Mail.select_by_sql(sql)
    return mails
# delete by mail id
# @orm.db_session
# def delMailByID(id) :
# update by mail id
# @orm.db_session
# def updateMailByID(id) :

# debug
# save_mail_message("test","test","test","test","test","test","test")
# print(getMailByID(1).SUBJECT)
# getMailByID(1)
# print(get_mail_by_id("email").SUBJECT)