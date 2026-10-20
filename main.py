"""
Basic example of a Mkdocs-macros module
"""

import math
import yaml
import os
import csv
import json

def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    - filter: a function with one of more arguments,
        used to perform a transformation
    """

    @env.macro
    def get_table_headers():
        print(env.project_dir)
        d = env.project_dir+"/docs/GEMIBRA_2580_V2_07_Apr_2026.csv"
        # d = env.project_dir+"/docs/test.csv"
        reader = csv.DictReader(open(d))
        headers = reader.fieldnames
        print(headers)
        return headers

    @env.macro
    def get_table_rows():
        d = env.project_dir+"/docs/GEMIBRA_2580_V2_07_Apr_2026.csv"
        print(d)
        # d = env.project_dir+"/docs/test.csv"
        data = []
        for i,row in enumerate(csv.reader(open(d))):
            if i==0:
                continue
            data.append(row)

        
        return json.dumps(data)

    try:
        from copy import deepcopy
        from pathlib import PurePath
        from mkdocs_static_i18n import folder, is_relative_to
        from mkdocs_static_i18n.reconfigure import ExtendedPlugin

        if not getattr(folder.create_i18n_file, "_gemibra_patched", False):
            _orig_create_i18n_file = folder.create_i18n_file

            def _create_i18n_file(file, current_language, default_language, all_languages, config):
                i18n_file = _orig_create_i18n_file(
                    file, current_language, default_language, all_languages, config
                )
                if (
                    current_language == default_language
                    and i18n_file.localization == default_language
                    and not is_relative_to(i18n_file.dest_path, current_language)
                ):
                    i18n_file.dest_path = PurePath(
                        PurePath(current_language) / PurePath(i18n_file.dest_path)
                    ).as_posix()
                    i18n_file.abs_dest_path = os.path.normpath(
                        os.path.join(config.site_dir, i18n_file.dest_path)
                    )
                    i18n_file.url = i18n_file._get_url(config.use_directory_urls)
                return i18n_file

            _create_i18n_file._gemibra_patched = True
            folder.create_i18n_file = _create_i18n_file

        if not getattr(ExtendedPlugin.reconfigure_page_context, "_gemibra_patched", False):
            def _reconfigure_page_context(self, context, page, config, nav):
                if self.extra_alternate:
                    config.extra.alternate = deepcopy(self.extra_alternate)
                    for extra_alternate in config.extra.alternate:
                        alternate_lang = extra_alternate["lang"]
                        if alternate_lang in page.file.alternates:
                            alternate_file = page.file.alternates[alternate_lang]
                            extra_alternate["link"] = alternate_file.url
                return context

            _reconfigure_page_context._gemibra_patched = True
            ExtendedPlugin.reconfigure_page_context = _reconfigure_page_context
    except ImportError:
        pass


def on_post_build(env):
    site_dir = env.conf["site_dir"]
    root_index = os.path.join(site_dir, "index.html")
    with open(root_index, "w", encoding="utf-8") as f:
        f.write(
            '<!DOCTYPE html>\n'
            '<html lang="pt">\n'
            '<head>\n'
            '  <meta charset="utf-8">\n'
            '  <title>GEMIBRA</title>\n'
            '  <link rel="canonical" href="pt/">\n'
            '  <meta http-equiv="refresh" content="0; url=pt/">\n'
            '  <script>window.location.replace("pt/" + window.location.search + window.location.hash);</script>\n'
            '</head>\n'
            '<body>\n'
            '  <p>Redirecionando para <a href="pt/">Português</a>...</p>\n'
            '</body>\n'
            '</html>\n'
        )
