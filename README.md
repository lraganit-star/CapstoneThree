
# Introduction
The mood maker is a program that is able to detect 4 different emotions using the user's webcam. These being angry, happy, neutral and sad. From these detected emotions, given the playlist and user APIs, the program will then provide a song from the user's playlist that would best fit their mood.


# Libraries Used
* Pandas
* NumPy
* Os
* Glob
* Pillow
* TensorFlow
* Keras
* Scikit-Learn
* CV2
* iMutils
* Spotipy


# Components
There are going to be multiple components that go into the project. One cannot just poof a machine learning project into existence, instead it is broken down into different parts and then combined together. I had first created a model that can differentiate the different emotions shown on a human's face and then placed that model into a program that can connect to the user's webcam. Afterwards, the detected emotion would get input into the recommender system in order to produce a song that is correlated with the user's emotions. 

## Creating the Emotion Model

### Data

In order to create a program that can detect emotions, we have to teach a computer how the facial expressions on a person's face changes as they go through the four different indicated emotions. This is done by feeding multiple images of each of the different expressions and creating a convolutional neural network. This part has an assumption built into the model. Not everybody expresses their emotions the same way especially outwardly on their face. The images that get fed into the CNN are going to be stereotypical in the sense that the faces within the images are going to be smiling when happy and frowning when sad. The images that were used came from the following Kaggle data set.

## Connecting to Webcamera


## Spotify Recommender System


# How to use
![](user_uri.png)
![](playlist_uri.png)
