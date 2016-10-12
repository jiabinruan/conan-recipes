from conans import ConanFile, CMake, tools
from conans.tools import download, unzip, untargz 
import os


class OracleinstantclientConan(ConanFile):
    name = "oracle-instantclient"
    version = "11.2"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    unzip_file = "oracle-instantclient-%s" % version
    zip_file = "%s.tgz" % unzip_file


    def config(self):
        pass
        
    def source(self):
        self.run("cp /data/software/%s ." % self.zip_file) # or you can download from any where
        untargz(self.zip_file)
        os.unlink(self.zip_file)

    def build(self):
        pass

    def package(self):
        self.copy("*", dst="include", src="%s/include" % self.unzip_file, keep_path=True)
        self.copy("*", dst="lib", src="%s/lib" % self.unzip_file, keep_path=True)

    def package_info(self):
        self.cpp_info.includedirs = ['include/oracle-%s' % self.version]
        self.cpp_info.libs = ["clntsh", "nnz11", "ociei"]

    def conan_info(self):
        pass
