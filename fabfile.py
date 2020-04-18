import os
from fabric.api import *

# globals
env.project_name = os.path.basename(os.getcwd()) ## maybe change this
env.do_backup = True
env.do_migrate = True
env.do_synccompress = False
env.do_collectstatic = True
env.extra_fixtures = '' #["fixtures/sites.json"]

def run_manage(cmd):
    ### PYTHONPATH here is alwaysdata specific - strange things going on with virtualenvs there ; wasnt needed perviously
    run("%s %s" % (
        "cd %(path)s ; PYTHONPATH=/usr/local/lib/python2.6/site-packages/ %(runtime_path)s/bin/python manage.py" % env,
        cmd))

def quick():
    env.do_backup = False

def alwaysdata():
    env.hosts = ['ssh.alwaysdata.com']
    env.user = "deucalion"
    env.homedir = '/home/%(user)s/' % env
    
    env.local_settings_file = "local_settings_alwaysdata.py"
    env.destination_root = '%(homedir)s/production/' % env
    env.backups_root = '%(homedir)s/backups/' % env
    env.runtime_path = '%(homedir)s/runtime/%(project_name)s/' % env
    env.sitepackages_path = '%(runtime_path)slib/python2.6/site-packages/' % env
    env.path = '%(destination_root)s/%(project_name)s' % env
##    env.admin_media_root = "%(sitepackages_path)s/django/contrib/admin/media" % env

def production():
    alwaysdata()
    env.target_name = "production"

def preprod():
    alwaysdata()
    env.local_settings_file = "local_settings_alwaysdata_preprod.py"
    env.destination_root = '%(homedir)s/preprod/' % env
    env.path = '%(destination_root)s/%(project_name)s' % env
    env.target_name = "preprod"

def setup():
    ## setup directory layout
    run("mkdir -p %(backups_root)s" % env)
    run("mkdir -p %(destination_root)s" % env)
    run("mkdir -p %(runtime_path)s" % env)
    run("mkdir -p %(sitepackages_path)s" % env)

    run("PYTHONPATH=%(sitepackages_path)s easy_install --prefix %(runtime_path)s virtualenv==1.10.1" % env)
    run("PYTHONPATH=%(sitepackages_path)s %(runtime_path)s/bin/virtualenv %(runtime_path)s" % env)
    put("requirements.txt", "%(runtime_path)s/requirements.txt" % env)
    run("PYTHONPATH=%(sitepackages_path)s %(runtime_path)s/bin/pip install -U setuptools" % env)
    run("PYTHONPATH=%(sitepackages_path)s %(runtime_path)s/bin/pip install -r %(runtime_path)s/requirements.txt" % env)

    ## ## setup django env
    ## #run("virtualenv %(runtime_env)s" % env)
    ## put("requirements.txt", "%(destination_root)s/requirements.txt" % env)
    ## run("pip -E %(runtime_env)s install -r %(destination_root)s/requirements.txt" % env)

def configure():
    if env.local_settings_file:
        run("ln -fs %(path)s/%(local_settings_file)s %(path)s/local_settings.py" % env)
    env.public_path = "%(path)s/public" % env
    run("mkdir -p %(public_path)s" % env)
    run("chmod +x %(path)s/deploy/django.fcgi" % env)
    run("ln -fs %(path)s/deploy/django.fcgi %(public_path)s" % env)
    run("ln -fs %(path)s/deploy/htaccess %(public_path)s/.htaccess" % env)
    run("ln -fs %(sitepackages_path)s %(path)s/deploy/site-packages" % env)
    run("ln -fs %(path)s/media %(public_path)s/" % env)
    run("ln -fs %(path)s/static %(public_path)s/" % env)
##    run("mkdir -p %(public_path)s/admin/" % env)
##    run("ln -fs %(admin_media_root)s %(public_path)s/admin/" % env)
    
    run_manage("syncdb --noinput")

    if env.do_migrate:
        run_manage("migrate")
    if env.do_collectstatic:
        run_manage("collectstatic --noinput")
    if env.do_synccompress:
        run_manage("synccompress")

    for fixture in env.extra_fixtures:
        run_manage("loaddata %s" % fixture)
   
def deploy():
    import datetime
    #require('env', provided_by=['production','staging'])
    env.temp_dir = "/tmp/deploy-%(project_name)s" % env
    env.timestamp = datetime.datetime.now().strftime("%y%m%d%H%M")
    env.tar_filename = "%(project_name)s-%(timestamp)s.tgz" % env
    env.backup_filename = "%(project_name)s-%(target_name)s-%(timestamp)s" % env
    # create and upload tar
    local("rm -rf '%(temp_dir)s'" % env)
    local("mkdir -p '%(temp_dir)s'" % env)
    if os.path.exists(".svn"):
        local("svn export . %(temp_dir)s/%(project_name)s" % env)
    elif os.path.exists(".git"):
        local("git archive --prefix %(project_name)s/ HEAD | gzip >%(temp_dir)s/%(tar_filename)s" % env)
        
    run("mkdir -p %(destination_root)s %(backups_root)s" % env)
    put("%(temp_dir)s/%(tar_filename)s" % env, "%(destination_root)s" % env)

    if env.do_backup:
        test = run("test -d %(destination_root)s/%(project_name)s || echo NOTFOUND" % env)
        if not test == "NOTFOUND":
            run ("cp -a %(destination_root)s/%(project_name)s %(backups_root)s/%(backup_filename)s" % env)
    run("tar -C %(destination_root)s -xvzf %(destination_root)s/%(tar_filename)s " % env)
    configure()
