#!/usr/bin/env python
from __future__ import print_function
from selenium import webdriver
from time import sleep
from sub_process import call
import webbrowser
"""
test the libraries' Google Forms which are hooked up to Google Apps Script
need to run this periodically since the forms tend to lose their ability to
send emails without warning, this checks that scripts still have permissions
"""

form_root = 'https://docs.google.com/a/cca.edu/forms/d/{0}/viewform'
forms = {
    'acquisitions': '17pKoZ_U8AHbFjEg4blXiJod8uZwKI0s1DFJBSSSB7rE',
    'ill': '1pyhf7krGP3PQX1McJIt1fwLUYAwUd88vGG1brC33qe8',
    'instruction': '1i6Xn0q3MI7EXM6VpxUr64oywifGDcU-4NZoitp2y7-g'
}
# values submitted through form
vals = {
    'first title': 'TEST Sweet Citation to First Title\n\ndoobie doowop bedoo',
    'name': 'Testy Testerson',
    'email': 'ephetteplace@cca.edu'
}


def test_recommendations():
    """
    test the recommended acquisitions form
    """
    browser.get(form_root.format(forms['acquisitions']))

    # first citation
    browser.find_element_by_id('entry_420214461').send_keys(vals['first title'])
    # leave blank a bunch of optional fields...
    # name
    browser.find_element_by_id('entry_967350359').send_keys(vals['name'])
    # CCA affilliation => Grad Student
    browser.find_element_by_id('group_942677086_1').click()
    # email
    browser.find_element_by_id('entry_1030731656').send_keys(vals['email'])
    # program => Writing/Literature/Comics
    browser.find_element_by_id('group_1569646515_7').click()

    # submit form
    browser.find_element_by_id('ss-submit').click()


def test_ill():
    """
    test the inter-library loan request form
    """
    browser.get(form_root.format(forms['ill']))
    # citation
    browser.find_element_by_id('entry_17105932').send_keys(vals['first title'])
    # name
    browser.find_element_by_id('entry_1904144554').send_keys(vals['name'])
    # email
    browser.find_element_by_id('entry_1309367559').send_keys(vals['email'])
    # CCA affilliation => Grad Student
    browser.find_element_by_id('group_2072708086_2').click()
    # department => Architecture
    # <select> drop-down, get appropriate <option>
    browser.find_element_by_id('entry_443514869').find_elements_by_tag_name(
        'option')[1].click()
    # submit form
    browser.find_element_by_id('ss-submit').click()


def test_instruction():
    """
    test the instruction session request form
    """
    browser.get(form_root.format(forms['instruction']))
    # wait for user to manually sign into Google
    # @TODO should automate this, probably by passing credentials on the cli
    print('Waiting to sign into Google, hit Return when done...')
    call('read')  # gotta be a native Python way to do this a/o/t shelling out
    # course name
    browser.find_element_by_id('entry_93795666').send_keys('TESTS-101')
    # date/time, string sent looks weird here but it's just the date
    # 01/01/200000 10:00 AM with the date/time autofill behavior
    browser.find_element_by_id('entry_608498536').send_keys('0101200000100A')
    browser.find_element_by_id('ss-submit').click()


def open_sheets():
    """
    Open the back-end spreadsheets for each form
    to see if entries were copied over properly
    """
    sheet_root = 'https://docs.google.com/spreadsheets/d/'
    sheets = {
        'acquisitions': '1A0bBB4_mYWtcWoqfB5HP6H7WbIWjTknzHnVr-5EPw8s/edit#gid=1311627534',
        'ill': '1V4yaJajQ37oGEFZXYxGcTtlF6Jq_XhQvZVGF4xBWO1k/edit#gid=275875544',
        'instruction': '1WpdyyvrVjCrWzHprUOZ1IlDmU2pQEb2qrzNML9G2JRw/edit#gid=1190654636'
    }
    for sheet in sheets:
        webbrowser.open(sheet_root + sheets[sheet])


if __name__ == '__main__':
    # PhantomJS is a preferable, faster option but it seems to choke
    # whereas an actual browser window does not
    # browser = webdriver.PhantomJS()
    browser = webdriver.Chrome()
    browser.implicitly_wait(30)

    for test in (test_recommendations, test_ill, test_instruction):
        test()
        sleep(1)

    open_sheets()
    browser.quit()
