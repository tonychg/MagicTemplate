# coding: utf-8
import os
import neovim
import subprocess

ignored_directories = (
    ".git",
    ".gitignore",
    ".gitmodules",
    "_templates",
)

ENCODING = "utf8"
TEMPLATE_EXTENSION = ".gitlab-ci.yml"
FZF_EXECUTABLE = "/usr/bin/fzf"


def abs_path_to_display_name(abs_path, source_dir):
    return abs_path[len(source_dir) + 1 : -len(TEMPLATE_EXTENSION)]


def search_templates(source_dir):
    templates = {}

    for root, _, files in os.walk(source_dir):
        for filename in files:
            if filename.endswith(TEMPLATE_EXTENSION):
                abs_path = os.path.join(root, filename)
                display_name = abs_path_to_display_name(abs_path, source_dir)
                templates[display_name] = abs_path
    return templates


def select_template(templates):
    fzf_input = "\n".join(templates.keys())

    fzf = subprocess.Popen(
        FZF_EXECUTABLE, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    output = fzf.communicate(input=fzf_input.encode(ENCODING))
    selected_template = output[0].decode(ENCODING).strip()
    return templates.get(selected_template, "")


class Template:
    def __init__(self, template_directory):
        self.template_directory = str(os.path.expanduser(template_directory))

    def search(self, buffer_filename, filetype=None):
        for filename in os.listdir(self.template_directory):
            fullpath = os.path.join(self.template_directory, filename)

            if filename not in ignored_directories and filename in (
                filetype,
                buffer_filename,
            ):
                if os.path.isfile(fullpath):
                    yield fullpath
                elif os.path.isdir(fullpath):
                    for root, _, files in os.walk(fullpath):
                        for file in files:
                            yield os.path.join(root, file)


@neovim.plugin
class Main(object):
    def __init__(self, vim):
        self.vim = vim

    def get_template_directory(self):
        return self.vim.eval("g:templatesDirectory")

    def get_filetype(self):
        return self.vim.eval("&filetype")

    def get_filename(self):
        return self.vim.eval("%:t")

    @neovim.function("PythonWriteTemplate")
    def write_template(self, args):
        templates = search_templates(self.get_template_directory())
        template_selected = select_template(templates)
