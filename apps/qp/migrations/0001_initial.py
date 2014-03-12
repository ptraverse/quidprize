# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Business'
        db.create_table('qp_business', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('auth_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='64')),
            ('logo', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('contact_person', self.gf('django.db.models.fields.CharField')(max_length='64')),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length='12')),
            ('address', self.gf('django.db.models.fields.CharField')(max_length='64')),
        ))
        db.send_create_signal('qp', ['Business'])

        # Adding model 'Document'
        db.create_table('qp_document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('qp', ['Document'])

        # Adding model 'Raffle'
        db.create_table('qp_raffle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qp.Business'])),
            ('target_url', self.gf('django.db.models.fields.CharField')(max_length='64')),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('draw_winner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('draw_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('qp', ['Raffle'])

        # Adding model 'Ticket'
        db.create_table('qp_ticket', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activation_email', self.gf('django.db.models.fields.CharField')(default=None, max_length='75', null=True)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length='16')),
            ('raffle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qp.Raffle'])),
            ('date_activated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('parent_ticket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qp.Ticket'], null=True, blank=True)),
        ))
        db.send_create_signal('qp', ['Ticket'])


    def backwards(self, orm):
        # Deleting model 'Business'
        db.delete_table('qp_business')

        # Deleting model 'Document'
        db.delete_table('qp_document')

        # Deleting model 'Raffle'
        db.delete_table('qp_raffle')

        # Deleting model 'Ticket'
        db.delete_table('qp_ticket')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'qp.business': {
            'Meta': {'object_name': 'Business'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': "'64'"}),
            'auth_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': "'64'"}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': "'12'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'64'"})
        },
        'qp.document': {
            'Meta': {'object_name': 'Document'},
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'qp.raffle': {
            'Meta': {'object_name': 'Raffle'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qp.Business']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'draw_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'draw_winner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target_url': ('django.db.models.fields.CharField', [], {'max_length': "'64'"})
        },
        'qp.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'activation_email': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': "'75'", 'null': 'True'}),
            'date_activated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': "'16'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qp.Ticket']", 'null': 'True', 'blank': 'True'}),
            'raffle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qp.Raffle']"})
        }
    }

    complete_apps = ['qp']