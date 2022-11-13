from django.urls import path

from .views import FileUploadView, upload_shapefile_zip,upload_data

urlpatterns = [
    path('file-s3/', FileUploadView.as_view(), name='upload-to-s3'),
    path('file-s3-upload/', upload_shapefile_zip, name='upload-zip'),
    path('app_upload/', upload_data, name='upload_app_data')
]
