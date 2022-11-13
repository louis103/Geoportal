from django.shortcuts import render,redirect
from rest_framework import generics, status, viewsets
from rest_framework.routers import SimpleRouter
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from datetime import datetime
from django.contrib import messages
from boto3.session import Session
from botocore.exceptions import ConnectionError,ClientError,EndpointConnectionError, ConnectTimeoutError, ReadTimeoutError, ProxyConnectionError, ConnectionClosedError
import logging
import io
from django.http.response import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
import boto3
import zipfile
from django.http import HttpResponseRedirect

import os
import environ

from .serializers import FileSerializer
from users.models import GisData
from users.forms import FileUploadForm
import uuid
from django.core.files.uploadedfile import TemporaryUploadedFile,UploadedFile

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()

session = Session(
    region_name=env('REGION_NAME'),
    aws_access_key_id=env('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=env('AWS_SECRET_ACCESS_KEY')
)

CLIENT = boto3.client(
            "s3", 
            aws_access_key_id=env('AWS_ACCESS_KEY_ID'), 
            aws_secret_access_key=env('AWS_SECRET_ACCESS_KEY'),
)

BUCKET_NAME = env('BUCKET_NAME')

ALLOWED_EXTENSIONS = ["jpg","jpeg","png","shp","dbf",
                      "prj","sbn","sbx","shx","cpg",
                      "geotiff","tif","tiff","geojson",
                      "json","pdf","csv","xlsx","zip"]

# s3 file upload
class FileUploadView(generics.GenericAPIView):

    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.FILES)
        serializer.is_valid(raise_exception=True)

        key_name = os.path.splitext(str(request.FILES['file']))[0]
        file_extension = os.path.splitext(str(request.FILES['file']))[1]
        filename = key_name + file_extension
        # receive the rest of data here
        
        title=request.POST.get('title')
        description=request.POST.get('description')
        category = request.POST.get('category')
        tags = request.POST.get('tags')
        
        gis_data_type = request.POST.get('gis_data_type')
        gis_data_key = filename

        # creating a session from boto3 amazon.
        s3 = session.resource('s3')
        try:
            s3.Bucket(env('BUCKET_NAME')).put_object(Key=filename, Body=request.FILES['file'])  
        except ClientError as e:
            return Response({"message": "Failed to Upload!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        finally:
            ready_data = GisData(
            title=title,
            description=description,
            category=category,
            tags=tags,
            gis_data_type=gis_data_type,
            gis_data_key=gis_data_key,
            )
            ready_data.save()
            return Response({"message": "File Upload and Data Addition Success!"}, status=status.HTTP_200_OK)

#create bucket in s3 buckets
@api_view(['GET'])
def create_s3_bucket(request):
     session = session
     s3_resource = session.resource("s3")
     current_region = session.region_name
     bucket_name = BUCKET_NAME
     bucket_response = s3_resource.create_bucket(
         Bucket=bucket_name,
         CreateBucketConfiguration={
             'LocationConstraint':current_region,
         }
     )
     return Response({'message':'Bucket created successfully!'},status=status.HTTP_201_CREATED)
    
# download data from s3 bucket
@api_view(['GET'])
def download_from_s3(request, filename):
    s3_resource = session.resource("s3")
    if request.method == 'GET':
        try:
            s3_resource.Bucket(BUCKET_NAME).download_file(filename,f'/Downloads/{filename}')
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                return Response({'message':f'File not Found within S3 Bucket: {BUCKET_NAME}!'}, status=status.HTTP_404_NOT_FOUND) 
            else:
                raise
    else:
        return Response({"message": "Method not allowed!"}, status=status.HTTP_403_FORBIDDEN)

#delete data in s3 buckets
@api_view(['DELETE'])
def delete_s3_file(request, filename):
    try:
        response = CLIENT.delete_object(
            Bucket=BUCKET_NAME,
            Key=filename,
        )
        return Response({"message": "File Deleted!"}, status=status.HTTP_200_OK) 
    except ClientError as e:
        return Response({"message":"An Error Occurred!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# delete files from folder in s3 buckets
@api_view(['DELETE']) 
def delete_all_objects_from_s3_folder(request):
    """
    This function deletes all files in a folder from S3 bucket
    :return: None
    """
    bucket_name = BUCKET_NAME

    # First we list all files in folder
    response = CLIENT.list_objects_v2(Bucket=bucket_name, Prefix="main_gis_data/")

    files_in_folder = response["Contents"]
    files_to_delete = []
    # We will create Key array to pass to delete_objects function
    for f in files_in_folder:
        files_to_delete.append({"Key": f["Key"]})

    # This will delete all files in a folder
    response = CLIENT.delete_objects(
        Bucket=bucket_name, Delete={"Objects": files_to_delete}
    )
    return response

S3_FOLDER = "/zipped/"
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

files_list = []
@api_view(['POST'])
def upload_shapefile_zip(request):
    s3 = session.resource('s3')
    ALLOWED_EXTENSIONS = ["7z","gz","rar","jpg","jpeg","png","shp","geotiff","tif","tiff","geojson","json","pdf","csv","xlsx","zip"]
    RASTER_FILES = ["jpg","jpeg","png","geotiff","tif","tiff"]
    VECTOR_FILES = ["csv","xlsx","zip", "json","geojson","shp","tar","gz"]
    file = request.FILES.get("file_field_single")
    filename = os.path.splitext(str(file))[0]
    extension = os.path.splitext(str(file))[1][1:]
    full_name = filename+"."+extension
    print(file,filename, extension, full_name)
    data_form = FileUploadForm(request.POST)
    if extension in ALLOWED_EXTENSIONS:
            
        # if extension in RASTER_FILES:
        #     gis_data_type = 'Raster'
        # elif extension in VECTOR_FILES:
        #     gis_data_type = 'Vector'
        # elif extension == 'pdf':
        #     gis_data_type = 'Pdf Document'
        # else:
        #     gis_data_type = 'Not Specified'
        try:
            if data_form.is_valid(): 
                # response = s3.Bucket(env('BUCKET_NAME')).put_object(Key='Datasets/{}'.format(full_name), Body=request.FILES['file_field_single']) 
                response = True
                if response:  
                    print("received response") 
                    com_form = data_form.save(commit=False)
                    com_form.user = request.user
                    com_form.gis_data_type = 'Vector'
                    com_form.gis_data_key = full_name
                    print("saving form data")
                    com_form.save()       
                    messages.success(request, f'Dataset and metadata uploaded successfully!')
                    return redirect(to='list_datasets')
        # else:
        #     return Response({"message": "Please fill out the form!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({"message": "Upload Failed!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                messages.error(request, f'Fill the form kindly!')
                return redirect(to='file-upload')   

        except ClientError as e:
            messages.error(request, f'Failed to Upload Dataset!') 
            return HttpResponse(f'Failed to upload Dataset due to {e}')
        except ConnectTimeoutError as e:
            messages.error(request, f'Failed to Upload Dataset!') 
            return HttpResponse(f'Failed to upload Dataset, Check your internet connection. {e}')
        except ConnectionClosedError as e:
            messages.error(request, f'Failed to Upload Dataset!') 
            return HttpResponse(f'Failed to upload Dataset, Check your internet connection. {e}')
        except ReadTimeoutError as e:
            messages.error(request, f'Failed to Upload Dataset!') 
            return HttpResponse(f'Failed to upload Dataset, Read Timeout Error. {e}')
        except ConnectionError as e:
            messages.error(request, f'Failed to Upload Dataset!') 
            return HttpResponse(f'Failed to upload Dataset, Connection Error. {e}')
            # return Response({"message": "Please fill out the form!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    else:
        return HttpResponse(f"Files with that extension are not allowed! extension {extension}")
    # else:
    #     return Response({"message": "Form Invalid,please fill out the form!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # return HttpResponse(f'Success') 
    # else:
    #     return HttpResponse("Please upload a dataset file!")

    
@api_view(['POST'])
def upload_data(request):
    data_form = FileUploadForm(request.POST, instance=request.user)
    if data_form.is_valid():
        try:
        #   exclude = ('gis_data_type','gis_data_key',)
        #   fields = ['title','metadata','tags','category','data_projection']
            # f = data_form.save(commit=False)
            # f.user = request.user
            # f.title = "TITLE TEST"
            # f.metadata = "METADATA"
            # f.tags = "TAGS"
            # f.category = "CATEGORY"
            # f.data_projection = "EPSG:3245  "
            # f.gis_data_type = "VECTOR"
            # f.gis_data_key = "HTML.csv"
            # print("This is the current user: ",f.user)
            # com_form = data_form.save(commit=False)
            # com_form.user = request.user
            print("Saving")
            data_form.save()
            # print(data_form)
            messages.success(request, f'Dataset and metadata uploaded successfully!')
            return redirect(to='list_datasets')
        except Exception as e:
            messages.error(request, f'Dataset Failed to Upload! due to {e}')
            return redirect(to='file-upload')
    else:
        messages.error(request, f'Form Invalid!')
        return redirect(to='file-upload') 

