"""Models for Topsy content."""

from django.utils import timezone
from django.db import models
from . import entities


class NoteManager(models.Manager):
    """Helper functions for notes."""

    def from_entity(self, entity):
        return self.model(
            id=entity.id,
            title=entity.title,
            body=entity.body,
            board=entity.board_id,
            created_by=entity.created_by,
            created_at=entity.created_at,
            modified_at=entity.modified_at,
            status=entity.status
        )


class Note(models.Model):
    """All Topsy content is contained in Notes."""

    title = models.CharField(max_length=150)
    body = models.TextField()
    board = models.ForeignKey('Board', null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateField()
    modified_at = models.DateField()
    status = models.CharField(max_length=50)

    objects = NoteManager()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()

        self.modified_at = timezone.now()

        super(Note, self).save(*args, **kwargs)

    def to_entity(self):
        return entities.Note(
            id=self.id,
            title=self.title,
            body=self.body,
            board_id=self.board.id if self.board else None,
            created_by=self.created_by,
            created_at=self.created_at,
            modified_at=self.modified_at,
            status=self.status
        )


class Board(models.Model):
    """Boards are containers for notes."""

    name = models.CharField(max_length=150)