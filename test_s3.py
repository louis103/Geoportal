import boto3  # pip install boto3

# Let's use Amazon S3
# s3 = boto3.resource("s3")
s3 = boto3.client("s3")
s3_resource = boto3.resource('s3')
my_bucket = s3_resource.Bucket('gisdata-001')
my_files = []
for object in my_bucket.objects.filter(Prefix='Datasets/'):
    my_files.append(object.key)
    print(my_files)

# Print out bucket names
# for bucket in s3.buckets.all():
#     print(bucket.name)
    
# s3.download_file(
#     Bucket="gisdata-001", Key="healthcare_facilities.csv", Filename="healthcare_facilities.csv"
# )

# s3.upload_file(
#     Filename="kenya_all_towns.csv",
#     Bucket="gisdata-001",
#     Key="kenya_towns.csv",
# )


# client = boto3.client('s3')
# s3.delete_object(Bucket='gisdata-001', Key='kenya_towns.csv')


# from boto.s3.connection import S3Connection, Bucket, Key

# conn = S3Connection(AWS_ACCESS_KEY, AWS_SECERET_KEY)

# b = Bucket(conn, S3_BUCKET_NAME)

# k = Key(b)

# k.key = 'images/my-images/'+filename

# b.delete_key(k)


import io
# import zipfile

# zip_buffer = io.BytesIO()

# with zipfile.ZipFile(zip_buffer, "a",
#                      zipfile.ZIP_DEFLATED, False) as zip_file:
#     for file_name, data in [('1.txt', io.BytesIO(b'111')),
#                             ('2.txt', io.BytesIO(b'222'))]:
#         zip_file.writestr(file_name, data.getvalue())

# with open('C:/1.zip', 'wb') as f:
#     f.write(zip_buffer.getvalue())

