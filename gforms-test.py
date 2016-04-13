#!/usr/bin/env python
from __future__ import print_function
from selenium import webdriver
from time import sleep
from subprocess import call
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


def fill_in(label, value):
    """
    Given ARIA label, fill in all matching form inputs with provided value
    """
    # find_elements type method return lists
    for el in browser.find_elements_by_css_selector('[aria-label="' + label + '"]'):
        el.send_keys(value)


def click(label):
    """
    Given ARIA label, click the DOM element
    """
    browser.find_elements_by_css_selector('[aria-label="' + label + '"]')[0].click()


def test_recommendations():
    """
    test the recommended acquisitions form
    """
    browser.get(form_root.format(forms['acquisitions']))

    # first citation
    fill_in("First Title", vals['first title'])
    # leave blank a bunch of optional fields...
    # name
    fill_in("Name", vals['name'])
    # CCA affilliation => Grad Student
    click("Graduate Student")
    # email
    fill_in("Email", vals['email'])
    # program => Writing/Literature/Comics
    click("Writing/Literature/Comics")

    # submit form
    browser.find_element_by_tag_name('form').submit()


def test_ill():
    """
    test the inter-library loan request form
    """
    browser.get(form_root.format(forms['ill']))
    # citation
    fill_in('Citation', vals['first title'])
    # name
    fill_in('Name', vals['name'])
    # email
    fill_in('Email', vals['email'])
    # CCA affilliation => Grad Student
    click('Graduate Student')
    # Department drop-down is complicated because choices are hidden & cannot be clicked
    # We need to do something like click Department label, click specific option
    drop_down = browser.find_elements_by_css_selector('[aria-label="Department"]')[0]
    dept = browser.find_elements_by_css_selector('[aria-label="Architecture"]')[0]
    # http://selenium-python.readthedocs.org/api.html#module-selenium.webdriver.common.action_chains
    webdriver.ActionChains(browser).click(drop_down).move_to_element(dept).click(dept).perform()
    # submit form
    browser.find_element_by_tag_name('form').submit()


def test_instruction():
    """
    test the instruction session request form
    """
    browser.get(form_root.format(forms['instruction']))
    # wait for user to manually sign into Google
    # @TODO should automate this, probably by passing credentials on the CLI
    print('Waiting to sign into Google, hit Return when done...')
    call('read')  # gotta be a native Python way to do this w/o shelling out
    # course name
    fill_in('Course', 'TESTS-101')
    # date/time, string is more complicated to do, multi-part input
    # we set to 01/01/2000 10:10 AM
    for el in browser.find_elements_by_css_selector('input[type="date"]'):
        el.send_keys('01012000')
    fill_in('Hour', '10')
    fill_in('Minute', '10')
    # AM is default so we don't need to specify
    browser.find_element_by_tag_name('form').submit()


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
