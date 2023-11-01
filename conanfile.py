import os

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.meson.toolchain import MesonToolchain
from conan.tools.scm import Git
from conan.tools.build import check_min_cppstd


class DepLibVips(ConanFile):
    name = "hello"
    version = "1.0"

    def requirements(self):
        # self.build_requires('make/4.4')
        # self.requires('libiconv/1.17')
        self.requires('libgettext/0.22')
        # self.requires('pcre2/10.42')
        self.requires('glib/2.78.0')
        self.requires('libvips/8.14.2')
        # self.requires('libtiff/4.6.0')
        # self.requires("libiconv/1.17")
        # self.requires('giflib/5.2.1')
        # self.requires('ffmpeg/5.1')
