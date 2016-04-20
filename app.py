from flask import Flask, request, Response
from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage, SuggestedResponseKeyboard, TextResponse, VideoMessage, StartChattingMessage, PictureMessage
import getGiphy

app = Flask(__name__)
kik = KikApi('whatabot', '5c42b012-9000-4954-b03b-f62d89447c27')

kik.set_configuration(Configuration(webhook='https://a570e0b8.ngrok.io/incoming'))


@app.route('/incoming', methods=['POST'])
def incoming():
    if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
        return Response(status=403)

    messages = messages_from_json(request.json['messages'])

    for message in messages:
        if isinstance(message, TextMessage):
            if message.body == 'Hi':
                body = 'What\'s the motive?'
                kik.send_messages([
                        VideoMessage(
                            to=message.from_user,
                            chat_id=message.chat_id,
                            video_url=getGiphy.getGiphy('Hello'),
                            autoplay=True,
                            loop=True,
                        ),
                        TextMessage(
                            to=message.from_user,
                            chat_id=message.chat_id,
                            body=body,
                            keyboards=[
                                SuggestedResponseKeyboard(
                                    responses=[
                                        TextResponse('Staying in'),
                                        TextResponse('Going out'),
                                    ]
                                )
                            ]
                        )
                    ])
                message = TextResponse

        if isinstance(message, TextMessage):
            if message.body == 'Going out':
                body = 'What day though?'
                kik.send_messages([
                        TextMessage(
                            to=message.from_user,
                            chat_id=message.chat_id,
                            body=body,
                            keyboards=[
                                SuggestedResponseKeyboard(
                                    responses=[
                                        TextResponse('Sunday'),
                                        TextResponse('Monday'),
                                        TextResponse('Tuesday'),
                                        TextResponse('Wednesday'),
                                        TextResponse('Thursday'),
                                        TextResponse('Friday'),
                                        TextResponse('Saturday'),
                                    ]
                                )
                            ]
                        )
                    ])
                message = TextResponse

        if isinstance(message, TextMessage):
            if message.body == 'Friday':
                body = ('This is what\'s gucci tonight:\nChainsaw: $3 shots\nEthel\'s: $8 for 1.5lbs wings')
                kik.send_messages([
                        TextMessage(
                            to=message.from_user,
                            chat_id=message.chat_id,
                            body=body,
                            keyboards=[
                                SuggestedResponseKeyboard(
                                    responses=[
                                        TextResponse('Chainsaw'),
                                        TextResponse('Ethel\'s'),
                                    ]
                                )
                            ]
                        )
                    ])
                message = TextResponse

        if isinstance(message, TextMessage):
            if message.body == 'Chainsaw':
                kik.send_messages([
                        PictureMessage(
                            to=message.from_user,
                            chat_id=message.chat_id,
                            pic_url='http://thecord.ca/wp-content/uploads/2014/09/Chainsaw-Heather-Davidson.jpg',
                        ),
                        TextMessage(
                            to=message.from_user,
                            chat_id=message.chat_id,
                            body='Address: 28 King St N,\n Waterloo, ON N2J 2W6\nPhone:(519) 954-8660'
                        )
                ])

        return Response(status=200)


if __name__ == "__main__":
    app.run(port=8080, debug=True)