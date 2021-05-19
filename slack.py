import requests



# 슬랙
def post_message(channel, text):
    token = 'xoxb-2074733445556-2068785694675-fYEQuAOf2n1uGHkirhMBDeyA'
    response = requests.post("https://slack.com/api/chat.postMessage",
                headers={"Authorization": "Bearer "+token},
                data={"channel": channel,"text": text}
    )
    print(response)

