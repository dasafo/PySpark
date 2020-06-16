import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json


# Set up your credentials
consumer_key='u89miYwyHmPu2XHdrgJqWPcBU'
consumer_secret='J9uBls2k8nSUqiifl0xoFJDQ93Pf8cGH3G14kOwKK1dGgC9we2'
access_token ='754714491875684352-ZXeKu9MNs4Xk8nyMI6sqvZl8LrbEku2'
access_secret='elZhit57ybWPAnf8gswTcas30MzP97aCb2oWavel1Xtsa'


class TweetsListener(StreamListener):

  def __init__(self, csocket):
      self.client_socket = csocket

  def on_data(self, data):
        try:
            msg = json.loads( data ) # Create a message from json file
            print( msg['text'].encode('utf-8') ) # Print the message and UTF-8 coding will eliminate emojis
            ## self.client_socket.send( msg['text'].encode('utf-8') )  this line is wrong , add the "\n" 
            self.client_socket.send((str(msg['text']) + "\n").encode('utf-8'))
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

  def on_error(self, status):
      print(status)
      return True

def sendData(c_socket):
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)

  twitter_stream = Stream(auth, TweetsListener(c_socket))
  twitter_stream.filter(track=['soccer'])

if __name__ == "__main__":
  s = socket.socket()         # Create a socket object
  host = "127.0.0.1"     # Get local machine name
  port = 9998                 # Reserve a port for your service.
  s.bind((host, port))        # Bind to the port

  print("Listening on port: %s" % str(port))

  s.listen(5)                 # Now wait for client connection.
  c, addr = s.accept()        # Establish connection with client.

  print( "Received request from: " + str( addr ) )

  sendData( c )