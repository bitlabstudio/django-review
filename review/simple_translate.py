"""Translations for the ``review`` app."""
from simple_translation.translation_pool import translation_pool

from . import models


translation_pool.register_translation(models.RatingCategory,
                                      models.RatingCategoryTranslation)
