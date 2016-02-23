# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from ..compat import USER_MODEL


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RatingCategoryChoiceTranslation'
        db.create_table(u'review_ratingcategorychoice_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['review.RatingCategoryChoice'])),
        ))
        db.send_create_signal(u'review', ['RatingCategoryChoiceTranslation'])

        # Adding unique constraint on 'RatingCategoryChoiceTranslation', fields ['language_code', 'master']
        db.create_unique(u'review_ratingcategorychoice_translation', ['language_code', 'master_id'])

        # Adding model 'RatingCategoryChoice'
        db.create_table(u'review_ratingcategorychoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ratingcategory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['review.RatingCategory'])),
            ('value', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'review', ['RatingCategoryChoice'])

        # Adding field 'RatingCategory.counts_for_average'
        db.add_column(u'review_ratingcategory', 'counts_for_average',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'RatingCategoryChoiceTranslation', fields ['language_code', 'master']
        db.delete_unique(u'review_ratingcategorychoice_translation', ['language_code', 'master_id'])

        # Deleting model 'RatingCategoryChoiceTranslation'
        db.delete_table(u'review_ratingcategorychoice_translation')

        # Deleting model 'RatingCategoryChoice'
        db.delete_table(u'review_ratingcategorychoice')

        # Deleting field 'RatingCategory.counts_for_average'
        db.delete_column(u'review_ratingcategory', 'counts_for_average')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        USER_MODEL['model_label']: {
            'Meta': {'object_name': USER_MODEL['object_name']},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'generic_positions.objectposition': {
            'Meta': {'object_name': 'ObjectPosition'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'review.rating': {
            'Meta': {'ordering': "['category', 'review']", 'object_name': 'Rating'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['review.RatingCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'review': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'to': u"orm['review.Review']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'review.ratingcategory': {
            'Meta': {'object_name': 'RatingCategory'},
            'counts_for_average': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'blank': 'True'})
        },
        u'review.ratingcategorychoice': {
            'Meta': {'object_name': 'RatingCategoryChoice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ratingcategory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['review.RatingCategory']"}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'review.ratingcategorychoicetranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'RatingCategoryChoiceTranslation', 'db_table': "u'review_ratingcategorychoice_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['review.RatingCategoryChoice']"})
        },
        u'review.ratingcategorytranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'RatingCategoryTranslation', 'db_table': "u'review_ratingcategory_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['review.RatingCategory']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'review.review': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'Review'},
            'average_rating': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'content': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'extra_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'reviews_attached'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'extra_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s']" % USER_MODEL['orm_label'], 'null': 'True', 'blank': 'True'})
        },
        u'review.reviewextrainfo': {
            'Meta': {'ordering': "['type']", 'object_name': 'ReviewExtraInfo'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'review': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['review.Review']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'user_media.usermediaimage': {
            'Meta': {'object_name': 'UserMediaImage'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumb_h': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumb_w': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumb_x': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumb_x2': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumb_y': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumb_y2': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s']" % USER_MODEL['orm_label']})
        }
    }

    complete_apps = ['review']
