# Instollowing

![GitHub Release](https://img.shields.io/github/v/release/jabibamman/instollowing)
[![codecov](https://codecov.io/gh/jabibamman/instollowing/graph/badge.svg?token=H6H59NPSDB)](https://codecov.io/gh/jabibamman/instollowing)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=jabibamman_instollowing&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=jabibamman_instollowing)

Instollowing is a simple script to get the list of people who are following and not following you back on Instagram.

## Usage

> Make you sure you have Python 3 installed on your machine.

1. Clone the repository using `git clone git@github.com:jabibamman/instollowing.git`
2. Install the requirements using `pip install -r requirements.txt`

At this point, you can either use the script with your own credentials or use json files containing your data provided by Instagram.

3. Download your data from Instagram by following these steps:
    - Go to your Instagram profile and click on the `Settings` button.
    - Then click on `Security and Login`.
    - Then click on `Download Data`.
    - Then click on `Request Download`.
    - Specify the date range and the file format.
    - Wait for Instagram to send you an email with a link to download your data.
    - Download the data and unzip it.
    - The link is : https://accountscenter.instagram.com/info_and_permissions/dyi/
    
4. Drag _`following.json`_ and _`followers.json`_ into the project folder (to get these files, go to your Instagram profile and click on the
`Settings` button. Then click on `Security and Login` and then click on `Download Data`.)
   
    - Or, you can use your own instagram credentials by creating a file named _`credentials.json`_ and add your username and password in the following format:
    
```json  
{
     "username": "your_username",
     "password": "your_password"
}
```
    
   
5. Run the script using `python instollowing.py`
6. Wait for the script to finish running
7. Check the output file
8. Enjoy and unfollow those who don't follow you back because they are not your friends :D.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
