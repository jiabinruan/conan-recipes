from conans import ConanFile, CMake
from conans.tools import download, untargz 

import os, shutil

class MySQLClientConan(ConanFile):
    name = "MySQLClient"
    version = "6.1.6"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/hklabbers/conan-mysqlclient.git" # copy from
    license = "GPL v2"
    author = "Jiabin Ruan (jiabinruan@qq.com)"
    generators = "cmake"
    untar_file = "mysql-connector-c-%s-linux-glibc2.5-x86_64" % version
    tar_file = "%s.tar.gz" % untar_file

    def config(self):
        pass
        
    def source(self):
        self.run("cp /data/software/%s ." % self.tar_file) # or you can download from any where
        untargz(self.tar_file)
        os.unlink(self.tar_file)

    def build(self):
        pass

    def package(self):
        self.copy("*", dst="include", src="%s/include" % self.untar_file, keep_path=True)
        self.copy("*", dst="lib", src="%s/lib" % self.untar_file, keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["mysqlclient"]
        self.cpp_info.libs.extend(["dl", "pthread"])

    def conan_info(self):
        pass
