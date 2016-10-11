from conans import ConanFile, CMake, tools, ConfigureEnvironment
import os
import shutil


class ProtobufConan(ConanFile):
    name = "Protobuf"
    version = "2.6.1"
    url = "https://github.com/memsharded/conan-protobuf.git"
    license = "https://github.com/google/protobuf/blob/v2.6.1/LICENSE"
    requires = "zlib/1.2.8@lasote/stable"
    settings = "os", "compiler", "build_type", "arch"
    exports = "CMakeLists.txt", "lib*.cmake", "extract_includes.bat.in", "protoc.cmake", "tests.cmake", "change_dylib_names.sh"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    tarbz_name = "protobuf-%s.tar.bz2" % version

    def config(self):
        self.options["zlib"].shared = self.options.shared

    def source(self):
        # you can download from the url, but it may be too slow
        # url = "https://github.com/redis/hiredis/archive/%s" % self.tarbz_name
        # tools.download("https://github.com/google/protobuf/"
        #               "releases/download/v2.6.1/protobuf-2.6.1.zip",
        #               "protobuf.zip")
        # you can also copy from local path, but make sure the zip file is there
        self.run("cp /data/software/%s ." % self.tarbz_name)
        self.run("tar -xjf %s" % self.tarbz_name)
        os.makedirs("protobuf-2.6.1/cmake")

    def build(self):
        if self.settings.os == "Windows":
            args = ['-DBUILD_TESTING=OFF']
            args += ['-DBUILD_SHARED_LIBS=%s' % ('ON' if self.options.shared else 'OFF')]
            cmake = CMake(self.settings)
            self.run('cd protobuf-2.6.1/cmake && cmake . %s %s' % (cmake.command_line, ' '.join(args)))
            self.run("cd protobuf-2.6.1/cmake && cmake --build . %s" % cmake.build_config)
        else:
            env = ConfigureEnvironment(self.deps_cpp_info, self.settings)

            concurrency = 1
            try:
                import multiprocessing
                concurrency = multiprocessing.cpu_count()
            except (ImportError, NotImplementedError):
                pass

            self.run("chmod +x protobuf-2.6.1/autogen.sh")
            self.run("chmod +x protobuf-2.6.1/configure")
            self.run("cd protobuf-2.6.1 && ./autogen.sh")

            args = []
            if not self.options.shared:
                args += ['--disable-shared']

            self.run("cd protobuf-2.6.1 && %s ./configure %s" % (env.command_line, ' '.join(args)))
            self.run("cd protobuf-2.6.1 && make -j %s" % concurrency)

    def package(self):
        self.copy_headers("*.h", "protobuf-2.6.1/src")

        if self.settings.os == "Windows":
            self.copy("*.lib", "lib", "protobuf-2.6.1/cmake", keep_path=False)
            self.copy("protoc.exe", "bin", "protobuf-2.6.1/cmake/bin", keep_path=False)

            if self.options.shared:
                self.copy("*.dll", "bin", "protobuf-2.6.1/cmake/bin", keep_path=False)
        else:
            # Copy the libs to lib
            if not self.options.shared:
                self.copy("*.a", "lib", "protobuf-2.6.1/src/.libs", keep_path=False)
            else:
#                 self.run("cp -P protobuf-2.6.1/src/.libs/*.so* lib")
                self.copy("*.so*", "lib", "protobuf-2.6.1/src/.libs", keep_path=False)
                self.copy("*.9.dylib", "lib", "protobuf-2.6.1/src/.libs", keep_path=False)

            # Copy the exe to bin
            if self.settings.os == "Macos":
                if not self.options.shared:
                    self.copy("protoc", "bin", "protobuf-2.6.1/src/", keep_path=False)
                else:
                    # "protoc" has libproto*.dylib dependencies with absolute file paths.
                    # Change them to be relative.
                    self.run("cd protobuf-2.6.1/src/.libs && bash ../../cmake/change_dylib_names.sh")

                    # "src/protoc" may be a wrapper shell script which execute "src/.libs/protoc".
                    # Copy "src/.libs/protoc" instead of "src/protoc"
                    self.copy("protoc", "bin", "protobuf-2.6.1/src/.libs/", keep_path=False)
                    self.copy("*.9.dylib", "bin", "protobuf-2.6.1/src/.libs", keep_path=False)
            else:
                self.copy("protoc", "bin", "protobuf-2.6.1/src/", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["libprotobuf"]
            if self.options.shared:
                self.cpp_info.defines = ["PROTOBUF_USE_DLLS"]
        elif self.settings.os == "Macos":
            self.cpp_info.libs = ["libprotobuf.a"] if not self.options.shared else ["libprotobuf.9.dylib"]
        else:
            self.cpp_info.libs = ["libprotobuf.a"] if not self.options.shared else ["libprotobuf.so.9"]
