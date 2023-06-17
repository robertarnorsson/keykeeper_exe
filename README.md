# Key Keeper

## Description
Key Keeper is a password management app designed to securely store your passwords locally on your computer. It provides a convenient and easy-to-use interface for managing your passwords without relying on external servers or cloud storage.

![Main screen in all available colors](https://github.com/RobertArnosson/keykeeper_exe/blob/main/assets/keykeeper_all_colors.png)

The passwords stored on your computer is highly encrypted in a way that only you on your computer with your personal password can decrypt them.

## Installation
To install and use Key Keeper, please follow these steps:

1. Clone or download the Key Keeper repository from [GitHub](https://github.com/RobertArnosson/keykeeper_exe) or download directly [Here](https://github.com/RobertArnosson/keykeeper_exe/archive/refs/heads/main.zip).
2. Extract the downloaded ZIP file to a preferred location on your computer.
3. Open the extracted folder and locate the `keykeeper` folder.
4. Inside the `keykeeper` folder, you will find the `keykeeper.exe` file. Double-click on it to run the program.

*Note: Key Keeper is currently only supported for Windows 10+ operating systems, but might work on other systems like MacOS, Linux and Ubuntu.*

*Important! Windows might say that it might be harmfull to run the `keykeeper.exe` file, but this is because it has no author yet. This will be fixed soon!*

## Usage
How to get to start using the Key Keeper app.

### How to create a new account 
1. Double click the `keykeeper.exe` file in the `keykeeper` folder
2. When the program opens click the button in the bottom right to create a new account.
![Add user button position](https://github.com/RobertArnosson/keykeeper_exe/blob/main/assets/keykeeper_add_user_button.png)
3. Enter a name that recognizes you *Example: `Jack` or `JackAccount`*
4. Enter a strong password that has lower and upper case letters, numbers and symbols. Recommended length is **14-16** characters! **Do NOT share this passord with anyone or save it in the app!**
5. When the account has been created just log into your newly created account.
Now your new account is made!

### How to add a new password
1. When logged in and at the main screen click the `Add` button at the top
![Add button position](https://github.com/RobertArnosson/keykeeper_exe/blob/main/assets/keykeeper_add_password_button.png)
2. Enter a title that shortly describes what is being saved. *Example: If you are saving a Google account the title can be `Google`*
3. Enter the username and password of what you want to save. *Example: username could be `jacksmith@gmail.com` and the password could be `S3cuRep4$$W0rdS950`*
4. Choose an icon with the arrow keys og click the icon if you wish to disable icons for that saved password.
6. Choose the filter that you want your saved passord to be in.
7. Click `Save Password` when you are ready to save your password.
Now you have added a new password to your account.

### How to add or remove a new filter
*Note: Icons are not currently supported for filters but will be added in the future*

**How to add**
1. When logged in and at the main screen click the plus icon beside the filter dropdown button
![Add button position](https://github.com/RobertArnosson/keykeeper_exe/blob/main/assets/keykeeper_add_filter_button.png)
2. Enter the name of your new filter. Example: `Google Mails` Note: Filters has a max length of 12 characters
3. Click the button called `Save Filter` to save the filter

**How to remove**
1. When logged in and at the main screen click the same plus icon as if you were going to add a filter
2. Click the filter dropdown button and select a filter that you want to be deleted
3. Click the button called `Remove Filter` to remove the filter *Note: A removed filter can't be recovered and every passord in the filter will be deleted!*

## What is coming
- More customization for the app to match your preferences
- Password generator
- Message encrypting

## Versions

### v1.0.0
- First release of the application!

### v1.0.1
- Removed keybind "`n`" for adding new user because it interfered when writing name or password
- Edited file structure

### v1.1.0
- Remake of the main screen
- Moved the viewing and adding of passwords to the main screen
- Added a hue slider to the settings for more customization
- Fixed bugs
