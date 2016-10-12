from conans import ConanFile, CMake, tools
from conans.tools import unzip
import os


class MysqlconnectorcppConan(ConanFile):
    name = "mysql-connector-cpp"
    version = "1.1.5"
    license = "GPL 2"
    url = ""
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    unzip_name = '%s-%s' % (name, version)
    zip_name = '%s.zip' % unzip_name
    requires = "MySQLClient/6.1.6@ruanjiabin/stable"

    def source(self):
        self.run("cp /data/software/%s ." % self.zip_name)
        unzip(self.zip_name)

    def build(self):
        self.run("cd %s && mkdir -p build && cmake -DCMAKE_INSTALL_PREFIX=./build && make && make install" % self.unzip_name)

    def package(self):
        # Copying headers
        self.copy(pattern="*.h", dst="include/", src="%s/build/include" %(self.unzip_name), keep_path=True)

        # Copying static and dynamic libs
        self.copy(pattern="*.a", dst="lib", src="%s/build/lib" %(self.unzip_name), keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="%s/build/lib" %(self.unzip_name), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["mysqlcppconn"]
