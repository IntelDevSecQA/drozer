import fnmatch
import glob
import os
import setuptools

from drozer import meta

def find_files(src):
    matches = []
    
    for root, dirnames, filenames in os.walk(src):
        matches.extend(map(lambda f: os.path.join(root, f), filenames))
    
    return matches

def find_libs(src):
    matches = []
    
    for root, dirnames, filenames in os.walk(src):
        for filename in fnmatch.filter(dirnames, 'lib'):
            matches.extend(glob.glob(os.path.join(root, filename, "*", "*")))
        for filename in fnmatch.filter(dirnames, 'libs'):
            matches.extend(glob.glob(os.path.join(root, filename, "*", "*")))

    return map(lambda fn: os.path.basename(fn), matches)
    
setuptools.setup(
  name = meta.name,
  version = meta.version,
  author = meta.vendor,
  author_email = meta.contact,
  description = meta.description,
  long_description = open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
  license = meta.license,
  keywords = meta.keywords,
  url = meta.url,

  packages = setuptools.find_packages("src"),
  package_dir = {   "drozer": "src/drozer",
                    "mwr": "src/mwr",
                    "pydiesel": "src/pydiesel" },
  package_data = { "": ["*.apk", "*.bks", "*.crt", "*.jar", "*.key", "*.sh", "busybox"] + find_libs("src"),
                   "drozer": ["lib/*.apk",
                              "lib/*.jar" ] + \
                              map(lambda f: f[11:], find_files("src/drozer/lib/gui-agent")) + \
                              map(lambda f: f[11:], find_files("src/drozer/lib/guiless-agent")) + \
                              map(lambda f: f[11:], find_files("src/drozer/lib/jdiesel")) + \
                              map(lambda f: f[11:], find_files("src/drozer/lib/mwr-android")) + \
                              map(lambda f: f[11:], find_files("src/drozer/lib/mwr-tls")) + \
                            [ "lib/weasel/*",
                              "server/web_root/*" ] },
  scripts = ["bin/drozer", "bin/drozer-complete"],
  install_requires = ["protobuf==2.4.1", "pyopenssl==0.13"],
  classifiers = [])
