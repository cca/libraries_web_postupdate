#!/usr/bin/env python
import argparse
from selenium import webdriver
from time import sleep

parser = argparse.ArgumentParser(description='Submit the Course Reserves form \
on the library website as a way to test module/Drupal upgrades.')
parser.add_argument('--live', dest="live", help='test the course reserves form \
on the live website', action='store_true')
parser.add_argument('--email', help='email address to submit through form',
                    default='ephetteplace@cca.edu')
parser.set_defaults(live=False)

args = parser.parse_args()

# default to dev site
if args.live:
    root = 'http://libraries.cca.edu/'
else:
    root = 'https://vm-lib-www-dev-01/'

path = 'content/course-reserves-request'
url = root + path
# values submitted through form
vals = {
    'instructor': 'Testy Testerson',
    'course': 'Testing 101',
    'email': args.email
}

# PhantomJS should be a preferable, faster option but it seems to choke
# whereas an actual browser window does not
# browser = webdriver.PhantomJS()
browser = webdriver.Chrome()
browser.implicitly_wait(30)

browser.get(url)

# location radio button
browser.find_element_by_id('edit-submitted-course-and-contact-information-\
course-reserves-requested-for-1').click()
# semester <select> drop-down, get first <option>
browser.find_element_by_id('edit-submitted-course-and-contact-information-\
semester').find_elements_by_tag_name('option')[1].click()
# instructor
browser.find_element_by_id('edit-submitted-course-and-contact-information-\
instructor').send_keys(vals['instructor'])
# course title
browser.find_element_by_id('edit-submitted-course-and-contact-information-\
course-title').send_keys(vals['course'])
# email
browser.find_element_by_id('edit-submitted-course-and-contact-information-\
email-addr').send_keys(vals['email'])

# submit the form
browser.find_element_by_id('edit-submit').click()

sleep(2)
browser.quit()
