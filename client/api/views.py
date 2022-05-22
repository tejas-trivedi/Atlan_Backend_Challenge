from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import *
import googletrans
from googletrans import Translator
from django.conf import settings
from django.http import HttpResponse
from twilio.rest import Client


# Task 1: Find slang in local language
class GetSlangView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        query_word = request.query_params.get("query_word")

        translator = Translator()
        to_lang = 'hi'

        text_to_translate = translator.translate(query_word, dest= to_lang)
        response = text_to_translate.text
        print(response)

        return Response(response, status=status.HTTP_200_OK)



# Task 2: Validate client data and inserting it if details are correct.
class ValidateData(APIView):
    permission_classes = [AllowAny]
    serializer_class = ValidateSerializer

    def post(self, request, *args, **kwargs):

        client_email = request.data.get('client_email')
        client_name = request.data.get('client_name')
        income_per_annum = request.data.get('income_per_annum')
        savings_per_annum = request.data.get('savings_per_annum')
        mobile_number = request.data.get('mobile_number')

        data = {
            "client_email": client_email,
            "client_name": client_name,
            "income_per_annum": income_per_annum,
            "savings_per_annum": savings_per_annum,
            "mobile_number": mobile_number,
        }

        if(savings_per_annum > income_per_annum):
            return Response(
                    {
                        "message": "Invalid Data: Savings cannot be more than Income"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            serializer = ValidateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": [
                            'Client Details added successfully'
                        ]
                    },
                    status = status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )


# Task 2: Validate all and send the invalid records to the data collector.
class ValidateAll(APIView):
    permission_classes = [AllowAny]
    serializer_class = ValidateSerializer

    def get(self, request, *args, **kwargs):
        clients = Client_Income_Data.objects.all()
        context = {
                "request": request,
            }
        client_serializer = ValidateSerializer(clients, many=True, context=context)
        invalid_data = []

        for i in range(0, len(clients)):
            if(client_serializer.data[i]['savings_per_annum'] > client_serializer.data[i]['income_per_annum']):
                invalid_data.append(client_serializer.data[i])

        if len(invalid_data)==0:
            return Response(
                {
                        "message": [
                            "All records are Valid",
                        ]
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(invalid_data)


# Task 4: Send SMS Middleware
class SendSMS(APIView):
    permission_classes = [AllowAny]
    serializer_class = ValidateSerializer

    def post(self, request, *args, **kwargs):

        client_email = request.data.get('client_email')
        client_name = request.data.get('client_name')
        income_per_annum = request.data.get('income_per_annum')
        savings_per_annum = request.data.get('savings_per_annum')
        mobile_number = request.data.get('mobile_number')

        data = {
            "client_email": client_email,
            "client_name": client_name,
            "income_per_annum": income_per_annum,
            "savings_per_annum": savings_per_annum,
            "mobile_number": mobile_number,
        }

        serializer = ValidateSerializer(data=data)
        if serializer.is_valid():

            message_to_broadcast = 'Your Details: \n' + 'Email ID: ' + client_email + '\n' + 'Name: ' + client_name + '\n' + 'Income Per Annum: ' + income_per_annum + '\n' + 'Savings Per Annum: ' + savings_per_annum + '\n' + 'Contact: ' + mobile_number + '\n' 'Thank you for your response'

            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            client.messages.create(to=mobile_number,
                                from_=settings.TWILIO_NUMBER,
                                body=message_to_broadcast)
            serializer.save()
            return Response(
                {
                    "message": [
                        'Message sent successfully'
                    ]
                },
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

