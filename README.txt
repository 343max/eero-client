# unofficial barebone client lib for eero router (https://eero.com)

This is a very simple client lib to access information about your eero home network. I got this API by intercepting the traffic of the eero app.

Right now it support the following features:
- login/login verification
- user_token refreshing
- account (all information about an account, most importantly a list of your networks)
- networks (information about a particular network)
- devices (a list of devices connected to a network)
- reboot

The API is pretty nice and it should be kind of easy to extend it from here if you miss something. There are a lot of URLs in the response json that will help you explore the API further.

There is a sample client that you might use for your experiments. On first launch it will ask you for the phone number you used to create your eero account. Afterwards you've been asked for the verfication code that you got via SMS. From here on you are logged in - running the command again will dump a ton of information about your network(s).

Right now this code only works for email/phone number login, not for users who login with their Amazon account.
