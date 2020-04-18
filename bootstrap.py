# -*- coding: utf-8 -*-
"""

* must be enough to setup whole environment when run the first time
* can be run as many times as you want, putting env up to date

Linux

apt-get install python python-setuptools python-virtualenv

Windows

Install: Python + setuptools (required):
* http://www.python.org/getit/
** http://www.python.org/ftp/python/2.7.1/python-2.7.1.msi
* http://pypi.python.org/pypi/setuptools#windows
** http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe

Configure: Parameters -> Advanced -> Environment variables -> Add PATH = ;C:\Python27;C:\Python27\Scripts

Install: Git (optional):
* http://msysgit.googlecode.com
** http://msysgit.googlecode.com/files/msysGit-fullinstall-1.7.4-preview20110204.exe


Install: PIL (optional):
* http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe

On Git bash:
$ git clone labs@labs.rlabs.fr:projects/rs-project-base \c\MyProject

On cmd.exe:
> cd C:\MyProject
> python bootstrap.py
> env\Scripts\activate.bat
> python manage.py runserver

"""

import logging, os, sys, shutil
import subprocess

project_directory = os.path.abspath(os.path.dirname(__file__))
project_name = os.path.basename(project_directory)
env_directory = os.path.join(project_directory, "env")
if sys.platform == 'win32':
    bin_directory = os.path.join(env_directory, 'Scripts')
    p = os.getenv("PATH")
    os.putenv("PATH",
              p+";%(prefix)s;%(prefix)s\Scripts" % {'prefix':sys.prefix})
else:
    bin_directory = os.path.join(env_directory, 'bin')


def run(options, args):
    logging.info("*** Bootstrapping environment...")
    bootstrap_env(options, args)
    
    logging.info("*** Installing dependencies...")
    install_dependencies(options, args)
    
    check_local_settings(options, args)
    
    logging.info("*** Running management commands...")
    manage_helper("syncdb")
    manage_helper("migrate")

    try:
        from main import settings 
    except ImportError:
        logging.error("Couldn't import settings")
        sys.exit(-1)

    if "south" in settings.INSTALLED_APPS:
        manage_helper("migrate")
    if "appmedia" in settings.INSTALLED_APPS:
        if sys.platform == "win32":
            apps = [
                (app, "env\\Lib\\site-packages\\%s\\" % app)
                for app in settings.INSTALLED_APPS
                if os.path.exists("env\\Lib\\site-packages\\%s\\" % app)
                ]
            symlinkmedia_helper_win32(apps)
        else:
            manage_helper("symlinkmedia")
    logging.info("Setup done")
    
    if sys.platform == 'win32':
        logging.info(r"Don't forget to run > env\Scripts\activate.bat")
    else:
        logging.info("Don't forget to run $ source env/bin/activate")

def check_local_settings(options, args):
    from main import settings
    if not settings.DATABASES["default"]["ENGINE"]:
        p = os.path.join(project_directory, "local_settings.py")
        if not os.path.exists(p):
            a = raw_input("Create local_settings.py ? (Y/n)")
            if not a or a in "yY":
                shutil.copy(p+"-dist", p)
                logging.info("Created %s" % p)
    
    

def bootstrap_env(options, args):
    try:
        import setuptools
    except ImportError:
        logging.error("setuptools not installed (http://pypi.python.org/pypi/setuptools#installation-instructions)")
        sys.exit(-1)

    if not os.path.exists(env_directory) and not options.force_virtualenv:
        try:
            import virtualenv
            v = virtualenv.virtualenv_version
            logging.info("virtualenv found")
        except ImportError:
            logging.warning("virtualenv not found, installing...")
            easy_install_helper("virtualenv")
            if not sys.platform == 'win32': ## TODO
                import virtualenv
                logging.info("virtualenv installed (path=%s)" % virtualenv.__file__)
        ## virtualenv_options = dict(site_packages=True, clear=False)
        ## virtualenv.create_environment(env_directory, **virtualenv_options)
        virtualenv_helper(env_directory)


def install_dependencies(options, args):
    from setuptools.command import easy_install

    try:
        import pip
        logging.info("pip found")
    except ImportError:
        logging.warning("pip not found, installing...")
        easy_install_helper("pip")
        if not sys.platform == 'win32': ## TODO
            import pip
            logging.info("pip installed")

    pip_helper(env_directory, "requirements.txt")

class ManagementCommandError(Exception): pass
def manage_helper(*args):
    logging.info("Calling manage %s" % (" ".join(args)))
    if not subprocess.call((os.path.join(bin_directory, "python"),
                            "manage.py")+args)==0:
        raise ManagementCommandError

def symlinkmedia_helper_win32(apps, media_path="media"):
    import shutil
    for app_name, app_path in apps:
        ## app_file = os.path.abspath(app.__file__)
        ## if os.path.splitext(app_file)[0].endswith('/__init__'):
        ##     # models are an folder, go one level up
        ##     app_file = os.path.dirname(app_file)

        ## app_path = os.path.dirname(app_file)
        if 'media' in os.listdir(app_path) and os.path.isdir(os.path.join(app_path,'media')):
            app_media = os.path.join(app_path, "media", app_name)
            if not os.path.isdir(app_media):
                app_media = os.path.join(app_path, "media")                
            try:
                shutil.copytree(app_media, os.path.join(media_path, app_name))
                print " + added %s as %s" % (app_media, os.path.join(media_path, app_name))
            except OSError, e:
                if e.errno == 17:
                    pass
                    print " o skipping %s" % app_media
                else:
                        raise

class EasyInstallCommandError(Exception): pass
def easy_install_helper(package):
    logging.info("Calling easy_install %s" % package)
    if not subprocess.call(("easy_install", package))==0:
        raise EasyInstallCommandError    

class VirtualenvCommandError(Exception): pass
def virtualenv_helper(directory):
    logging.info("Calling virtualenv %s" % directory)
    if not subprocess.call(("virtualenv", directory))==0:
        raise VirtualenvCommandError    

def pip_helper(env_directory, requirement_file_path):
    logging.info("Calling pip on %s from %s" % (env_directory, requirement_file_path))
    pip_path = os.path.join(bin_directory, "pip")
    subprocess.call([pip_path, "install", 
                     "-r", requirement_file_path])




def main():
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="print many status messages to stdout")
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="don't print status messages to stdout")
    parser.add_option("--force-virtualenv",
                      action="store_true", dest="force_virtualenv", default=False,
                      help="don't rebuild virtualenv if exists")

    (options, args) = parser.parse_args()

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif options.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    run(options, args)

if __name__=="__main__":
    main()
