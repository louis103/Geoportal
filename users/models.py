from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.webp', upload_to='profile_images')
    profile_url = models.CharField(max_length=1000, blank=True, null=True,default='https://gisdata-001.s3.amazonaws.com/media/default.webp')
    bio = models.TextField()
    

    # resizing images
    # def save(self, *args, **kwargs):
    #     super().save()

    #     img = Image.open(self.avatar.url)

    #     if img.height > 100 or img.width > 100:
    #         new_img = (100, 100)
    #         img.thumbnail(new_img)
    #         img.save(self.avatar.path)

    def __str__(self):
        return self.user.username

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='APPROVED')

CATEGORY = (
    ('Gis','Gis'),
    ('Humanitarian','Humanitarian'),
    ('Disasters','Disasters'),
    ('Health','Health'),
    ('Climate','Climate'),
    ('Social','Social'),
    ('Society','Society'),
    ('Remote','Remote'),
    ('Research','Research'),
    ('Economy','Economy'),
    ('Demography','Demography'),
    ('Other','Other'),
    )
STATUS = (
        ('PENDING','PENDING'),
        ('APPROVED','APPROVED'),
    )
TYPES = (
        ('Vector','Vector'),
        ('Raster','Raster'),
        ('Other','Other'),
    )
# SOS- Avicii
IMG_URLS_LIST = (
    ('https://cdn-icons-png.flaticon.com/512/28/28814.png','ZIPFILE'),
    ('https://upload.wikimedia.org/wikipedia/commons/c/c6/.csv_icon.svg','CSV'),
    ('https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Microsoft_Excel_Logo_%282013-2019%29.svg/192px-Microsoft_Excel_Logo_%282013-2019%29.svg.png?20180217032706','EXCEL'),
    ('https://cdn-icons-png.flaticon.com/512/136/136443.png','JSON'),
    ('https://img.favpng.com/0/9/8/south-sumatra-west-sumatra-map-shapefile-png-favpng-qUCpKZdccecDaDJcJVn0NdFZS.jpg','SHAPEFILE'),
    ('https://visibleearth.nasa.gov/img/geotiff.png','GEOTIFF'),
    ('https://static.thenounproject.com/png/3962382-200.png','GEOJSON'),
    ('https://cdn-icons-png.flaticon.com/512/29/29058.png','TIFF'),
    ('https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Simple_Comic_7z.png/640px-Simple_Comic_7z.png','7ZIP'),
    ('https://icons.iconarchive.com/icons/icons8/windows-8/512/Files-Png-icon.png','PNG'),
    ('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLPqd4e8xWKGB_J13hrARNidyJ6u2KzM5CHCX9CRWXYg&s','RAR FILE'),
    ('https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/PDF_icon.svg/1200px-PDF_icon.svg.png','PDF'),
    ('https://cdn-icons-png.flaticon.com/512/29/29620.png','GZ'),
    ('https://static.thenounproject.com/png/3180095-200.png','JPEG'),
    ('https://cdn-icons-png.flaticon.com/512/29/29264.png','JPG'),
    ('https://cdn-icons-png.flaticon.com/512/29/29528.png','KML'),
    )

class GisData(models.Model):
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=1000, blank=True)
    img_icon_url = models.CharField(_('Icon Url'), choices=IMG_URLS_LIST, default="",max_length=1000, blank=True)
    metadata = models.TextField(_('Metadata'),blank=True, null=True)
    attribution = models.CharField(_('Attribution'),max_length=1000,blank=True, null=True, default='No Attribution for this dataset!')
    organization = models.CharField(_('Organization'),max_length=1000,blank=True, null=True, default='Lowa Geoportal!')
    license = models.TextField(_('License'),blank=True, null=True, default='Not Specified.')
    category = models.CharField(_('Category'), max_length=100, choices=CATEGORY, default='GIS',blank=True)
    data_projection = models.CharField(_('Projection System'), max_length=100, default='EPSG:4326', blank=True)
    spatial_extent = models.CharField(_('Spatial Extent'), max_length=100, null=True, blank=True, default='No Spatial Extent Specified!')
    tags = models.TextField(_('Tags'), blank=True, null=True)
    gis_data_type = models.CharField(_('Gis Data Type'), max_length=200, null=True, blank=True, choices=TYPES, default='Other')
    gis_data_key = models.CharField(_('S3 Data Key'),max_length=500, null=True, blank=True)
    status = models.CharField(_('Status'), max_length=100, choices=STATUS, default='PENDING')
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
class SendMessage(models.Model):
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True,null=True)
    email = models.EmailField(max_length=100, blank=True,null=True)
    message = models.TextField(blank=True,null=True)
    
    def __str__(self) -> str:
        return f"{self.name} said {self.message}"
