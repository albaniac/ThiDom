#!/usr/bin/python

import sys
import httplib2
import base64
from apiclient.discovery import build
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client import tools
import argparse
import mimetypes
import os

from apiclient import errors
import base64


# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'client_secret_643056256426-oc23as400lm6rkt91umqbnbu9nac3ers.apps.googleusercontent.com.json'

# Check https://developers.google.com/gmail/api/auth/scopes
# for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'

STORAGE = Storage('gmail.storage')

flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
http = httplib2.Http()

flags = tools.argparser.parse_args(args=[])

# Try to retrieve credentials from storage or run the flow to generate them
credentials = STORAGE.get()

if credentials is None or credentials.invalid:
  credentials = tools.run_flow(flow, STORAGE, flags)


# Authorize the httplib2.Http object with our credentials
http = credentials.authorize(http)

# Build the Gmail service from discovery
gmail_service = build('gmail', 'v1', http=http)


def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
  sender: Email address of the sender.
  to: Email address of the receiver.
  subject: The subject of the email message.
  message_text: The text of the email message.

  Returns:
  An object containing a base64 encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.b64encode(message.as_string())}



def CreateMessageWithAttachment(sender, to, subject, message_text, file_dir,
                                filename):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file_dir: The directory containing the file to be attached.
    filename: The name of the file to be attached.

  Returns:
    An object containing a base64 encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  path = os.path.join(file_dir, filename)
  content_type, encoding = mimetypes.guess_type(path)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(path, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(path, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(path, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(path, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()

  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.b64encode(message.as_string())}


def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
  service: Authorized Gmail API service instance.
  user_id: User's email address. The special value "me"
  can be used to indicate the authenticated user.
  message: Message to be sent.

  Returns:
  Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message).execute())
    #print 'Message Id: %s' % message['id']
    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


#print sys.argv[1]
#print sys.argv[2]
#print sys.argv[3]

message = CreateMessage(sender='**@**.com', to=sys.argv[1], subject=sys.argv[2], message_text=sys.argv[3])

SendMessage(gmail_service, 'me', message)
