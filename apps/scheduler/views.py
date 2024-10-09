from decimal import Decimal
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes,authentication_classes
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
import requests
from requests.auth import HTTPBasicAuth
from rest_framework.permissions import AllowAny

from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY

from .serializers import (
    DagSerializer,CreateDagSerializer,DagPauseSerializer
)

import logging


# Mock endpoint to create DAG
@permission_classes((AllowAny, ))
class CreateDagAPIView(APIView):
    serializer_class = CreateDagSerializer

    @swagger_auto_schema(request_body=CreateDagSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        dagId = data["dagId"]
        description = data["description"]
        schedule_interval = data["schedule_interval"]

        payload = {
            "description": description,
            "schedule_interval": schedule_interval
        }

        url = f"{settings.AIRFLOW_URL}dags/{dagId}"
        
        response = requests.post(
        url,
        auth=HTTPBasicAuth(settings.AIRFLOW_USERNAME, settings.AIRFLOW_PASSWORD),
        json=payload,
        headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            return Response(
                {
                    "successful": True,
                    "message": f"DAG '{dagId}' created successfully.",
                    "errors": None,
                    "data": None,
                    "code": status.HTTP_201_CREATED,
                }
            )
        else:
            return Response(
                {
                    "successful": False,
                    "message": f"Failed to create DAG. Status code: {response.status_code}, Response: {response.text}",
                    "errors": [f"Failed to create DAG. Status code: {response.status_code}, Response: {response.text}"],
                    "data": None,
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            )

#Trigger DAG with config,
@permission_classes((AllowAny, ))
class TriggerDagAPIView(APIView):
    serializer_class = DagSerializer

    @swagger_auto_schema(request_body=DagSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        dagId = data["dagId"]
        
        url = f"{settings.AIRFLOW_URL}dags/{dagId}/dagRuns"
        response = requests.post(
        url,
        auth=HTTPBasicAuth(settings.AIRFLOW_USERNAME, settings.AIRFLOW_PASSWORD),
        json={"conf": {}},  # Optional DAG run config
        headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            return Response(
                {
                    "successful": True,
                    "message": f"DAG '{dagId}' triggered successfully.",
                    "errors": None,
                    "data": None,
                    "code": status.HTTP_200_OK,
                }
            )
        else:
            return Response(
                {
                    "successful": False,
                    "message": f"Failed to trigger DAG. Status code: {response.status_code}, Response: {response.text}",
                    "errors": [f"Failed to trigger DAG. Status code: {response.status_code}, Response: {response.text}"],
                    "data": None,
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            )

#Returns a list of Dag Runs for a specific DAG ID.
@permission_classes((AllowAny, ))
class DagRunsListAPIView(APIView):

    def get(self, request,  *args, **kwargs):
        dagId = kwargs["dagId"]

        url = f"{settings.AIRFLOW_URL}dags/{dagId}/dagRuns"
        response = requests.get(
        url,
        auth=HTTPBasicAuth(settings.AIRFLOW_USERNAME, settings.AIRFLOW_PASSWORD),
        headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            return Response(
                {
                    "successful": True,
                    "message": "Successfully.",
                    "errors": None,
                    "data": response.json(),
                    "code": status.HTTP_200_OK,
                }
            )
        else:
            return Response(
                {
                    "successful": False,
                    "message": f"Failed to a list of Dag Runs for a specific DAG ID. Status code: {response.status_code}, Response: {response.text}",
                    "errors": [f"Failed to a list of Dag Runs for a specific DAG ID. Status code: {response.status_code}, Response: {response.text}"],
                    "data": None,
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            )   

# Pause and UnPause DAG => ‘<string:paused>’ must be a ‘true’ to pause a DAG and ‘false’ to unpause.
@permission_classes((AllowAny, ))
class DagPauseAPIView(APIView):

    @swagger_auto_schema()
    def get(self, request, *args, **kwargs):
        pause = kwargs('pause')
        dagId = kwargs('dagId')
        option = "true" if pause else "false"

        url = f"{settings.AIRFLOW_URL}dags/{dagId}/paused/{option}"
        response = requests.get(
        url,
        auth=HTTPBasicAuth(settings.AIRFLOW_USERNAME, settings.AIRFLOW_PASSWORD),
        headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            return Response(
                {
                    "successful": True,
                    "message": "DAG Paused Successful.",
                    "errors": None,
                    "data": response.json(),
                    "code": status.HTTP_200_OK,
                }
            )
        else:
            return Response(
                {
                    "successful": False,
                    "message": f"Failed to pause Dag. Status code: {response.status_code}, Response: {response.text}",
                    "errors": [f"Failed to pause Dag. Status code: {response.status_code}, Response: {response.text}"],
                    "data": None,
                    "code": status.HTTP_400_BAD_REQUEST,
                }
            )
