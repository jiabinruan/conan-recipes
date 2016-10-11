from conans import ConanFile, ConfigureEnvironment
from conans.tools import download, untargz, check_sha1, replace_in_file
import os
import shutil

class LibmongocConan(ConanFile):
    name = "libmongoc"
    version = "1.4.0"
    url = "https://github.com/theirix/conan-libbson"
    license = "https://github.com/mongodb/mongo-c-driver/blob/1.4.0/COPYING"
    FOLDER_NAME = 'mongo-c-driver-%s' % version
    settings = "os", "compiler", "build_type", "arch"
    requires = "libbson/1.4.0@ruanjiabin/stable"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def config_options(self):
        del self.settings.compiler.libcxx

    def source(self):
        tarball_name = self.FOLDER_NAME + '.tar.gz'
        self.run("cp /data/software/%s ." % (tarball_name))
#        download("https://github.com/mongodb/mongo-c-driver/releases/download/%s/%s.tar.gz"
#                 % (self.version, self.FOLDER_NAME), tarball_name)
        untargz(tarball_name)
        os.unlink(tarball_name)
        pass

    def build(self):

        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)

        if self.settings.os == "Linux" or self.settings.os == "Macos":
            
            env_line = env.command_line

            # compose configure options
            suffix = ''
            if self.options.shared:
                suffix += " --enable-shared --disable-static"
            else:
                suffix += " --disable-shared --enable-static"

            # disable rpath build
            old_str = "-install_name \$rpath/"
            new_str = "-install_name "
            replace_in_file("%s/%s/configure" % (self.conanfile_directory, self.FOLDER_NAME), old_str, new_str)

            cmd = 'cd %s/%s && %s ./configure %s' % (self.conanfile_directory, self.FOLDER_NAME, env_line, suffix)
            self.output.warn('Running: ' + cmd)
            self.run(cmd)

            cmd = 'cd %s/%s && %s make' % (self.conanfile_directory, self.FOLDER_NAME, env_line)
            self.output.warn('Running: ' + cmd)
            self.run(cmd)
            
        else:
            self.output.error("unsupported os: %s" (self.settings.os))

    def package(self):
        # exclude private headers
        for header in ['mongoc.h', 'mongoc-apm.h', 'mongoc-apm-private.h', 'mongoc-array-private.h', 'mongoc-async-private.h', 'mongoc-async-cmd-private.h', 'mongoc-b64-private.h', 'mongoc-buffer-private.h', 'mongoc-bulk-operation-private.h', 'mongoc-bulk-operation.h', 'mongoc-client-pool.h', 'mongoc-client-pool-private.h', 'mongoc-client-private.h', 'mongoc-client.h', 'mongoc-cluster-private.h', 'mongoc-collection-private.h', 'mongoc-collection.h', 'mongoc-counters-private.h', 'mongoc-cursor-array-private.h', 'mongoc-cursor-cursorid-private.h', 'mongoc-cursor-transform-private.h', 'mongoc-cursor-private.h', 'mongoc-cursor.h', 'mongoc-crypto-private.h', 'mongoc-database-private.h', 'mongoc-database.h', 'mongoc-errno-private.h', 'mongoc-error.h', 'mongoc-find-and-modify-private.h', 'mongoc-find-and-modify.h', 'mongoc-flags.h', 'mongoc-gridfs-file-list-private.h', 'mongoc-gridfs-file-list.h', 'mongoc-gridfs-file-page-private.h', 'mongoc-gridfs-file-page.h', 'mongoc-gridfs-file-private.h', 'mongoc-gridfs-file.h', 'mongoc-gridfs-private.h', 'mongoc-gridfs.h', 'mongoc-host-list-private.h', 'mongoc-host-list.h', 'mongoc-index.h', 'mongoc-init.h', 'mongoc-iovec.h', 'mongoc-list-private.h', 'mongoc-log.h', 'mongoc-log-private.h', 'mongoc-matcher-op-private.h', 'mongoc-matcher-private.h', 'mongoc-matcher.h', 'mongoc-memcmp-private.h', 'mongoc-opcode.h', 'mongoc-opcode-private.h', 'mongoc-queue-private.h', 'mongoc-read-concern-private.h', 'mongoc-read-concern.h', 'mongoc-read-prefs-private.h', 'mongoc-read-prefs.h', 'mongoc-rpc-private.h', 'mongoc-sasl-private.h', 'mongoc-scram-private.h', 'mongoc-server-description.h', 'mongoc-server-description-private.h', 'mongoc-server-stream-private.h', 'mongoc-set-private.h', 'mongoc-socket.h', 'mongoc-socket-private.h', 'mongoc-stream-buffered.h', 'mongoc-stream-file.h', 'mongoc-stream-gridfs.h', 'mongoc-stream-private.h', 'mongoc-stream-socket.h', 'mongoc-stream.h', 'mongoc-thread-private.h', 'mongoc-topology-description-private.h', 'mongoc-topology-private.h', 'mongoc-topology-scanner-private.h', 'mongoc-trace.h', 'mongoc-trace-private.h', 'mongoc-uri.h', 'mongoc-uri-private.h', 'mongoc-util-private.h', 'mongoc-version.h', 'mongoc-version-functions.h', 'mongoc-write-command-private.h', 'mongoc-write-concern-private.h', 'mongoc-write-concern.h', 'utlist.h', 'mongoc-crypto-cng-private.h', 'mongoc-crypto-common-crypto-private.h', 'mongoc-crypto-openssl-private.h', 'mongoc-openssl-private.h', 'mongoc-rand.h', 'mongoc-rand-private.h', 'mongoc-secure-channel-private.h', 'mongoc-secure-transport-private.h', 'mongoc-ssl.h', 'mongoc-ssl-private.h', 'mongoc-stream-tls.h', 'mongoc-stream-tls-openssl-bio-private.h', 'mongoc-stream-tls-openssl.h', 'mongoc-stream-tls-openssl-private.h', 'mongoc-stream-tls-private.h', 'mongoc-stream-tls-secure-channel.h', 'mongoc-stream-tls-secure-channel-private.h', 'mongoc-stream-tls-secure-transport.h', 'mongoc-stream-tls-secure-transport-private.h', 'op-delete.def', 'op-get-more.def', 'op-header.def', 'op-insert.def', 'op-kill-cursors.def', 'op-msg.def', 'op-query.def', 'op-reply.def', 'op-reply-header.def', 'op-update.def', 'mongoc-counters.defs', 'mongoc-config.h']:
            self.copy(header, dst="include/libmongoc-1.0", src="%s/src/mongoc" % (self.FOLDER_NAME), keep_path=False)
        
        if self.settings.os == "Macos":
            self.copy(pattern="*.dylib", dst="lib", src="%s/.libs" % (self.FOLDER_NAME), keep_path=False)
        else:
            self.copy(pattern="*.so*", dst="lib", src="%s/.libs" % (self.FOLDER_NAME), keep_path=False)
            
        self.copy(pattern="*mongoc*.a", dst="lib", src="%s/.libs" % (self.FOLDER_NAME), keep_path=False)
        self.copy(pattern="*mongoc*.la", dst="lib", src="%s/.libs" % (self.FOLDER_NAME), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['mongoc-1.0']
        self.cpp_info.includedirs = ['include/libmongoc-1.0']
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["pthread", "rt", "ssl", "crypto"])
