# GeolocationAPI

Hi :)

I would like to show you my version of GeolocationAPI app.


You may see and use it via:
https://tomaszbeben.herokuapp.com/


If you want to run the application locally you will need a few things ;)


First, docker and docker compose.

I will not describe here how to install it, there are great docs for


docker -> https://docs.docker.com/install/

and

docker-compose -> https://docs.docker.com/compose/install/


OK, hardest thing behind us ;)


Now clone the repo by:

SSH -> git clone git@github.com:TheVerin/GeolocationAPI.git

HTTPS -> https://github.com/TheVerin/GeolocationAPI.git


Great :D

Now you can choose to run app in dev or prod environment.


At first you have to run terminal from project root and then execute command:

for DEV:

    make setup-dev
		
for PROD:

    make setup-prod



Really easy, right?



Last point is testing.

It is as simple as running the app. You need to run terminal from project root and:

for DEV:

    make run-tests-dev
		
for PROD:

    make run-tests-prod
		

That's all :)

I hope you enjoy the app ;)

P.S Remember, its always better to join premium...
