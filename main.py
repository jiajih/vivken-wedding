#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Rsvp(ndb.Model):
  comment = ndb.TextProperty()
  hotel = ndb.TextProperty()
  created = ndb.DateTimeProperty(auto_now_add=True)

class Guest(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  attending = ndb.BooleanProperty()
  shuttle = ndb.BooleanProperty()
  attending_beach = ndb.BooleanProperty()
  attending_aquarium = ndb.BooleanProperty()
  allergies = ndb.TextProperty()

class MainHandler(webapp2.RequestHandler):
  def get(self):
    if self.request.cookies.get('guest'):
      template = JINJA_ENVIRONMENT.get_template('index.html')
    else:
      template = JINJA_ENVIRONMENT.get_template('login.html')
    self.response.write(template.render())

  def post(self):
    password = self.request.get('password')
    if password.lower() == 'honolulu':
      self.response.set_cookie('guest', value='true', domain='coopergetsparents.com')
      template = JINJA_ENVIRONMENT.get_template('index.html')
    else:
      template = JINJA_ENVIRONMENT.get_template('login.html')
    self.response.write(template.render())

class RsvpHandler(webapp2.RequestHandler):
  def post(self):
    rsvp = Rsvp()
    rsvp.comment = self.request.get('comment')
    rsvp.hotel = self.request.get('hotel')
    rsvp_key = rsvp.put()

    arguments = self.request.arguments()
    guest_index = 0
    while 'first_name_' + str(guest_index) in arguments:
      guest = Guest(parent=rsvp_key)
      guest.first_name = self.request.get('first_name_' + str(guest_index))
      guest.last_name = self.request.get('last_name_' + str(guest_index))
      guest.attending = self.request.get('attending_' + str(guest_index)) == 'true'
      guest.shuttle = self.request.get('shuttle_' + str(guest_index)) == 'true'
      guest.attending_beach = self.request.get('attending_beach_' + str(guest_index)) == 'true'
      guest.attending_aquarium = self.request.get('attending_aquarium_' + str(guest_index)) == 'true'
      guest.allergies = self.request.get('allergies_' + str(guest_index))
      guest.put()
      guest_index += 1

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/rsvp', RsvpHandler)
], debug=True)
