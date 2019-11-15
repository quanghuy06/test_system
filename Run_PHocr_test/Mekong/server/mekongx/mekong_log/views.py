from django.shortcuts import render
from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MekongLog, MekongLogSerializer


@api_view(['POST'])
def log_all(request):
    """
    Create a new log.
    """

    serializer = MekongLogSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        serializer = MekongLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def log_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    
    try:
        log = MekongLog.objects.get(pk=pk)
    except MekongLog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = MekongLogSerializer(log)
    return Response(serializer.data)


@api_view(["GET"])
def log_view(request, pk):
    logs = MekongLog.objects.filter(client_address=pk).order_by('-at_time')[:100]
    serializer = MekongLogSerializer(logs, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def log_latest(request):
    context = {"clients": []}
    client_addresses = MekongLog.objects.values('client_address').distinct()
    
    for client in client_addresses:
        address = client["client_address"]
        logs = MekongLog.objects.filter(client_address=address).order_by('-at_time')[:100]
        serializer = MekongLogSerializer(logs, many=True)
        context["clients"].append({
            'address': address,
            'data': serializer.data
        })
    
    return Response(context)


@api_view(["GET"])
def log_client(request):
    client_addresses = MekongLog.objects.values('client_address').distinct()
    return Response(client_addresses)