from .models import Profile
def get_avatar(backend, strategy, details, response,user=None, *args, **kwargs):
    url = None
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large"%response['id']
    if backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal','')
    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
        ext = url.split('.')[-1]
    if url:
        user.avatar = url
        user.save()
        
def save_profile(backend, user, response, is_new=False, *args, **kwargs):
    if is_new and backend.name == "facebook":
        # The main part is how to get the profile picture URL and then do what you need to do
        Profile.objects.filter(owner=user).update(
            imageUrl='https://graph.facebook.com/{0}/picture/?type=large&access_token={1}'.format(response['id'],
                                                                                                  response[
                                                                                                      'access_token']))
    elif backend.name == 'google-oauth2':
        if is_new and response.get('picture'):
            Profile.objects.filter(owner=user).update(imageUrl=response['picture'])