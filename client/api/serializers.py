from rest_framework import serializers
from client.models import *

class FindSlangSerializer(serializers.Serializer):
    query_word = serializers.CharField(max_length=50)
    query_lang = serializers.CharField(max_length=10)



class ValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client_Income_Data
        fields = '__all__'

        def create(self, validated_data):
            client_data = Client_Income_Data(
                client_email=validated_data["client_email"],
                client_name=validated_data["client_name"],
                income_per_annum=validated_data["income_per_annum"],
                savings_per_annum=validated_data["savings_per_annum"],
                mobile_number=validated_data["mobile_number"],
            )
            client_data.save()
            return client_data