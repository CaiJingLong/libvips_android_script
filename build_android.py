#!/usr/bin/env python3

import datetime
import json
import os
from os.path import join
import shutil

script_dir = os.path.dirname(os.path.realpath(__file__))

print("Building Android...")
print('The script is located at: ' + script_dir)

deploy_name = "custom_deploy.py"

deploy_path = join(script_dir, deploy_name)

android_type_list = [
    'android-arm64-v8a',
    'android-armv7',
    'android-x86',
    'android-x86_64',
]

type_map = {
    'android-arm64-v8a': 'armv8',
    'android-armv7': 'armv7',
    'android-x86': 'x86',
    'android-x86_64': 'x86_64',
}

jni_folder_map = {
    'android-arm64-v8a': 'arm64-v8a',
    'android-armv7': 'armeabi-v7a',
    'android-x86': 'x86',
    'android-x86_64': 'x86_64',
}


def get_release_folder(type: str) -> str:
    return join(script_dir, 'output', 'Release', 'Android', type_map[type])


def get_jniLibs_path(type: str) -> str:
    return join(script_dir, 'output', 'android', 'jniLibs', jni_folder_map[type])


class Config:
    def __init__(self) -> None:
        with open(join(script_dir, 'config.json'), 'r') as f:
            params = json.load(f)
        self.build_type = params.get('build_type', 'missing')
        self.save()
        pass

    def change_build_missing(self):
        self.build_type = 'missing'
        self.save()
        pass

    def change_build_all(self):
        self.build_type = '*'
        self.save()
        pass

    def save(self):
        with open(join(script_dir, 'config.json'), 'w') as f:
            json.dump(self.__dict__, f, indent=4)
        pass


config = Config()


def make_command(type: str) -> str:
    options = [
        "*:shared=True",
        "libelf/*:shared=False",
        "libgettext/*:shared=False",
    ]

    cross_file_path = join(script_dir, 'cross', '%s.ini' % type)
    output_path = join(script_dir, 'output')

    cmd_list = [
        'conan',
        'install',
        '.',
    ]

    cmd_list.append('--build="%s"' % config.build_type)

    cmd_list.append('-of %s' % output_path)

    for option in options:
        cmd_list.append('-o')
        cmd_list.append('"%s"' % option)

    cmd_list.append('--profile:host %s' % cross_file_path)
    cmd_list.append('-d %s' % deploy_path)
    cmd_list.append('-v')

    return ' '.join(cmd_list)


def copy_android_jni(src: str, dest: str):
    if not os.path.exists(src):
        print('Warning: %s not exists' % src)
        return

    if not os.path.exists(dest):
        os.makedirs(dest)

    # just copy src/lib/* to dest
    src_libs = join(src, 'lib')
    print('Copying %s to %s' % (src_libs, dest))
    for file in os.listdir(src_libs):
        if file.endswith('.a') or file.endswith('.so'):
            shutil.copy(join(src_libs, file), dest)
            print('  %s' % file)


def make_jni_style_folder():
    output_path = join(script_dir, 'output')
    android_path = join(output_path, 'android', 'jniLibs')
    if not os.path.exists(android_path):
        os.makedirs(android_path)

    for android_type in android_type_list:
        build_release_path = get_release_folder(android_type)
        jni_path = get_jniLibs_path(android_type)
        copy_android_jni(build_release_path, jni_path)

    # copy headers
    header_src_path = join(get_release_folder(android_type_list[0]), 'include')
    dest_header_path = join(android_path, 'include')
    if os.path.exists(dest_header_path):
        shutil.rmtree(dest_header_path)

    shutil.copytree(header_src_path, join(android_path, 'include'))

    print('Done!\n')
    print('The jniLibs folder is located at: %s' % android_path)


def main_menu():
    while True:

        print('Choose the build type:')
        for i in range(len(android_type_list)):
            print(f'  {i+1}. {android_type_list[i]}')

        print('  c. Change config')
        print('  m. Make `jniLibs` folder with android style')
        print('  q. Quit')

        choice = input('Your choice: ')

        if choice == 'q':
            print('Bye!')
            exit(0)

        if choice == 'c':
            change_config_menu()
            continue

        if choice == 'm':
            make_jni_style_folder()
            continue

        try:
            choice = int(choice)
        except ValueError:
            print('Invalid input!')
            continue

        if choice < 1 or choice > len(android_type_list):
            print('Invalid input!')
            continue

        type = android_type_list[choice - 1]
        cmd = make_command(type)
        print('Running: %s' % cmd)
        os.system(cmd)

        # make a logs
        log_dir = join(script_dir, 'logs')
        if not os.path.exists(log_dir):
            os.system('mkdir -p %s' % log_dir)

        dt = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = join(log_dir, '%s_%s.log' % (type, dt))
        open(log_file, 'w').write(cmd)


def change_config_menu():
    while True:
        print('Choose the option:')
        print('  1. Build with "*"')
        print('  2. Build with "missing"')
        print('  q. Quit')

        choice = input('Your choice: ')

        if choice == 'q':
            main_menu()
            return

        try:
            choice = int(choice)
        except ValueError:
            print('Invalid input!')
            continue

        if choice == 1:
            config.change_build_all()
            print('Changed to build with "*"')
            continue

        if choice == 2:
            config.change_build_missing()
            print('Changed to build with "missing"')
            continue


main_menu()
