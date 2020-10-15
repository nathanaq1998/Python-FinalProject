# Import needed libaries/files
import tweepy
import datetime
import keys

# Login into twitter with user's account
auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_key_secret)

auth.set_access_token(keys.access_token, keys.access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

# Description of program
print('This program will look for bot followers for a provided account.')
# User inputs twitter screen name to look for bots that follow that account
screenName = input('Type the twitter screen name of an account you want to check for bot followers: ')

# Retrieves list of user objects that follow user provided account
followers = tweepy.Cursor(api.followers, id=screenName)

# Function checkBotFriends returns twitter users that a bot is following
# and if that user is verified or not
# It takes a response from the user and the bot's screen name
def checkBotFriends(response, screenName):
    if ((response == 'Y') or (response == 'y')):
        try:
            # Retrieves user object of the bot account
            user = api.get_user('screenName')
            
            # Print who the bot follows
            print('@',screenName,' follows:', sep = '')
            for friend in user.friends():
                # Check if the account is verified
                if friend.verified == True:
                    print('@',friend.screen_name, '(Verified)', sep = '')
                else:
                    print('@',friend.screen_name, '(Not Verified)', sep = '')
                    
                print()
        except tweepy.TweepError as e:
            print(e)
            pass
            # End of checkBotFriends
        return
    else:
        # User did not want to check who the bot follows
        # End of checkBotFriends
        return
    
# Function reportBot reports a bot to twitter and blocks the bot account on the
# user's account
# It takes a response from the user and the bot's screen name
def reportBot(response, screenName):
    if ((response == 'Y') or (response == 'y')):
        try:
            # Reports the bot account to twitter
            api.report_spam(screen_name = 'screenName')
            # Let the user know the account had been reported
            print('@',screenName,' has been reported.', sep = '')
            # End of reportBot
        except tweepy.TweepError as e:
            print(e)
            pass
        return
        
    else:
        # User did not want to report the bot
        # End of reportBot
        return
    
# Variables that hold boolean values to determine
# if an account is a bot account
# Check for no followers
noFollowers = False
# Check for no statuses
noStatuses = False
# Check for profile picture
noProfilePicture = False
# Check if account was created within the month
createdRecent = False

# Pull current month and year
date = datetime.datetime.today().strftime("%m/%y")
# Counter for bot accounts found
botCounter = 0

# Twitter url stored as a string
twitter = 'twitter.com/'

# Go through follower user object list
for follower in followers.items(400):
    
    # If 40 bot accounts are found stop looking
    if botCounter >= 40:
        break
        
    print()
    print()
    # Examine current follower
    print('Examining @',follower.screen_name, sep = '')
    
    # Check if account has any followers
    if follower.followers_count == 0:
        noFollowers = True
    else:
        noFollowers = False
    
    # Check if account has any statuses
    if follower.statuses_count == 0:
        noStatuses = True
    else:
        noStatuses = False
        
    # Check if account has a non-default profile image
    if follower.default_profile_image == True:
        noProfilePicture = True
    else:
        noProfilePicture = False
        
    # Check if follower account was created this month
    if follower.created_at.strftime("%m/%y") == date:
        createdRecent = True
    else:
        createdRecent = False
        
    # If all conditions are met follower is determined to be a bot
    if noFollowers == True & \
       noStatuses == True &  \
       noProfilePicture == True & \
       createdRecent == True:
        # Add 1 to the bot counter
        botCounter += 1
        # Notify user that the follower is a bot account
        print('Found follow-bot #',botCounter,': ',twitter, follower.screen_name, sep = '')
        # Ask the user if they want to see who the bot account follows
        response1 = input('Would you like to see other accounts this bot follows? (Y/N):')
        # Call checkBotFriends function
        checkBotFriends(response1, follower.screen_name)
        print()
        # Ask the user if they want to report the bot account
        response2 = input('Would you like to report this bot? (Y/N): ')
        # Call reportBot function
        reportBot(response2, follower.screen_name)
