from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from student.student_crud_models import Attendance, AttendanceRecord


class Command(BaseCommand):
    help = 'Send daily attendance report to students for previous day'

    def handle(self, *args, **options):
        yesterday = timezone.localdate() - timezone.timedelta(days=1)
        sessions = Attendance.objects.filter(date=yesterday)
        if not sessions.exists():
            self.stdout.write(f'No attendance sessions found for {yesterday}')
            return

        # For each attendance session, email its students
        for session in sessions:
            records = AttendanceRecord.objects.filter(attendance=session).select_related('student')
            for rec in records:
                student = rec.student
                if not student.email:
                    continue
                status = 'Present' if rec.present else 'Absent'
                subject = f'Attendance report for {yesterday}'
                message = f'Dear {student.name},\n\nYour attendance for {yesterday} is: {status}.\n\nRegards,\nSchool Admin'
                try:
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [student.email], fail_silently=True)
                except Exception as e:
                    self.stdout.write(f'Failed to send to {student.email}: {e}')

        self.stdout.write('Daily attendance emails processed.')
