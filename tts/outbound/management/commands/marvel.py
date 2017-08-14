import nexmo
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Random Avenger character as a TTS phonecall'

    def add_arguments(self, parser):
        parser.add_argument('to_number', type=str)
        parser.add_argument('from_number', type=str)

    def handle(self, *args, **options):
        
        client = nexmo.Client(
            application_id='de56d45e-0ff7-4aa7-b4f5-022647a2b0ca',
            private_key='django-tts.key'
        )

        to_number = [{'type': 'phone', 'number': options['to_number']}]
        from_number = {'type': 'phone', 'number': options['from_number']}
        answer_url = ['https://nexmo-django-tts.ngrok.io/marvel/']
        
        response = client.create_call({
            'to': to_number,
            'from': from_number,
            'answer_url': answer_url
        })

        self.stdout.write(str(response))
