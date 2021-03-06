from __future__ import unicode_literals

import os
import uuid

import requests
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
@python_2_unicode_compatible
class Commit(models.Model):
    git_repo = models.CharField(max_length=200)
    git_branch = models.CharField(max_length=200)
    git_hash = models.CharField(unique=True, max_length=200)

    # function to retrieve a list of images that pertain to this PR
    def get_images(self):
        image_list = []  # list of image objects pertain to this commit
        states = self.state_set.all()
        for state in states:
            image_list.extend(state.image_set.all())
        return image_list

    def __str__(self):
        return '%s/%s %s' % (self.git_repo, self.git_branch, self.git_hash)


# Fields that make a state unique: stateName, gitRepo, gitBranch, gitCommit
@python_2_unicode_compatible
class State(models.Model):
    state_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    state_name = models.CharField(max_length=200)
    state_desc = models.TextField()
    state_url = models.TextField()
    git_commit = models.ForeignKey(Commit, on_delete=models.CASCADE)  # many commits for one state

    def __str__(self):
        return '%s, %s:%s %s' % (self.state_name,
                                 self.git_commit.git_repo,
                                 self.git_commit.git_branch,
                                 self.git_commit.git_hash[:7])


@python_2_unicode_compatible
class PR(models.Model):
    git_repo = models.CharField(max_length=200)
    git_pr_number = models.IntegerField(unique=True)
    # BASE of the git pull request Before version of state
    # call state.gitCommit.targetCommit_set.all() to get PR's where state is used as a target
    git_target_commit = models.ForeignKey(Commit, related_name='target_commit_in_PR',
                                          on_delete=models.CASCADE)
    # HEAD of the git pull request After version of state
    git_source_commit = models.ForeignKey(Commit, related_name='source_commit_in_PR',
                                          on_delete=models.CASCADE)

    # function to retrieve a list of diffs that pertain to this PR
    def get_diffs(self):
        target_diff_list = []  # final list of diff objects that pertain to this pr
        source_diff_list = []
        # get 2 lists of images for target and source commit
        # find the common diffs from the diffs linked to those images
        for target_image in self.git_target_commit.get_images():
            target_diff_list.extend(target_image.target_img_in_Diff.all())

        for source_image in self.git_source_commit.get_images():
            source_diff_list.extend(source_image.source_img_in_Diff.all())

        # find the intersection between the two lists in case image is used in mulitple diffs
        return set(target_diff_list) & set(source_diff_list)

    def num_diffs_approved(self):
        count_approved = 0
        for diff in self.get_diffs():
            if diff.is_approved:
                count_approved = count_approved + 1
        return count_approved

    def __str__(self):
        return '%s: PR #%d' % (self.git_repo, self.git_pr_number)


@python_2_unicode_compatible
class History(models.Model):
    time = models.DateTimeField(auto_now=True)
    message = models.TextField()
    is_error = models.BooleanField(default=False)
    pr = models.ForeignKey(PR, on_delete=models.CASCADE)

    # record actions in a Pull Request Event Payload to History
    @classmethod
    def log_pr_action(cls, pr_obj, git_payload_action, username):
        msg = 'PR #{0} has been {1} by {2}'.format(pr_obj.git_pr_number,
                                                   git_payload_action,
                                                   username)
        cls(message=msg, pr=pr_obj).save()
        return

    # record how many diffs were generated and how many still avaliable in history
    @classmethod
    def log_initial_diffs(cls, pr_obj, num):
        msg = '{0} Diffs were generated, of which {1} were automatically approved'.format(
              len(pr_obj.get_diffs), pr_obj.num_diffs_approved())

        cls(message=msg, pr=pr_obj).save()
        return

    # record in history when a user manually approves of a diff
    @classmethod
    def log_user_approval(cls, pr_obj, diff_obj, username):
        msg = 'Diff of state "{0}" was approved by "{1}"'.format(
              diff_obj.target_img.state.state_name, username)
        cls(message=msg, pr=pr_obj).save()
        return

    # record in history any internal system errors
    @classmethod
    def log_sys_error(cls, pr_obj, error_message):
        msg = 'INTERNAL SYSTEM ERROR: {0}'.format(error_message)
        cls(message=msg, pr=pr_obj, is_error=True).save()
        return

    def __str__(self):
        return 'PR #%d: %s' % (self.pr.git_pr_number, self.message)


@python_2_unicode_compatible
class Image(models.Model):
    img_file = models.ImageField(upload_to='img', max_length=2000, null=True, blank=True)
    browser_type = models.CharField(max_length=200)
    operating_system = models.CharField(max_length=200)
    device_res_width = models.IntegerField()
    device_res_height = models.IntegerField()
    # many Images to one State (for multiple browsers)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    # Help check if the image is currently loading or not. Return True if done loaded
    def image_rendered(self):
        # callback images have no file name when rendering
        return not (self.img_file == None or self.img_file.name == '')  # noqa: E711

    # Returns the full path of the image_file or the url depending on where it stored
    def get_image_location(self):
        validator = URLValidator()
        try:
            validator(self.img_file.name)
            return self.img_file.name
        except ValidationError:  # is not a url
            return self.img_file.path

    # Validates if an image file exists whether as a url or a local image
    def image_exists(self):
        # If there is even a name to validate
        if self.image_rendered():
            # check if the file name is url or nah and see if that url is real
            validator = URLValidator()
            try:
                validator(self.img_file.name)
                return requests.get(self.img_file.name).status_code == 200
            except ValidationError:
                return os.path.exists(self.img_file.path)
        else:
            return False

    def __str__(self):
        # if the img_file doesn't exist and therefore has no file name, print so
        if not self.image_rendered():
            # for the case when the image is not done loading yet
            return 'Image File is Currently Processing...'
        else:
            return self.img_file.name


@python_2_unicode_compatible
class Diff(models.Model):
    diff_img_file = models.ImageField(upload_to='img', max_length=2000, null=True, blank=True)
    # GITHUB BASE of a PR (before state), many Diffs to one Image
    target_img = models.ForeignKey(Image, related_name='target_img_in_Diff',
                                   on_delete=models.CASCADE)
    # GITHUB HEAD of a PR (after state)
    source_img = models.ForeignKey(Image, related_name='source_img_in_Diff',
                                   on_delete=models.CASCADE)
    diff_percent = models.DecimalField(max_digits=6, decimal_places=5, default=0)
    is_approved = models.BooleanField(default=False)

    # Help check if the image is currently loading or not. Return True if rendered
    def diff_image_rendered(self):
        # callback images have no file name when rendering
        return not self.diff_img_file == None and not self.diff_img_file.name == ''  # noqa: E711

    def __str__(self):
        if not self.diff_image_rendered():
            # for the case when the image is not done loading yet
            return 'Diff is waiting on Images to Process...'
        else:
            return self.diff_img_file.name
