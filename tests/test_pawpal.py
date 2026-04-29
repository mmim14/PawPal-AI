import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pawpal_system import Pet, Owner, Task


def test_mark_complete_updates_status():
    pet = Pet("Minmin", "Cat", "American Shorthair", 5, "Female")
    task = Task(task_type="vet", pet=pet, date="2026-04-15 11:00 AM", notes="Checkup")
    assert task.status == "pending"
    task.mark_complete()
    assert task.status == "completed"


def test_adding_task_increases_task_count():
    owner = Owner("Mimi")
    pichu = Pet("Pichu", "Cat", "American Shorthair", 1.5, "Male")
    owner.add_pet(pichu)
    assert pichu.task_count == 0
    owner.scheduler.schedule_feeding_time(pichu, "2026-04-01", "every 4 hours")
    assert pichu.task_count == 1


def test_task_duration_and_priority_are_stored():
    pet = Pet("Buddy", "Dog", "Beagle", 4, "Male")
    task = Task(
        task_type="feeding",
        pet=pet,
        date="2026-05-01 08:00",
        frequency="daily",
        duration=20,
        priority="high",
    )
    assert task.duration == 20
    assert task.priority == "high"
    summary = task.get_summary()
    assert "Duration: 20 mins" in summary
    assert "Priority: high" in summary


def test_schedule_walk_sets_duration_and_priority():
    owner = Owner("Mimi")
    buddy = Pet("Buddy", "Dog", "Beagle", 4, "Male")
    owner.add_pet(buddy)
    owner.scheduler.schedule_walk(
        buddy,
        "2026-05-02 07:00",
        duration=30,
        frequency="daily",
        notes="Morning walk",
        priority="low",
    )
    assert buddy.task_count == 1
    task = buddy.tasks[0]
    assert task.task_type == "walks"
    assert task.duration == 30
    assert task.priority == "low"
