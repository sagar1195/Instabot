from Key import ACCESS_TOKEN
import requests
import urllib

BASE_URL = "https://api.instagram.com/v1/"

def get_user_id(insta_username):
    request_url= (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, ACCESS_TOKEN)
    print 'Get request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received'
        exit()

#id_var = get_user_id('195ffg')

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (ACCESS_TOKEN)
    print 'Requesting data from : %s' %(request_url)

    recent_post=requests.get(request_url).json()

    if recent_post['meta']['code'] == 200:
        if len(recent_post['data']) > 0:
            image_name = recent_post['data'][0]['id'] + ".jpeg"
            image_url = recent_post['data'][0]['images']['standard_resolution']['url']

            urllib.urlretrieve(image_url, image_name)
        else:
            print 'No posts to show'
    else:
        print "Error"

    return None

#get_own_post()

def get_user_post(username):
    user_id = get_user_id(username)

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id ,ACCESS_TOKEN)
    print ("Request URL: %s") % (request_url)

    recent_post = requests.get(request_url).json()

    if recent_post['meta']['code'] == 200:
        if len(recent_post['data']) > 0:
            image_name = recent_post['data'][0]['id'] + ".jpeg"
            image_url = recent_post['data'][0]['images']['standard_resolution']['url']

            urllib.urlretrieve(image_url, image_name)
        else:
            print 'No posts to show'
    else:
        print "Error"

get_user_post('195ffg')