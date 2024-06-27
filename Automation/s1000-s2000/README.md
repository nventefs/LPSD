The files in this folder run all the test cases for System 1000 and 2000. To use it, simply run the run_user_interface.py file then use the UI.

There are a few things that are required for this to work. You need to first have access to the LPSD system, but I am assuming that if you are using this you have that. If not, ask someone, I dont know how you get that. Next, you need to have a .env file somewhere in here, I have mine in the parent directory of this one (/Automation). In that file, you need to have your autodesk username (for me that is my nVent email), your nVent password, and a 2 factor authentication key in the format

AUTODESK_USERNAME = "your@username.here"
NVENT_PASSWORD = "your_password"
TWO_FACTOR_KEY = "your2factorkey"

<h4>If you dont have a 2 factor key or you need to get a new key:</h4>

1. Go to www.office.com and sign in
2. Click on the profile button in the upper right hand corner and click view account
3. Click on security info, then click on "Add sign-in method"
4. Choose authenticator app and click add
5. Click "I want to use a different authenticator app", then click next
6. Click "Can't scan image?"
7. Copy the "Secret key" and that is your 2 factor key

If you have that all set up and you have python installed, you should be good to run the system 1000 and 2000 tests!