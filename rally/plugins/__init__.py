# Copyright 2015: Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os

import decorator

from rally.common.plugin import discover


PLUGINS_LOADED = False


def load():
    global PLUGINS_LOADED

    if not PLUGINS_LOADED:
        from rally.common import opts

        opts.register()

        discover.import_modules_from_package("rally.plugins.common")

        packages = discover.find_packages_by_entry_point()
        for package in packages:
            if "options" in package:
                opts.register_options_from_path(package["options"])
        discover.import_modules_by_entry_point(_packages=packages)

        discover.load_plugins("/opt/rally/plugins/")
        discover.load_plugins(os.path.expanduser("~/.rally/plugins/"))

    PLUGINS_LOADED = True


@decorator.decorator
def ensure_plugins_are_loaded(f, *args, **kwargs):
    load()
    return f(*args, **kwargs)
