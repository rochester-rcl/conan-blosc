from conans import CMake, ConanFile
from conans.tools import replace_in_file


# Based on https://raw.githubusercontent.com/karasusan/conan-blosc/master/conanfile.py


class BloscConan(ConanFile):
    description = "A blocking, shuffling and lossless compression library"
    name = "Blosc"
    version = "1.5.0"
    license = "BSD"
    requires = ("zlib/1.2.8@conan/stable", )
    url = "https://github.com/karasusan/conan-blosc"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]
        , "fPIC": [True, False]
               }
    default_options = "shared=False", "fPIC=True"
    exports = ["FindBlosc.cmake"]

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        if self.options.shared and "fPIC" in self.options.fields:
            self.options.fPIC = True

    def source(self):
        self.run("git clone https://github.com/Blosc/c-blosc blosc")
        self.run("cd blosc && git checkout v{}".format(self.version))
        replace_in_file("blosc/CMakeLists.txt", "project(blosc)",
                        "project(blosc)\ninclude(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\nconan_basic_setup()")

    def build(self):
        cmake = CMake(self)
        cmake.definitions.update(
            {"BUILD_SHARED": self.options.shared
                , "BUILD_STATIC": not self.options.shared
                , "BUILD_TESTS": False
                , "BUILD_BENCHMARKS": False
                , "PREFER_EXTERNAL_LZ4": False
                , "PREFER_EXTERNAL_SNAPPY": False
                , "PREFER_EXTERNAL_ZLIB": False
                , "PREFER_EXTERNAL_ZSTD": False
                , "CMAKE_INSTALL_PREFIX": self.package_folder
             })
        if "fPIC" in self.options.fields:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC

        cmake.configure(source_dir="{}/blosc".format(self.source_folder))
        cmake.build(target="install")

    def package(self):
        self.copy("FindBlosc.cmake", ".", ".")
        self.copy("*.txt", src="src/LICENSES", dst="licenses")

        self.copy("*.lib", dst="lib", src="lib", keep_path=False)
        self.copy("*.a", dst="lib", src="lib", keep_path=False)
        self.copy("*.so", dst="lib", src="lib", keep_path=False)
        self.copy("*.so.*", dst="lib", src="lib", keep_path=False)
        self.copy("*.dylib*", dst="lib", src="lib", keep_path=False)
        self.copy("*blosc*.h", dst="include", src="{}/blosc/blosc".format(self.source_folder), keep_path=False)

    def package_info(self):
        prefix = "lib" if self.settings.os == "Windows" and not self.options.shared else ""
        self.cpp_info.libs.append(prefix + "blosc")
        if self.settings.os == "Windows" and self.options.shared:
            self.cpp_info.defines.append("BLOSC_SHARED_LIBRARY")
        if not self.options.shared and self.settings.os != "Windows":
            self.cpp_info.libs.extend(["pthread"])
