# from extract_module import MailInfoExtractor as mailExtractor
# from db_module import MailORM as mailRepo
#
# mailText = "MIME-Version: 1.0\nDate: Thu, 6 Feb 2025 16:50:56 +0800\nMessage-ID: <CAKHC1N6-KcTmtjzJ+k906qNX5nPcR7H8123ERBmSszQ_KAPLBQ@mail.gmail.com>\nSubject: Greeting email from Nora\nFrom: ZHONG waner <zhongwaner91@gmail.com>\nTo: 1403585646@qq.com\nContent-Type: multipart/alternative; boundary=\"0000000000002859e9062d755748\"\n\n\n--0000000000002859e9062d755748\nContent-Type: text/plain; charset=\"UTF-8\"\n\nHi there,\n\nThe weather is very nice today, hope everything is going well for you!\n\nYours,\nNora\n\n--0000000000002859e9062d755748\nContent-Type: text/html; charset=\"UTF-8\"\n\n<div dir=\"ltr\">Hi there,<div><br><div>The weather is very nice today, hope everything is going well for you!</div><div><br></div><div>Yours,</div><div>Nora</div></div></div>\n\n--0000000000002859e9062d755748--"
# mail = mailExtractor.extract_basic_info(mailText)
# print(mail)
#
# res = mailRepo.save_mail_message(mail['messageId'], mail['subject'],
#                          mail['fromAddress'], mail['recipient'],
#                          mail['mailbody'],mail['references'], mail['reply'])
# print(res)