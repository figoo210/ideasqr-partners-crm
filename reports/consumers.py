import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from datetime import datetime, timedelta
from django.db.models import Q
from django.utils import timezone

from accounts.models import CustomUser, Shift
from submissions.models import Submission


class ChartConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("#########################: Connected")
        await self.accept()

    async def disconnect(self, close_code):
        print("#########################: Closed")

    async def receive(self, text_data):
        # handle received data
        try:
            data = json.loads(text_data)
            print("################################ Received data: ", data)
        except:
            print("################################ text_data data: ", text_data)
            team_leaders_names, submissions_data = await self.handle_database_query(
                text_data
            )

        # Process the data as needed and send updates
        await self.send(
            text_data=json.dumps(
                {
                    "team_leaders": team_leaders_names,
                    "submissions_data": submissions_data,
                }
            )
        )

    @database_sync_to_async
    def handle_database_query(self, data):
        queryset = CustomUser.objects.filter(role="Team Leader").all()
        team_leaders_names = [item.username for item in queryset]
        submissions_data = []

        for tln in team_leaders_names:
            submissions_data.append(0)

        for indx, usr in enumerate(queryset):
            counter = 0
            counter = Submission.objects.filter(Q(user_queue__user=usr)).count()
            team_leader_employees = CustomUser.objects.filter(team_leader=usr).all()
            counter = (
                counter
                + Submission.objects.filter(
                    Q(user_queue__user__in=team_leader_employees)
                ).count()
            )
            submissions_data[indx] = counter

        return team_leaders_names, submissions_data


class RealtimeDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("#########################: Realtime Connected")
        await self.accept()

    async def disconnect(self, close_code):
        print("#########################: Realtime Closed")

    async def receive(self, text_data):
        # handle received data
        print("################################ text_data data: ", text_data)
        teams = await self.handle_database_query()

        # Process the data as needed and send updates
        await self.send(text_data=json.dumps({"teams": teams}))

    @database_sync_to_async
    def handle_database_query(self):
        queryset = CustomUser.objects.filter(
            is_superuser=False, is_staff=False, role="Team Leader"
        ).all()
        teams = [
            {"team_leader": item.username, "total_submissions": 0, "employees": []}
            for item in queryset
        ]

        current_date = timezone.now()
        shift_time = Shift.objects.get(pk=1)
        start_of_today = current_date.replace(
            hour=shift_time.start_time.hour or 16,
            minute=shift_time.start_time.minute or 0,
            second=shift_time.start_time.second or 0,
            microsecond=shift_time.start_time.microsecond or 0,
        )
        end_of_today = current_date.replace(
            hour=shift_time.end_time.hour or 2,
            minute=shift_time.end_time.minute or 0,
            second=shift_time.end_time.second or 0,
            microsecond=shift_time.end_time.microsecond or 0,
        ) + timedelta(days=1)

        start_of_week = current_date - timedelta(days=current_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month.replace(
            month=current_date.month + 1, day=1
        ) - timedelta(days=1)

        for indx, usr in enumerate(queryset):
            counter = 0
            counter = Submission.objects.filter(Q(user_queue__user=usr)).count()
            team_leader_employees = CustomUser.objects.filter(team_leader=usr).all()
            # get each employee number of submissions
            teams[indx]["employees"] = [
                {
                    "employee_username": emp.username,
                    "number_of_submissions": Submission.objects.filter(
                        Q(user_queue__user=emp)
                    ).count(),
                    # Day
                    "number_of_today_submissions": Submission.objects.filter(
                        Q(user_queue__user=emp),
                        created_at__range=(start_of_today, end_of_today),
                    ).count(),
                    # Week
                    "number_of_week_submissions": Submission.objects.filter(
                        Q(user_queue__user=emp),
                        created_at__range=(start_of_week, end_of_week),
                    ).count(),
                    # Month
                    "number_of_month_submissions": Submission.objects.filter(
                        Q(user_queue__user=emp),
                        created_at__range=(start_of_month, end_of_month),
                    ).count(),
                }
                for emp in team_leader_employees
            ]
            # get all team total submissions
            counter = (
                counter
                + Submission.objects.filter(
                    Q(user_queue__user__in=team_leader_employees)
                ).count()
            )
            teams[indx]["total_submissions"] = counter
        return teams
