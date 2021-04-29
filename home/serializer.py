from rest_framework import serializers

class DogeSerializer(serializers.Serializer):
    ts = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=11)


class TweetSerializer(serializers.Serializer):
    ts = serializers.IntegerField(read_only=True)
    tweet = serializers.CharField(read_only=True)
