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

import main

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class AdminHandler(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('rsvps.html')

    responded = len(main.Guest.query().fetch(130, keys_only=True))
    attending = len(main.Guest.query(main.Guest.attending == True).fetch(130, keys_only=True))

    results = []
    rsvps = main.Rsvp.query().order(main.Rsvp.created).fetch(150)
    for rsvp in rsvps:
      guests = main.Guest.query(ancestor=rsvp.key)
      results.append((rsvp, guests))

    template_values = {
      'responded': responded,
      'attending': attending,
      'results': results
    }
    self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/admin', AdminHandler)
], debug=True)
