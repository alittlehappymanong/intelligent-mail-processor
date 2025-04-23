#!/usr/bin/python
from pony import orm
from entities import PonyDBConn as dbConnector
from langchain_core.tools import tool
import uuid
from utils_module import log_factory

# init db step
db = dbConnector.getDB()

# inner class Ticket entity
class Tickets(db.Entity):
    TICKET_ID = orm.Optional(str)
    SUBJECT = orm.Required(str)
    ASSIGNEE = orm.Optional(str)
    TRANSACTION_TYPE = orm.Optional(str)
    MESSAGE_ID = orm.Required(str)

# before this need to def entity
db.generate_mapping(create_tables=True)

# update ticket assignee by message id and subject
@tool
@orm.db_session
def update_ticket_assignee(message_id, subject, assignee):
    """update ticket's attribute assignee by ticket's mail message id and ticket's subject

    :param message_id: the message id of mail which related with the ticket and saved in the ticket record
    :param subject: the subject of mail which related with the ticket and saved in the ticket record
    :param assignee: new assignee value need to update in the ticket record
    :return: none
    """
    logger = log_factory.get_logger()
    logger.info("start updating ticket's assignee, message id: %s, subject: %s, assignee: %s", message_id, subject, assignee)
    tickets = list(Tickets.select(lambda t: t.MESSAGE_ID == message_id and t.SUBJECT == subject))
    for tk in tickets:
        tk.set(ASSIGNEE=assignee)
    logger.info("update done...")
    return True

@tool
@orm.db_session
def find_tickets_by_message_id(message_id):
    """find mail message's related tickets, get tickets by message id

    :param message_id: related mail message id
    :return: tickets list
    """
    tickets = list(Tickets.select(lambda t: t.MESSAGE_ID == message_id))
    return tickets

# update ticket transaction type by message id and subject
@tool
@orm.db_session
def update_ticket_transaction_type(message_id, subject, transaction_type):
    """update ticket's attribute transaction type by ticket's mail message id and ticket's subject

    :param message_id: the message id of mail which related with the ticket and saved in the ticket record
    :param subject: the subject of mail which related with the ticket and saved in the ticket record
    :param transaction_type: new transaction type need to update in the ticket record
    :return: none
    """
    logger = log_factory.get_logger()
    logger.info("start updating ticket's transaction type, message id: %s, subject: %s, transaction type: %s", message_id, subject, transaction_type)
    tickets = list(Tickets.select(lambda t: t.MESSAGE_ID == message_id and t.SUBJECT == subject))
    for tk in tickets:
        tk.set(TRANSACTION_TYPE=transaction_type)
    logger.info("update done...")
    return True

@tool
@orm.db_session
def create_ticket(subject, message_id, assignee='', transaction_type=''):
    """create and save ticket in db

    :param subject: email subject of which creating ticket
    :param message_id: email subject of which creating ticket
    :param assignee: ticket assignee, optional
    :param transaction_type: transaction type for ticket, optional
    :return:
    """
    logger = log_factory.get_logger()
    logger.info("start creating, subject: %s, message id: %s, assignee: %s, transaction type: %s",
                subject, message_id, assignee, transaction_type)
    ticket_id = str(uuid.uuid1())
    ticket = Tickets(TICKET_ID=ticket_id, SUBJECT=subject, ASSIGNEE=assignee,
                TRANSACTION_TYPE=transaction_type, MESSAGE_ID=message_id)
    logger.info("ticket created, ticket id: %s", ticket_id)
    return ticket







