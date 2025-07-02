from django.db import models

# Create your models here.

class LessonPlan(models.Model):
    title = models.CharField(max_length=200, verbose_name="教案标题")
    duration = models.PositiveIntegerField(verbose_name="授课时长（分钟）", default=45)
    objectives = models.TextField(verbose_name="教学目标")
    key_points = models.TextField(verbose_name="教学重点")
    difficult_points = models.TextField(verbose_name="教学难点")
    content = models.TextField(verbose_name="课程内容")
    ideological_points = models.TextField(verbose_name="课程思政点", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
