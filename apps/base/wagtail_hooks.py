from wagtail import hooks
from wagtail.search.backends.database.postgres.postgres import (
    PostgresSearchQueryCompiler,
)


# fix split search
PostgresSearchQueryCompiler.LAST_TERM_IS_PREFIX = True


@hooks.register("insert_global_admin_js", order=-1)
def global_admin_js():
    """global admin javascript"""

    return """
        <script>
            window.addEventListener("DOMContentLoaded", function () {
              // fix wagtail's URLify
              // https://github.com/wagtail/wagtail/blob/2b061ac96e5ffdad2759e39bfdbca0fc242ae854/client/src/utils/urlify.ts#L13
              window.URLify = function() {return;};
            });
        </script>
    """


@hooks.register("register_rich_text_features", order=10)
def register_rich_text_features(features):
    default_features = features.default_features

    if "h1" not in default_features and "h2" in default_features:
        default_features.insert(default_features.index("h2"), "h1")

    if "h5" not in default_features and "h4" in default_features:
        default_features.insert(default_features.index("h4") + 1, "h5")

    if "h6" not in default_features and "h5" in default_features:
        default_features.insert(default_features.index("h5") + 1, "h6")

    extends = ["superscript", "subscript", "strikethrough", "code", "blockquote"]
    for tag in extends:
        if tag not in default_features:
            default_features.append(tag)
