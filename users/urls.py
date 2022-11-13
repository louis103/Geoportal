from django.urls import path
from .views import home, RegisterView  # Import the view here
from .views import profile,suggestionApi, s3_form, show_map,get_all_datasets, view_single_dataset, upload_data, contact_us, download_dataset, export_csv_metadata

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('upload/', s3_form, name='file-upload'),
    path('upload_data/', upload_data, name='upload_data'),
    path('list_datasets/', get_all_datasets, name='list_datasets'),
    path('view_single_dataset/<str:pk>', view_single_dataset, name='view_single_dataset'),
    path('contact_us/',contact_us,name='contact_us'),
    path('map/',show_map, name='map'),
    path('suggestionapi/', suggestionApi, name="suggestionapi"),
    path('download_dataset/<str:pk>', download_dataset, name="download_dataset"),
    path('download_metadata/<str:pk>', export_csv_metadata, name="download_metadata"),
]