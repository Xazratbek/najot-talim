from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime

def generate_uuid():
    return uuid4().hex[:10]

class TaskSystemError(Exception):
    """Task tizimidagi barcha xatolar uchun asos"""
    pass

class InvalidStatusTransitionError(TaskSystemError):
    """Status noto'g'ri o'zgartirilganda chiqadi"""
    pass

class UserNotAuthorizedError(TaskSystemError):
    """Ruxsati bo'lmagan foydalanuvchi harakat qilganda chiqadi"""
    pass

class User:
    def __init__(self,username, role):
        self.__uuid = generate_uuid()
        self.username = username
        self.__role = role

    def __str__(self):
        return f"ID: {self.__uuid} | Username: {self.username} | Role: {self.__role}"

    def get_username(self):
        return self.username

    def set_username(self,new_username):
        self.username = new_username
        return self.username

    @property
    def uuid(self):
        return self.__uuid

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self,new_role):
        self.__role = new_role

class TaskStatus(Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"

    def is_finished(self):
        return self in (TaskStatus.DONE, TaskStatus.BLOCKED)

class TaskType(Enum):
    BUG = "bug"
    FEATURE = "feature"

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    @staticmethod
    def from_score(to_score: int):
        if 1 <= to_score <= 5:
            return TaskPriority.LOW
        elif 6 <= to_score <= 7:
            return TaskPriority.MEDIUM
        elif 8 <= to_score <= 10:
            return TaskPriority.HIGH
        else:
            raise ValueError("Required score out of range")

class WorkflowRule:
    def __init__(
        self,
        from_status: TaskStatus,
        to_status: TaskStatus
        ):
        self.from_status = from_status
        self.to_status = to_status

    def check_status_change(self,current_status,new_status):
        if self.from_status == current_status and self.to_status == new_status:
            return True
        return False

@dataclass
class TaskEvent:
    task_id: int
    old_status: TaskStatus
    new_status: TaskStatus
    changed_by: User
    timestampt: datetime

class NotificationService(ABC):
    @abstractmethod
    def send(self,message: str, message_to: User) -> None:
        pass

class EmailNotificationService(NotificationService):
    def send(self,message: str, message_to: User):
        print(f"Email notification ishga tushdi\nXabar: {message} | {message_to.username}-userga yuborildi")

class SlackNotificationService(NotificationService):
    def __init__(self, channel_id: int):
        self.channel_id = channel_id

    def send(self, message: str, receiver: User):
        line = f"Slack notification ishga tushdi\n: '{message}' -> Kanal id: {self.channel_id} (Qabul qiluvch: {receiver.username})"
        n = len(line)

        print("┌" + "─" * (n + 2) + "┐")
        print("│ " + line + " │")
        print("└" + "─" * (n + 2) + "┘")

@dataclass(frozen=True)
class TaskDTO:
    id: int
    title: str
    status: TaskStatus
    task_type: TaskType
    task_priority: TaskPriority
    assigned_to: str | None

class Task:
    def __init__(
        self,
        title: str,
        description: str,
        task_status: TaskStatus,
        task_type: TaskType,
        created_by: User,
        assigned_to: User | None,
        notification_service: NotificationService
    ):
        self.id = generate_uuid()
        self.title = title
        self.description = description
        self.__status = task_status
        self.task_type = task_type
        self.created_by = created_by
        self.assigned_to = assigned_to
        self.events = []
        self.workflow_rules = []
        self.notification_service = notification_service
        self.task_dto = []

        self.notification_service.send(f"Yangi task yaratildi: {self.title}\nTask: {self.description}\nAssigned to: {self.assigned_to}\nTask created by: {self.created_by.username}",self.created_by)

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self,new_status):
        self.__status = new_status

    def __str__(self):
        return f"ID: {self.id}\nTitle: {self.title}\nDescription: {self.description}\nStatus: {self.__status.value}\nTask type: {self.task_type.value}\nCreated by: {self.created_by.username}\nAssigned to: {self.assigned_to.username if self.assigned_to is not None else "Not assigned"}\n"

    def add_event(self, event: TaskEvent):
        self.events.append(event)

    def add_task_dto(self, task_dto: TaskDTO):
        self.task_dto.append(task_dto)

    def get_task_dtos(self):
        return self.task_dto

    def assign_user(self, user: User):
        if self.created_by.uuid != user.uuid and user.role.lower() != "admin":
            self.assigned_to = user
            self.notification_service.send(f"{self.created_by.get_username()} -> {user.get_username()}-ga vazifani topshirdi.\nTask ID: {self.id}\nTask: {self.title}\nAssigned at: {datetime.now().strftime("%d-%B-%Y %H:%M")}",user)
            new_event = TaskEvent(self.id,self.__status,self.__status,self.created_by,datetime.now().strftime("%d-%B-%Y %H:%M"))
            self.events.append(new_event)

            return f"Task assigned to user: {user.get_username()}\n"
        return f"Task can not be assigned to user: {user.get_username()}"

    def unassign(self,user: User):
        if self.assigned_to is not None and self.assigned_to.uuid == user.uuid:
            self.assigned_to = None
            self.notification_service.send(f"Task: {self.title}-vazifasini bajarish sizdan olib tashlandi.\nID: {self.id}",user)
            new_event = TaskEvent(self.id,self.__status,self.__status,user,datetime.now())
            self.events.append(new_event)
            return f"Task: {self.title} - id: {self.id}\n Unassigned from user: {self.assigned_to.username}"

        raise ValueError(f"Task: {self.title} ID: {self.id} can not be assigned from user: {user.username}")

    def change_task_status(self,new_status):
        can_change = False
        for rule in self.workflow_rules:
            if rule.check_status_change(self.__status,new_status):
                can_change = True
                break

        if not can_change:
            raise InvalidStatusTransitionError(f"Xatolik!\nTask statusni: {self.__status.value} -> {new_status.value}-ga o'zgartirib bo'lmaydi!")

        old_status = self.__status
        self.__status = new_status
        new_event = TaskEvent(
            self.id,old_status,new_status,self.created_by,datetime.now().strftime("%d-%B-%Y %H:%M")
        )
        self.add_event(new_event)
        return f"Task:{self.title}-statusi {old_status.value} dan {new_status.value} ga o'zgardi va tarixga yozildi."

    def get_task_type(self):
        return f"Task type: {self.task_type.value}"

    def get_title(self):
        return f"Task title: {self.title}"

    def get_description(self):
        return f"Task description: {self.description}"

    def get_task_events(self):
        data = ""
        if self.events:
            for event in self.events:
                data += f"Task Events History\n ID: {event.task_id} | Old status: {event.old_status.value} | new_status: {event.new_status.value} | Changed by: {event.changed_by.username} | timestampt: {event.timestampt}" + "\n"
            return data
        return "Events mavjud emas!"

    def add_worklow_rule(self,from_status,to_status):
        workflow = WorkflowRule(from_status,to_status)
        if workflow.check_status_change(self.status,to_status):
            self.workflow_rules.append(workflow)
        else:
            return "Workflow can not be written because status is not changed"

    def change_task_type(self,new_task_type):
        if not isinstance(new_task_type,TaskType):
            raise ValueError("Yaroqsiz TaskType!")

        if self.task_type != new_task_type:
            old_task_type = self.task_type
            self.task_type = new_task_type
            return f"Task: {self.title}\nTask turi: {old_task_type}-dan {new_task_type}-ga o'zgartirildi!"
        else:
            raise ValueError("Vazifa tipini o'zgartirish uchun yangi vazifa turini kiriting!")


print("Notification servicelar yaratish boshlandi...")
email_notification_service = EmailNotificationService()
slack_notification_service = SlackNotificationService(1411196712)
print("Notification servicelar yaratish tugadi...\n\nUserlar yaratish boshlandi...\n")

user_1 = User("xazratbek","admin")
user_2 = User("Adminjon","student")
user_3 = User("Nozimjon","student")

print(f"User_1 username: {user_1.get_username()}")
print(f"User_1 role: {user_1.role}")

print(f"User_2 username: {user_2.get_username()}")
print(f"User_2 role: {user_2.role}")
print(f"User_3 username: {user_3.get_username()}")
print(f"User_3 role: {user_3.role}")

print("\bUserlar yaratish tugadi...\nTasklar yaratish boshlandi...\n")

task_1 = Task(title="@property decoratorni o'rganish",description="@property decoratiri ishlatilgan biror bir mini loyiha qilish",task_status=TaskStatus.DRAFT,task_type=TaskType.FEATURE,assigned_to=None,created_by=user_1,notification_service=email_notification_service)

task_2 = Task(title="So'z yodlash",description="100-ta yangi so'z yod olish",task_status=TaskStatus.DRAFT,task_type=TaskType.FEATURE,assigned_to=None,created_by=user_2,notification_service=slack_notification_service)

print(f"\nTasklar yaratish tugadi...\nTask: {task_1.title}-taski bilan amaliyotlar boshlandi, task id: {task_1.id}")

print(f"Task 1 status: {task_1.status.value}")
print(task_1.get_description())
print(f"Task 1 type: {task_1.get_task_type()}")
print(task_1.assign_user(user_3))
print(task_1)
print(task_1.add_worklow_rule(task_1.status,TaskStatus.IN_PROGRESS))
print(task_1.change_task_status(TaskStatus.IN_PROGRESS))
print(task_1.add_worklow_rule(task_1.status,TaskStatus.DONE))
print(task_1.get_task_events())