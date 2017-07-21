from Key import ACCESS_TOKEN
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import requests
import urllib

BASE_URL = "https://api.instagram.com/v1/"                                                                              #Taking the common url part and saving it in BASE_URL

#-----------------------------------------------------------------------------------------------------------------------
#Fetching our own information

def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
            print '\n'
        else:
            print 'User does not exist!'
            print '\n'
    else:
        print 'Status code other than 200 received!'
        print '\n'

#-----------------------------------------------------------------------------------------------------------------------
#Getting the id of the user

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
        print '\n'
        exit()

#-----------------------------------------------------------------------------------------------------------------------
#Fetching the information of the user

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
            print '\n'
        else:
            print 'There is no data for this user!'
            print '\n'
    else:
        print 'Status code other than 200 received!'
        print '\n'

#-----------------------------------------------------------------------------------------------------------------------
#Fetching owners recent post

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
            print '\n'
    else:
        print "Error"
        print '\n'

    return None

#-----------------------------------------------------------------------------------------------------------------------
#Fetching the users recent post

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
            print '\n'
    else:
        print "Error"
    print '\n'

#-----------------------------------------------------------------------------------------------------------------------
#Getting the id of the recent post of the user

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print ("Request URL: %s") % (request_url)

    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']) > 0:
            return user_media['data'][0]['id']
        else:
            print 'No posts to show'
            print '\n'
    else:
        print "Status code other than 200 received"
        print '\n'
    return None

#-----------------------------------------------------------------------------------------------------------------------
#Getting the list of people that liked a post

def get_like_list():

    request_url = (BASE_URL + 'users/self/media/%s/liked?access_token=%s')% ([ACCESS_TOKEN])

    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):

            image_name = user_info['data'][0]['id'] + '.jpeg'

            image_url = user_info['data'][0]['images']['standard_resolution']['url']

            # Downloading the image liked
            urllib.urlretrieve(image_url, image_name)

            return user_info['data'][0]['id']
        else:
            print 'There is no recent post!'
    else:
        print 'Error :-  %s' % str(user_info['meta']['code'])

    return None

#-----------------------------------------------------------------------------------------------------------------------
#liking the post of some user

def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {
        "access_token": ACCESS_TOKEN
        }
    print 'Liking the post %s' % (request_url)
    post_a_like = requests.post(request_url,payload).json()

    if post_a_like['meta']['code'] == 200:
        print "like was successful"
    else:
        print 'Your like was unsuccessful. Try again!'

#-----------------------------------------------------------------------------------------------------------------------
#Leaving a comment on a post

def make_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input(" Your comment:  ")

    payload = {
        "access_token": ACCESS_TOKEN,
        'text':comment_text
        }
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'Making comment on post %s' % (request_url)
    make_comment = requests.post(request_url,payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment"
    else:
        print 'Unable to add comment. Try again!'

#-----------------------------------------------------------------------------------------------------------------------
#deleting the negative comments from your post with help of Textblob library

def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'Get request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                    media_id, comment_id, ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print "There are no existing comments on the post"
    else:
        print 'Status code other than 200 received!'

#-----------------------------------------------------------------------------------------------------------------------
#Fuction to create a menue for the user to access our bot easily

def start_bot():
    while True:

        print 'The menu options are :-\n' \
              '1. Get your own details.\n' \
              '2. Get details of a user using username.\n' \
              '3. Get your recent posts.\n' \
              '4. Get recent posts of a user using username.\n' \
              '5. Get the recent media liked by the user.\n' \
              '6. Like the recent post of a user.\n' \
              '7. Post a comment on the recent post of a user.\n' \
              '8. Delete negative comments from recent post of a user.\n' \
              '9. Exit.\n'

        choice = int(raw_input('Enter your choice :- '))

        if choice == 1:
            self_info()

        elif choice == 2:
            insta_username = raw_input('Please enter the instagram username :- ')
            get_user_info(insta_username)

        elif choice == 3:
            post_id = get_own_post()
            print 'Recent post with id: %s has been downloaded.' % post_id

        elif choice == 4:
            insta_username = raw_input('Please enter the instagram username :- ')
            post_id = get_user_id(insta_username)
            print 'Recent post by %s with id: %s has been downloaded.' % (insta_username, post_id)

        elif choice == 5:
            post_id = get_like_list()
            print 'Recent liked post with id: %s has been downloaded.' % post_id

        elif choice == 6:
            insta_username = raw_input('Please enter the instagram username :- ')
            like_a_post(insta_username)

        elif choice == 7:
            insta_username = raw_input('Please enter the instagram username :- ')
            make_a_comment(insta_username)

        elif choice == 8:
            insta_username = raw_input('Please enter the instagram username :- ')
            delete_negative_comment(insta_username)

        elif choice == 9:
            exit()

        else:
            print 'Wrong choice'

start_bot()