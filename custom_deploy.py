import json
import os
from conans.model.conanfile_interface import ConanFileInterface


def copy_with_cmd(cmd: str):
    print('copy_with_cmd: %s' % cmd)
    os.system(cmd)


# def deploy(graph, output_folder):
#     conanfile = graph.root.conanfile
#     conanfile.output.info(f"Conan built-in full deployer to {output_folder}")
#     for dep in conanfile.dependencies.values():
#         dep: ConanFileInterface
#         print('%s dep.folders: '% (dep))
#         if dep.package_folder is None:
#             continue
#         folder_name = output_folder
#         build_type = dep.info.settings.get_safe("build_type")
#         arch = dep.info.settings.get_safe("arch")
#         if build_type:
#             folder_name = os.path.join(folder_name, build_type)
#         if arch:
#             folder_name = os.path.join(folder_name, arch)
#         copy_with_cmd('mkdir -p %s' % folder_name)
#         copy_with_cmd('cp -r %s/* %s' % (dep.package_folder, folder_name))

#     print('Installed to the %s' % folder_name)

def deploy(graph, output_folder):
    conanfile = graph.root.conanfile
    conanfile.output.info(f"Conan all libraries full deployer to {output_folder}")
    for dep in conanfile.dependencies.values():
        dep: ConanFileInterface
        # print(str(dep))
        # print('%s %s: ' % (str(dep), str(dep.package_path)))
        if dep.package_folder is None:
            continue
        folder_name = output_folder
        build_type = dep.info.settings.get_safe("build_type")
        arch = dep.info.settings.get_safe("arch")
        if build_type:
            folder_name = os.path.join(folder_name, build_type)
        if arch:
            folder_name = os.path.join(folder_name, arch)
        copy_with_cmd('mkdir -p %s' % folder_name)
        copy_with_cmd('cp -r %s/* %s' % (dep.package_folder, folder_name))

    # print('Installed to the %s' % folder_name)
