from __future__ import print_function
import os, shutil
from conans import ConanFile, RunEnvironment, tools

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "demo")


class CTemplateConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "CTemplate/2.3@%s/%s" % (username, channel)
    generators = ["gcc"]
    exports_sources = ['example.cpp', 'example.tpl']
    options = {'shared': [True, False]}
    default_options = "shared=False"

    def build(self):
        srcdir = self.conanfile_directory
        shutil.copy(srcdir + '/example.tpl', '.')
        self.run('g++ "%s/example.cpp" @conanbuildinfo.gcc -o example' % srcdir)

    def test(self):
        env = RunEnvironment(self)
        with tools.environment_append(env.vars):
            self.run(os.path.join('.', 'example'))
