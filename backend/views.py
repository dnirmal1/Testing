from django.db.models.fields import UUIDField
from django.http.response import HttpResponse
from django.shortcuts import render, HttpResponse
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
# from .serializers import DoctorDetailSerializer
from .models import DoctorDetails, PatientDetails, VitalDetails, Allergy
import uuid
from .serializers import DoctorDetailsSerializer, PatientDetailsSerializer, VitalDetailsSerializer, AllergySerializer
from rest_framework import status

from backend import serializers


class IndAllergyViewSet(APIView):
    def post(self,request,patientid,id):
        serializer_class = AllergySerializer
        patientid = uuid.UUID(patientid)
        id = int(id)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        allergydetail = Allergy.objects.get(pk=id)
        
        data=request.data
        data['patient']=patientid
        print(data)
        serializer = AllergySerializer(allergydetail,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class AllergyDetailsViewSet(APIView):

    def get(self,request,patientid):
        serializer_class = AllergySerializer
        patientid = uuid.UUID(patientid)
        patient = None
        
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        try:
            allergydetails = Allergy.objects.filter(patient=patient)
            return Response(AllergySerializer(allergydetails, many=True).data, status=status.HTTP_200_OK)
        except:
            content = {'Allergy details not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


    def post(self,request,patientid):
        serializer_class = AllergySerializer
        patientid = uuid.UUID(patientid)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        
        data=request.data
        data['patient']=patientid
        print(data)
        serializer = AllergySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class VitalDetailsViewSet(APIView):
    
    def get(self, request, patientid):
        serializer_class = VitalDetailsSerializer
        patientid = uuid.UUID(patientid)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            vitaldetails = VitalDetails.objects.get(patient=patient)
            return Response(VitalDetailsSerializer(vitaldetails).data, status=status.HTTP_200_OK)
        except:
            content = {'Vital details not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


    def post(self, request, patientid):
        serializer_class = VitalDetailsSerializer
        patientid = uuid.UUID(patientid)
        patient = None
        try:
            patient = PatientDetails.objects.get(id=patientid)
        except:
            content = {'Patient does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        
        try:
            vitaldetails = VitalDetails.objects.get(patient=patient)
            serializer = VitalDetailsSerializer(vitaldetails, data=request.data)
            print(vitaldetails)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            data=request.data
            data['patient']=patientid
            print(data)
            serializer = VitalDetailsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class DoctorViewSet(ModelViewSet):
    queryset = DoctorDetails.objects.all()
    serializer_class = DoctorDetailsSerializer
        
    @action(methods=['get'], detail=True)
    def me(self, request, *args, **kwargs):
        target_user = uuid.UUID(kwargs['doctorid'])
        try:
            doctor = DoctorDetails.objects.get(id=target_user)
            serializer = DoctorDetailsSerializer(doctor)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class PatientViewSet(ModelViewSet):
    queryset = PatientDetails.objects.all()
    serializer_class = PatientDetailsSerializer

    @action(methods=['post'], detail=True)
    def addpatient(self, request, *args, **kwargs):
        target_user = uuid.UUID(kwargs['doctorid'])
        serializer = PatientDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
     
    