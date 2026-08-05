from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model


#  our custome user this we have specified in settings.py
User = get_user_model()  


#  class name must be command only because djando expects 
# this exact name because it internally run commads using 
#  this Command class name ....
class Command(BaseCommand):

    #  description what does this command ->
    # [python manage.py create_dummy_users]  will do  
    help = "Create dummy users"


    #  entry point of our command this will be run automtly. 
    #  when ever we run our command 

    def handle(self, *args, **kwargs):

        for i in range(1, 11):

            #  check for duplicates ....
            if User.objects.filter(username=f"dummyUser{i}").exists():

                print(f"dummyUser{i} already exists.")
                continue

            # here not objects.create bcoz it wiil not hash pswd 
            #  so use create_user it will store pswd in hash form.

            User.objects.create_user(

                username=f"dummyUser{i}",

                email=f"dummyUser{i}@gmail.com",

                password="password123",

                city="Jaipur",

                state="Rajasthan",

                phone_no=f"98765432{i:02d}"

            )

            print(f"Created dummyUser{i}")

        print("\nSuccessfully created 10 users.")