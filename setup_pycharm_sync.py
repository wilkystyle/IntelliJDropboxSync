#!/usr/bin/env python

# A Python script for syncing your PyCharm configuration across multiple
# machines using your Dropbox folder.
#
# Author: Mike Wilkerson
# Email: wilkystyle@gmail.com
# Version: 0.2.0
#
# USAGE:
# Run this file from the root of your Dropbox folder.
#
# NOTE: This has been tested on OSX 10.8.5, and using PyCharm 3.0. Your
# results may vary.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import re
import sys

# This dictionary lists the known configuration values for a given platform. To
# support additional platforms, provide the appropriate values in a nested
# dictionary here.
config_dict = {
    "darwin": {
        # The os command to clear the screen.
        "clear_cmd": "clear",
        # The Dropbox dir. Assumes that this script was run from within the
        # user's Dropbox folder.
        "dropbox_dir": os.path.dirname(os.path.abspath(__file__)),
        # A list of known JetBrains products that we can sync. JetBrains stores
        # configuration information in directories with the <PRODUCT><VERSION>
        # naming structure, so populate the list below with case-insensitive
        # versions of the <PRODUCT> string for this script to match on.
        "products": [
            "idea",
            "pycharm",
        ],
        # A list of directories that need to be synced to Dropbox. This is a
        # list, since JetBrains spreads its configuration over multiple
        # directories on OS X.
        "sync_dirs": [
            # Apple's preferences folder.
            os.path.join(
                os.path.expanduser("~"),
                "Library",
                "Preferences",
            ),
            # Apple's application support folder.
            os.path.join(
                os.path.expanduser("~"),
                "Library",
                "Application Support",
            ),
        ]
    }
}

# Get the configuration for the current platform.
config = config_dict.get(sys.platform)
if not config:
    print "This script does not support the {} platform!".format(
        sys.platform,
    )
    sys.exit(1)


def get_installed_products():
    """
    A utility function that will return a list of all installed JetBrains
    products that we can sync.
    """
    regex_string = "({})".format("|".join(config['products']))
    reg = re.compile(regex_string, re.IGNORECASE)

    # Get the first (or only) directory we want to sync...
    search_dir = config['sync_dirs'][0]

    # And then get a list of all directories which match known products.
    products = [x for x in os.listdir(search_dir) if reg.match(x.lower())]

    # Return a list of products.
    to_return = []
    for product in products:
        to_return.append({
            "name": product,
            # See if we have already symlinked this product.
            "synced": os.path.islink(
                os.path.join(search_dir, product)
            ),
        })
    return to_return


def verify_path(the_path):
    """
    Simple utility function for verifying that a path exists on the filesystem.
    """
    if not os.path.exists(the_path):
        raise Exception("Could not find path {}".format(the_path))
    else:
        return True


def list_products(products):
    for index, product in enumerate(products):
        print "{}: {}	(Synced: {})".format(
            index,
            product['name'],
            product['synced'],
        )

#
# # Get the user's home and dropbox folders.
# dropbox_sync_dir = os.path.join(
#     dropbox_dir,
#     'pycharm3_settings',
# )
#
# dropbox_preferences = os.path.join(
#     dropbox_sync_dir,
#     'preferences',
# )
#
# dropbox_app_support = os.path.join(
#     dropbox_sync_dir,
#     'app_support',
# )
#
# # Make sure we can find the Preferences folder for PyCharm.
# pycharm_preferences = os.path.join(
#         home_dir,
#         'Library',
#         'Preferences',
#         'PyCharm30',
#     )
# verify_path(pycharm_preferences)
#
# preferences_backup = os.path.join(
#         home_dir,
#         'Library',
#         'Preferences',
#         'PyCharm30_OLD',
#     )

# # Make sure preferences_backup exists.
# if not os.path.exists(preferences_backup):
#     print
#     print "Creating {0}".format(
#         preferences_backup
#     )
#     print
#     os.makedirs(preferences_backup)

# # Make sure we can find the Application Support folder for PyCharm.
# pycharm_application_support = os.path.join(
#         home_dir,
#         'Library',
#         'Application Support',
#         'PyCharm30',
#     )
# verify_path(pycharm_application_support)


# application_support_backup = os.path.join(
#         home_dir,
#         'Library',
#         'Application Support',
#         'PyCharm30_OLD',
#     )

# # Make sure application_support_backup exists.
# if not os.path.exists(application_support_backup):
#     print
#     print "Creating {0}".format(
#         application_support_backup
#     )
#     print
#     os.makedirs(application_support_backup)

# print
# print "home_dir is {0}".format(home_dir)
# print "dropbox_dir is {0}".format(dropbox_dir)
# print
# print "dropbox_preferences is {0}".format(dropbox_preferences)
# print "dropbox_app_support is {0}".format(dropbox_app_support)
# print
# print "pycharm_preferences is {0}".format(pycharm_preferences)
# print "preferences_backup is {0}".format(preferences_backup)
# print
# print "pycharm_application_support is {0}".format(pycharm_application_support)
# print "application_support_backup is {0}".format(application_support_backup)
# print

# if not os.path.exists(dropbox_sync_dir):
#     print "First time running this script..."
#     print "Creating {}".format(dropbox_sync_dir)
#     os.makedirs(dropbox_sync_dir)

if __name__ == "__main__":
    installed_products = get_installed_products()
    error_msg = ""
    title_msg = "         JetBrains Dropbox Sync"
    sep_line = "--------------------------------------------"
    help_msg = "(Enter a number below, or type q to quit)"
    product = None

    while True:
        os.system(config['clear_cmd'])
        print title_msg
        print sep_line
        print help_msg
        print error_msg
        print
        list_products(installed_products)
        cmd = raw_input("Select the product to sync: ")
        if cmd.lower() == "q":
            sys.exit(0)
        try:
            selection = int(cmd)
            product = installed_products[selection]
            break
        except ValueError:
            error_msg = (
                "ERROR: Please enter the number corresponding to the product "
            )
        except IndexError:
            error_msg = (
                "ERROR: Please choose one of the products listed below!"
            )

    print "You have selected {}!".format(product['name'])

    # if os.path.islink(pycharm_preferences):
    #     print "{0} is already symlinked! Skipping...".format(
    #         pycharm_preferences
    #     )
    # elif not os.path.exists(dropbox_preferences):
    #     print "Moving from {0} to {1}".format(
    #         pycharm_preferences,
    #         dropbox_preferences,
    #     )
    #
    #     # Move the file to the backup directory.
    #     os.rename(pycharm_preferences, dropbox_preferences)
    #
    #     # Then create a symlink back where we just moved it from.
    #     print "Creating a symlink at {0} to {1}".format(
    #         pycharm_preferences,
    #         dropbox_preferences
    #     )
    #     os.symlink(dropbox_preferences, pycharm_preferences)
    # else:
    #     print "Moving from {0} to {1}".format(
    #         pycharm_preferences,
    #         preferences_backup,
    #     )
    #
    #     # Move the file to the backup directory.
    #     os.rename(pycharm_preferences, preferences_backup)
    #
    #     # Then create a symlink back where we just moved it from.
    #     print "Creating a symlink at {0} to {1}".format(
    #         pycharm_preferences,
    #         dropbox_preferences
    #     )
    #     os.symlink(dropbox_preferences, pycharm_preferences)
    #
    # if os.path.islink(pycharm_application_support):
    #     print "{0} is already symlinked! Skipping...".format(
    #         pycharm_application_support
    #     )
    # elif not os.path.exists(dropbox_app_support):
    #     print "Moving from {0} to {1}".format(
    #         pycharm_application_support,
    #         dropbox_app_support,
    #     )
    #
    #     # Move the file to the backup directory.
    #     os.rename(pycharm_application_support, dropbox_app_support)
    #
    #     # Then create a symlink back where we just moved it from.
    #     print "Creating a symlink at {0} to {1}".format(
    #         pycharm_application_support,
    #         dropbox_app_support
    #     )
    #     os.symlink(dropbox_app_support, pycharm_application_support)
    # else:
    #     print "Moving from {0} to {1}".format(
    #         pycharm_application_support,
    #         application_support_backup,
    #     )
    #
    #     # Move the file to the backup directory.
    #     os.rename(pycharm_application_support, application_support_backup)
    #
    #     # Then create a symlink back where we just moved it from.
    #     print "Creating a symlink at {0} to {1}".format(
    #         pycharm_application_support,
    #         dropbox_app_support
    #     )
    #     os.symlink(dropbox_app_support, pycharm_application_support)
