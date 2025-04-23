from langchain_core.prompts import ChatPromptTemplate

from langchain.agents import AgentExecutor, create_tool_calling_agent
import os
from entities import ticket_repo
from process_module import generators
from process_module import validators
from process_module import identifiers
from entities import mail_repo
from langchain.chat_models import init_chat_model
from mailbox_module import mailbox_processor

class EmailProcessor:
    def process_mail_with_tool(self):
        # get llm connection
        # llm = LLMConnector.get_agent()
        # structured_llm = llm.with_structured_output(schema=MailMessageBM)
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert email processor. "
                    "Call the binding tool to process first email once. "
                    
                    "Business background: "
                    "User send email to mail box, one email corresponds to one ticket processing action "
                    "email processor help user to process ticket including create ticket and update ticket. "
                    "Tickets attribute: assignee, transaction type. "

                    "If two emails are related emails, then the two emails are in the same mail thread. "
                    "A email thread, also known as an email thread or email chain, is a series of related emails grouped together as part of the same conversation."
                    "It starts with an original email and includes all subsequent replies and forwards, allowing users to follow the discussion easily."
                    "Essentially, it organizes the communication around a specific topic or subject line, making it easier to track responses."
                    
                    "Mail processor need find email's related emails in database according to email attributes."
                    "If not find related email, then create one ticket for this email, and save email message id in ticket record, that means the ticket is this email's related ticket. "
                    "If find related emails, then find related mails' related tickets, and update ticket."
                    "Email subject or body might contain updating information in mail. " 
                    
                    
                    
                    "Tickets need to be persisted in database"
                    "Processed email need to be saved in database. "
                    "processed folder store the processed email. "
                    # "Get the first email in mailbox, then processed the mail, then move the processed email to processed folder. "
                    
                    "please transform the output to json without json type tag"
                    "please output the actions done like 'actions':[retrieve_first]"
                    ,
                ),
                # Please see the how-to about improving performance with
                # reference examples.
                # MessagesPlaceholder('examples'),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )
        os.environ['OPENAI_API_BASE'] = 'https://api.ohmygpt.com/v1/'
        os.environ['OPENAI_API_KEY'] = 'sk-SIMz5BFx1457F6af0d1DT3BLbkFJE43943ea051c4Ad6925D'
        # os.environ['OPENAI_API_KEY'] = 'sk-KMg0EfQ3CC0A151D99c1T3BLbKFJD46c81384d494f73be84'

        # Construct the tool calling agent
        llm = init_chat_model("gpt-4o-mini", model_provider="openai")

        tools = [mailbox_processor.retrieve_first,
                 mailbox_processor.move_first,
                 ticket_repo.create_ticket,
                 ticket_repo.update_ticket_assignee,
                 ticket_repo.update_ticket_transaction_type,
                 ticket_repo.find_tickets_by_message_id,
                 identifiers.is_kick_off_mail,
                 validators.is_related_mail,
                 generators.get_related_email_sql,
                 mail_repo.get_mail_by_id,
                 mail_repo.get_mails_by_sql,
                 mail_repo.get_mail_by_subject,
                 mail_repo.save_mail_message]

        # Construct the tool calling agent
        # Get the prompt to use - can be replaced with any prompt that includes variables "agent_scratchpad" and "input"!
        # prompt.pretty_print()
        agent = create_tool_calling_agent(llm, tools, prompt_template)
        # mail = structured_llm.invoke(prompt)
        # mail = llm.invoke(prompt)
        # Create an agent executor by passing in the agent and tools
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        return agent_executor.invoke(
            {
                "input": "process one email by tools according to business background"
            }
        )

    def __init__(self):
        pass

if __name__ == '__main__':
    email_processor = EmailProcessor()
    result = email_processor.process_mail_with_tool()
    print(result)