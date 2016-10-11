from conans import ConanFile
import os
from conans.tools import download
from conans.tools import unzip
from conans import CMake

class HiredisConan(ConanFile):
    name = "hiredis"
    version = "0.13.3"
    ZIP_FOLDER_NAME = "hiredis-%s" % version
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    url="https://github.com/dwerner/conan-hiredis"
    license="https://github.com/google/googletest/blob/master/googletest/LICENSE"
    exports="FindHiredis.cmake", "change_dylib_names.sh"
    zip_name = "hiredis-%s.zip" % version
    unzipped_name = "hiredis-%s" % version

    def source(self):
        # you can download from the url, but it may be too slow
        # url = "https://github.com/redis/hiredis/archive/%s" % self.zip_name
        # download(url, self.zip_name)
        # you can also copy from local path, but make sure the zip file is there
        self.run("cp /data/software/%s ." % self.zip_name)
        unzip(self.zip_name)
        os.unlink(self.zip_name)

    def build(self):
        cd_build = "cd %s" % self.unzipped_name
        self.run("%s && make && mkdir -p build && PREFIX=./build make install" % cd_build)

    def package(self):

        if self.settings.os == "Macos" and self.options.shared:
            self.run("bash ./change_dylib_names.sh")

        # Copy findHiredis script into project
        self.copy("FindHiredis.cmake", ".", ".")

        # Copying headers
        self.copy(pattern="*.h", dst="include/", src="%s/build/include" %(self.unzipped_name), keep_path=True)

        # Copying static and dynamic libs
        self.copy(pattern="*.a", dst="lib", src="%s/build/lib" %(self.unzipped_name), keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="%s/build/lib" %(self.unzipped_name), keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src="%s/build/lib" %(self.unzipped_name), keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="%s/build/lib" %(self.unzipped_name), keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src="%s/build/lib" %(self.unzipped_name), keep_path=False)      

    def package_info(self):
        self.cpp_info.libs = ['hiredis']
