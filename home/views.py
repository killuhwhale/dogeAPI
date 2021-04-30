""" Rest API for doge project.

Endpoints to retrieve tweets and doge prices.
"""
import json
import psycopg2
from django.core import serializers
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Doge, Tweets
from .serializer import DogeSerializer, TweetSerializer

# Allows access from all origins.
headers = {"Access-Control-Allow-Origin": "*"}

@api_view(['GET'])
def prices(request):
    """ Returns all data in the table doge as json.

    Args:
        request: The request information
    Returns:
        data: A list of objects representing a row in the doge table.
    """
    if request.method == 'GET':
        prices = Doge.objects.all()
        data = [DogeSerializer(price).data for price in prices]
        return Response(data, headers=headers)
    else:
        return Response("Error", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def tweets(request):
    """ Returns all data in the table tweets as json.

    Args:
        request: The request information
    Returns:
        data: A list of objects representing a row in the tweets table.
    """
    if request.method == 'GET':
        tweets = Tweets.objects.all()
        data = [TweetSerializer(tweet).data for tweet in tweets]
        return Response(data, headers=headers)
    else:
        return Response("Error", status=status.HTTP_400_BAD_REQUEST)