# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-11 01:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HookCatcher', '0027_auto_20170711_0100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commit',
            old_name='gitBranch',
            new_name='git_branch',
        ),
        migrations.RenameField(
            model_name='commit',
            old_name='gitHash',
            new_name='git_hash',
        ),
        migrations.RenameField(
            model_name='commit',
            old_name='gitRepo',
            new_name='git_repo',
        ),
        migrations.RenameField(
            model_name='diff',
            old_name='diffPercent',
            new_name='diff_percent',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='browserType',
            new_name='browser_type',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='operatingSystem',
            new_name='operating_system',
        ),
        migrations.RenameField(
            model_name='pr',
            old_name='gitPRNumber',
            new_name='git_pr_number',
        ),
        migrations.RenameField(
            model_name='pr',
            old_name='gitRepo',
            new_name='git_repo',
        ),
        migrations.RenameField(
            model_name='state',
            old_name='gitCommit',
            new_name='git_commit',
        ),
        migrations.RenameField(
            model_name='state',
            old_name='stateDesc',
            new_name='state_desc',
        ),
        migrations.RenameField(
            model_name='state',
            old_name='stateName',
            new_name='state_name',
        ),
        migrations.RenameField(
            model_name='state',
            old_name='stateUrl',
            new_name='state_url',
        ),
        migrations.RenameField(
            model_name='state',
            old_name='stateUUID',
            new_name='state_uuid',
        ),
        migrations.RemoveField(
            model_name='diff',
            name='diffImgName',
        ),
        migrations.RemoveField(
            model_name='diff',
            name='sourceImg',
        ),
        migrations.RemoveField(
            model_name='diff',
            name='targetImg',
        ),
        migrations.RemoveField(
            model_name='image',
            name='height',
        ),
        migrations.RemoveField(
            model_name='image',
            name='imgName',
        ),
        migrations.RemoveField(
            model_name='image',
            name='width',
        ),
        migrations.RemoveField(
            model_name='pr',
            name='gitPRCommit',
        ),
        migrations.RemoveField(
            model_name='pr',
            name='gitSourceCommit',
        ),
        migrations.RemoveField(
            model_name='pr',
            name='gitTargetCommit',
        ),
        migrations.AddField(
            model_name='diff',
            name='diff_img_file',
            field=models.ImageField(default='', upload_to='media/img'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='diff',
            name='source_img',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='source_img_in_Diff', to='HookCatcher.Image'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='diff',
            name='target_img',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='target_img_in_Diff', to='HookCatcher.Image'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='img_file',
            field=models.ImageField(default='', upload_to='media/img'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pr',
            name='git_pr_commit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merge_commit_in_PR', to='HookCatcher.Commit'),
        ),
        migrations.AddField(
            model_name='pr',
            name='git_source_commit',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='source_commit_in_PR', to='HookCatcher.Commit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pr',
            name='git_target_commit',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='target_commit_in_PR', to='HookCatcher.Commit'),
            preserve_default=False,
        ),
    ]
