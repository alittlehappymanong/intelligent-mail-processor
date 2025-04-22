from llm_config import LLMConnector
from langchain_core.prompts import ChatPromptTemplate
from extract_module.MailBaseModel import MailMessageBM

def extract_basic_info(mail_text) :
    # Define a custom prompt to provide instructions and any additional context.
    # 1) You can add examples into the prompt template to improve extraction quality
    # 2) Introduce additional parameters to take context into account (e.g., include metadata
    #    about the document from which the text was extracted.)
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert extraction algorithm. "
                "Only extract relevant information from the text. "
                "If you do not know the value of an attribute asked to extract, "
                "return null for the attribute's value.",
            ),
            # Please see the how-to about improving performance with
            # reference examples.
            # MessagesPlaceholder('examples'),
            ("human", "{text}"),
        ]
    )

    # get llm connection
    llm = LLMConnector.get_llm()
    structured_llm = llm.with_structured_output(schema=MailMessageBM)

    # if (mailText == None): mailText = "MIME-Version: 1.0\nDate: Thu, 6 Feb 2025 16:50:56 +0800\nMessage-ID: <CAKHC1N6-KcTmtjzJ+k906qNX5nPcR7H8123ERBmSszQ_KAPLBQ@mail.gmail.com>\nSubject: Greeting email from Nora\nFrom: ZHONG waner <zhongwaner91@gmail.com>\nTo: 1403585646@qq.com\nContent-Type: multipart/alternative; boundary=\"0000000000002859e9062d755748\"\n\n\n--0000000000002859e9062d755748\nContent-Type: text/plain; charset=\"UTF-8\"\n\nHi there,\n\nThe weather is very nice today, hope everything is going well for you!\n\nYours,\nNora\n\n--0000000000002859e9062d755748\nContent-Type: text/html; charset=\"UTF-8\"\n\n<div dir=\"ltr\">Hi there,<div><br><div>The weather is very nice today, hope everything is going well for you!</div><div><br></div><div>Yours,</div><div>Nora</div></div></div>\n\n--0000000000002859e9062d755748--"
    prompt = prompt_template.invoke({"text": mail_text})
    mail = structured_llm.invoke(prompt)
    return mail.dict()

def extract_business_info(mail_text):
    # Define a custom prompt to provide instructions and any additional context.
    # 1) You can add examples into the prompt template to improve extraction quality
    # 2) Introduce additional parameters to take context into account (e.g., include metadata
    #    about the document from which the text was extracted.)
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert ticket manager, please return all the result as json format without json style tag. "

                "One ticket has status including open, closed, reopened, and if email header or body mentioned, you will also output 'status: ' plus ticket current status"
                "if email header or body not mentioned ticket status, you can output 'status: null'"
                
                "One ticket may be related with some transaction teams, and if email header or body mentioned, you will also output 'teams: ' plus team name"
                "if email header or body not mentioned transaction teams, you can output 'teams: null'"

                "One ticket may be related with one assignee, and if email header or body mentioned, you will also output 'assignee: ' plus assignee name"
                "if email header or body not mentioned assignee name, you can output 'assignee: null'"
                
                "One ticket may be related with one trans type, and if email header or body mentioned, you will also output 'trans type: ' plus trans type"
                "if email header or body not mentioned trans type, you can output 'trans type: null'"

                "One ticket may be related with one ticket id, and if email header or body mentioned, you will also output  'ticket id: ' plus ticket id"
                "if email header or body not mentioned or the action is create ticket, you can output 'ticket id: null'"

                "return 'unknown message' if you cannot process the email.",
            ),
            # Please see the how-to about improving performance with
            # reference examples.
            # MessagesPlaceholder('examples'),
            ("human", "{text}"),
        ]
    )

    # get llm connection
    llm = LLMConnector.get_llm()
    # structured_llm = llm.with_structured_output(schema=MailMessageBM)

    # if (mailText == None): mailText = "MIME-Version: 1.0\nDate: Thu, 6 Feb 2025 16:50:56 +0800\nMessage-ID: <CAKHC1N6-KcTmtjzJ+k906qNX5nPcR7H8123ERBmSszQ_KAPLBQ@mail.gmail.com>\nSubject: Greeting email from Nora\nFrom: ZHONG waner <zhongwaner91@gmail.com>\nTo: 1403585646@qq.com\nContent-Type: multipart/alternative; boundary=\"0000000000002859e9062d755748\"\n\n\n--0000000000002859e9062d755748\nContent-Type: text/plain; charset=\"UTF-8\"\n\nHi there,\n\nThe weather is very nice today, hope everything is going well for you!\n\nYours,\nNora\n\n--0000000000002859e9062d755748\nContent-Type: text/html; charset=\"UTF-8\"\n\n<div dir=\"ltr\">Hi there,<div><br><div>The weather is very nice today, hope everything is going well for you!</div><div><br></div><div>Yours,</div><div>Nora</div></div></div>\n\n--0000000000002859e9062d755748--"
    prompt = prompt_template.invoke({"text": mail_text})
    # mail = structured_llm.invoke(prompt)
    mail = llm.invoke(prompt)
    result = mail.model_dump()
    return result.get("content")