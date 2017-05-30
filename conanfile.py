from conans import ConanFile
import os


class CTemplateConan(ConanFile):
    name = "CTemplate"
    version = "2.3"
    license = "BSD"
    url = "https://github.com/cjalmeida/conan-ctemplate"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def source(self):
        # Fetch sources from GitHub
        self.run("git clone https://github.com/OlafvdSpek/ctemplate")
        # Checkout the version we're targeting (latest release)
        self.run("cd ctemplate && git checkout ctemplate-%s" % self.version)

    def build(self):
        # "Install" artifacts into '<build_folder>/target'
        prefix = '--prefix="%s/target"' % os.path.abspath('.')
        # Select ./configure flags based on Conan options
        libmode = self.options.shared and "--enable-shared --disable-static" or "--disable-shared --enable-static"
        # Run usual ./configure && make && make install routine
        self.run('cd ctemplate && ./configure %s %s && make -j5 && make install' % (prefix, libmode))

    def package(self):
        # Select the artifacts we want in the Conan package
        # By default it recurses and keep the paths under the 'src' attribute folder
        self.copy("*.h", dst="include", src="target/include")
        self.copy("*", dst="lib", src="target/lib")

    def package_info(self):
        # Tell we need -lctemplate and -lpthread when using this package
        self.cpp_info.libs = ["ctemplate", "pthread"]
