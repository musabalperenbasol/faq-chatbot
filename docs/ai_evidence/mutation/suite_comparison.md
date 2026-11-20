# Suite comparison (mutation testing)

| Suite | Killed | Survived | Score |
|---|---|---|---|
| ours | 71 | 19 | 78.9% |
| ai | 68 | 22 | 75.6% |
| combined | 73 | 17 | 81.1% |
| all | 81 | 9 | 90.0% |

## Killed by the AI suite but survived our suite (2)

- app.chatbot.xǁFAQChatbotǁ__init____mutmut_8
- app.chatbot.xǁFAQChatbotǁask__mutmut_4

## Killed by our suite but survived the AI suite (5)

- app.chatbot.x__is_token__mutmut_2
- app.prompts.x_build_system_prompt__mutmut_1
- app.prompts.x_build_system_prompt__mutmut_2
- app.prompts.x_build_system_prompt__mutmut_5
- app.prompts.x_build_system_prompt__mutmut_6

## Survived BOTH suites (17)

- app.chatbot.x__is_token__mutmut_3
- app.chatbot.x_load_faq__mutmut_2
- app.chatbot.x_load_faq__mutmut_4
- app.chatbot.x_load_faq__mutmut_6
- app.chatbot.xǁFAQChatbotǁ__init____mutmut_12
- app.chatbot.xǁFAQChatbotǁ__init____mutmut_5
- app.chatbot.xǁFAQChatbotǁvalidate_question__mutmut_10
- app.chatbot.xǁFAQChatbotǁvalidate_question__mutmut_11
- app.chatbot.xǁFAQChatbotǁvalidate_question__mutmut_13
- app.chatbot.xǁFAQChatbotǁvalidate_question__mutmut_2
- app.chatbot.xǁFAQChatbotǁvalidate_question__mutmut_3
- app.chatbot.xǁFAQChatbotǁvalidate_question__mutmut_4
- app.chatbot.xǁFAQChatbotǁvalidate_question__mutmut_5
- app.chatbot.xǁFAQChatbotǁvalidate_question__mutmut_8
- app.chatbot.xǁFAQChatbotǁvalidate_question__mutmut_9
- app.prompts.x_format_faq__mutmut_11
- app.prompts.x_format_faq__mutmut_9

## Survived even the final suite (all) (9)

- app.chatbot.x_load_faq__mutmut_2
- app.chatbot.x_load_faq__mutmut_4
- app.chatbot.x_load_faq__mutmut_6
- app.chatbot.xǁFAQChatbotǁvalidate_question__mutmut_10
- app.chatbot.xǁFAQChatbotǁvalidate_question__mutmut_11
- app.chatbot.xǁFAQChatbotǁvalidate_question__mutmut_3
- app.chatbot.xǁFAQChatbotǁvalidate_question__mutmut_4
- app.chatbot.xǁFAQChatbotǁvalidate_question__mutmut_5
- app.chatbot.xǁFAQChatbotǁvalidate_question__mutmut_9
