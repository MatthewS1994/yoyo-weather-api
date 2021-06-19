import re
import unicodedata

from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.text import slugify as django_slugify

SLUGIFY_RE = re.compile(r"[^\w\s-]", re.UNICODE)


def cautious_slugify(value):
    """
    Convert a string to ASCII exactly as Django's slugify does, with the exception
    that any non-ASCII alphanumeric characters (that cannot be ASCIIfied under Unicode
    normalisation) are escaped into codes like 'u0421' instead of being deleted entirely.
    This ensures that the result of slugifying e.g. Cyrillic text will not be an empty
    string, and can thus be safely used as an identifier (albeit not a human-readable one).

    cautious_slugify was copied from Wagtail:
    <https://github.com/wagtail/wagtail/blob/8b420b9/wagtail/core/utils.py>

    Copyright (c) 2014-present Torchbox Ltd and individual contributors.
    Released under the BSD 3-clause "New" or "Revised" License
    <https://github.com/wagtail/wagtail/blob/8b420b9/LICENSE>

    Date: 2018-06-15
    """
    # Normalize the string to decomposed unicode form. This causes accented Latin
    # characters to be split into 'base character' + 'accent modifier'; the latter will
    # be stripped out by the regexp, resulting in an ASCII-clean character that doesn't
    # need to be escaped
    value = unicodedata.normalize("NFKD", value)

    # Strip out characters that aren't letterlike, underscores or hyphens,
    # using the same regexp that slugify uses. This ensures that non-ASCII non-letters
    # (e.g. accent modifiers, fancy punctuation) get stripped rather than escaped
    value = SLUGIFY_RE.sub("", value)

    # Encode as ASCII, escaping non-ASCII characters with backslashreplace, then convert
    # back to a unicode string (which is what slugify expects)
    value = value.encode("ascii", "backslashreplace").decode("ascii")

    # Pass to slugify to perform final conversion (whitespace stripping); this will
    # also strip out the backslashes from the 'backslashreplace' conversion
    return django_slugify(value)


def default_slugifier(value, allow_unicode=False):
    """
    default slugifier function. When unicode is allowed
    it uses Django's slugify function, otherwise it uses cautious_slugify.
    """
    if allow_unicode:
        return django_slugify(value, allow_unicode=True)
    else:
        return cautious_slugify(value)


def slugify(value):
    """
    Slugify a string

    The DJANGO_SLUG_FUNCTION can be set with a dotted path to the slug
    function to use, defaults to 'common.utils.utils.default_slugifier'.

    DJANGO_SLUG_MAP can be set of a dictionary of target:replacement pairs

    DJANGO_SLUG_BLACKLIST can be set to a iterable of words to remove after
    the slug is generated; though it will not reduce a slug to zero length.
    """
    value = str(value)

    # Re-map some strings to avoid important characters being stripped.  Eg
    # remap 'c++' to 'cpp' otherwise it will become 'c'.
    for k, v in settings.DJANGO_SLUG_MAP.items():
        value = value.replace(k, v)

    slugifier = import_string(settings.DJANGO_SLUG_FUNCTION)
    slug = slugifier(value, allow_unicode=settings.DJANGO_SLUG_ALLOW_UNICODE)

    # Remove stopwords from slug
    for word in settings.DJANGO_SLUG_BLACKLIST:
        slug = slug.replace(word + "-", "")
        slug = slug.replace("-" + word, "")

    return slug
